import sqlite3
import click
import numpy as np
from app.data import get_asset_data, FF_FACTORS, RISK_FREE, TODAY_DATETIME, STOCK_TICKERS, ETF_TICKERS
from app.util import limit_list_size
from dateutil.relativedelta import relativedelta
from business_logic.farma_french import ff3_ols, ff3_cov_est, ff3_return_estimates
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # grab S&P500 and ETF asset data
    market_caps, prices = get_asset_data()
    assert(len(market_caps) == len(prices))

    # populate the asset and asset data tables
    returns = [[price_array[i] / price_array[i - 1] - 1 for i in range(1, len(price_array))]
               for ticker, price_array in prices.items()]

    times = [TODAY_DATETIME - relativedelta(weeks=i) for i in range(len(returns[0]))]
    assert(len(times) == len(returns[0]))

    xreturns = np.array(returns, dtype=np.dtype('float'))
    xreturns = np.transpose(xreturns)

    # make sure the factors are the same size as the returns
    # grab return and covariances from Farma French factor model
    factors = limit_list_size(FF_FACTORS, len(returns[0]))
    risk_free = limit_list_size(RISK_FREE, len(returns[0]))

    xfactors = np.array(factors, dtype=np.dtype('float'))
    xrisk_free = np.array(risk_free, dtype=np.dtype('float'))

    xcoefficients = ff3_ols(xreturns, xfactors, xrisk_free)

    xff_returns = ff3_return_estimates(xreturns, xfactors, xrisk_free, xcoefficients)
    xff_covariances = ff3_cov_est(xreturns, xfactors, xcoefficients)

    ff_returns = xff_returns.tolist()
    ff_covariances = xff_covariances.tolist()

    tickers = STOCK_TICKERS + ETF_TICKERS

    assert(len(ff_returns) == len(tickers))
    assert(len(ff_covariances) == len(tickers))
    assert(len(ff_covariances[0]) == len(tickers))

    db.executemany(
        'INSERT INTO Asset (ticker, average_return, price) VALUES (?, ?, ?)',
        zip(tickers, ff_returns, [value[-1] for key, value in prices.items()])
    )

    for i in range(len(xff_covariances)):
        for j in range(len(xff_covariances)):
            db.execute(
                'INSERT INTO Covariance (ticker1, ticker2, covariance) VALUES (?, ?, ?)',
                (tickers[i], tickers[j], ff_covariances[i][j])
            )

    for ticker in tickers:
        for i in range(len(times)):
            db.execute(
                'INSERT INTO WeeklyAssetData (ticker, date_time, price, market_cap)'
                'VALUES (?, ?, ?, ?)',
                (ticker, times[i], prices[ticker][i], market_caps[ticker][i],)
            )

    for i in range(len(times)):
        db.execute(
            'INSERT INTO WeeklyMarketData (date_time, capm, small_vs_big, high_vs_low, risk_free_rate)'
            'VALUES (?, ?, ?, ?, ?)',
            (times[i], factors[i][0], factors[i][1], factors[i][2], risk_free[i])
        )

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized Database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
