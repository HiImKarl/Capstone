import sqlite3
import click
import numpy as np
from app.data import get_asset_data, FF_FACTORS, RISK_FREE, TODAY_DATETIME, TICKERS
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
    times.reverse()
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
    xff_covariances = ff3_cov_est(xreturns, xfactors, xrisk_free, xcoefficients)

    ff_returns = xff_returns.tolist()
    ff_covariances = xff_covariances.tolist()

    assert(len(ff_returns) == len(TICKERS))
    assert(len(ff_covariances) == len(TICKERS))
    assert(len(ff_covariances[0]) == len(TICKERS))

    db.executemany(
        'INSERT INTO Asset (ticker, average_return, market_cap, price) VALUES (?, ?, ?, ?)',
        zip(TICKERS, ff_returns, [value[-1] for key, value in market_caps.items()],
            [value[-1] for key, value in prices.items()])
    )

    for i in range(len(xff_covariances)):
        for j in range(len(xff_covariances)):
            db.execute(
                'INSERT INTO Covariance (ticker1, ticker2, covariance) VALUES (?, ?, ?)',
                (TICKERS[i], TICKERS[j], ff_covariances[i][j])
            )

    for TICKER in TICKERS:
        for i in range(len(times)):
            db.execute(
                'INSERT INTO WeeklyAssetData (ticker, date_time, price, market_cap)'
                'VALUES (?, ?, ?, ?)',
                (TICKER, times[i], prices[TICKER][i], market_caps[TICKER][i],)
            )

    for i in range(len(times)):
        db.execute(
            'INSERT INTO WeeklyMarketData (date_time, capm, small_vs_big, high_vs_low, risk_free_rate)'
            'VALUES (?, ?, ?, ?, ?)',
            (times[i], factors[i][0], factors[i][1], factors[i][2], risk_free[i])
        )

    db.commit()


def get_covariance_matrix(tickers):
    db = get_db()
    cov_matrix = np.zeros((len(tickers), len(tickers)), dtype=np.float64)
    for i in range(len(tickers)):
        for j in range(len(tickers)):
            cov = db.execute(
                'SELECT covariance FROM Covariance WHERE ticker1 = ? AND ticker2 = ?',
                (tickers[i], tickers[j], )
            ).fetchone()
            cov_matrix[i][j] = cov['covariance']

    return cov_matrix


def get_mu_vector():
    db = get_db()
    mu_vector = np.zeros((len(TICKERS), ), dtype=np.float64)
    for i in range(len(TICKERS)):
        mu = db.execute(
            'SELECT average_return FROM Asset WHERE ticker = ?',
            (TICKERS[i], )
        ).fetchone()
        mu_vector[i] = mu['average_return']

    return mu_vector


def get_market_caps(tickers):
    db = get_db()
    market_caps = np.zeros((len(tickers), ), dtype=np.float64)
    for i in range(len(tickers)):
        market_cap = db.execute(
            'SELECT market_cap FROM Asset WHERE ticker = ?',
            (tickers[i], )
        ).fetchone()
        market_caps[i] = market_cap['market_cap']

    return market_caps


def get_views(tickers):
    db = get_db()
    views = np.zeros((len(tickers), ), dtype=np.float64)
    for i in range(len(tickers)):
        view = db.execute(
            'SELECT views FROM Asset WHERE ticker = ?',
            (tickers[i], )
        ).fetchone()
        views[i] = view['views']

    return views


def get_portfolio_id(user_id):
    db = get_db()
    portfolio_id = db.execute(
        'SELECT portfolio_id FROM Portfolio '
        'WHERE user_id = ?',
        (user_id, )
    ).fetchone()['portfolio_id']

    return portfolio_id


def get_portfolio(portfolio_id):
    db = get_db()
    portfolio = db.execute(
        'SELECT ticker, amount, views FROM PortfolioAsset '
        'WHERE portfolio_id = ?',
        (portfolio_id, )
    ).fetchall()

    portfolio = [dict(row) for row in portfolio]
    json_portfolio = {'amount': [], 'ticker': [], 'views': []}
    for row in portfolio:
        json_portfolio['ticker'].append(row['ticker'])
        json_portfolio['amount'].append(row['amount'])
        json_portfolio['views'].append(row['views'])

    return json_portfolio


def get_prices(start_date, end_date, tickers):
    """
    n = # of assets
    m = # of data points
    :return: n x m np array; for each asset, the historical prices
    """
    db = get_db()
    prices_all = []
    for ticker in tickers:
        db_price_data = db.execute(
            'SELECT price FROM WeeklyAssetData '
            'WHERE ticker = ? '
            'AND date_time >= ? ' 
            'AND date_time <= ? ',
            (ticker, start_date, end_date,)
        ).fetchall()
        prices = []
        for row in db_price_data:
            prices.append(row['price'])
        prices_all.append(prices)

    # FIXME assertions
    for prices in prices_all:
        assert len(prices) == len(prices_all[0])

    return np.array(prices_all)


def get_returns(tickers):
    """
    n = # of assets
    m = # of data points
    :return: n x m np array; for each asset, the returns
    """
    db = get_db()
    returns = np.zeros((len(tickers), ), dtype=np.float64)
    for i in range(len(tickers)):
        db_return = db.execute(
            'SELECT average_return FROM Asset '
            'WHERE ticker = ?',
            (tickers[i], )
        ).fetchone()
        returns[i] = db_return['average_return']

    return returns


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized Database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

