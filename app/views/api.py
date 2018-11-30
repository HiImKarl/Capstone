import numpy as np
from flask import (
    Blueprint, abort, request, jsonify, render_template
)
from app.db import get_db, get_covariance_matrix, get_mu_vector, get_market_caps, get_prices
from app.data import TICKERS, RISK_FREE, TODAY_DATETIME
from business_logic.black_litterman import black_litterman
from business_logic.md_mvo import cov_to_cor
from business_logic.mvo import mvo
from dateutil.relativedelta import relativedelta

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/assets', methods=('GET', ))
def assets():
    prices = []
    db = get_db()
    for TICKER in TICKERS:
        price = db.execute(
            'SELECT price FROM Asset WHERE ticker = ?', (TICKER, )
        ).fetchone()
        prices.append(price['price'])

    return jsonify(
        tickers=TICKERS,
        prices=prices
    )


# FIXME SECURITY ISSUE
@bp.route('/portfolios', methods=('GET', ))
def portfolios():
    user_id = request.args.get('user_id')
    assert(user_id is not None)
    db = get_db()
    portfolio = db.execute(
        'SELECT pa.ticker, pa.amount FROM User u '
        'INNER JOIN Portfolio p ON u.user_id = p.user_id '
        'INNER JOIN PortfolioAsset pa ON p.portfolio_id = pa.portfolio_id '
        'WHERE u.user_id = ?',
        (user_id, )
    ).fetchall()

    portfolio = [dict(row) for row in portfolio]
    json_portfolio = {'amount': [], 'ticker': []}
    for row in portfolio:
        json_portfolio['ticker'].append(row['ticker'])
        json_portfolio['amount'].append(row['amount'])
    return jsonify(json_portfolio)


# FIXME TESTING
@bp.route('/black_litterman', methods=('GET',))
def black_litterman():
    cov = get_covariance_matrix()
    mu = get_mu_vector()
    market_caps = get_market_caps()
    rf = RISK_FREE[-1]
    return jsonify(black_litterman(mu, cov, rf, market_caps).tolist())


# FIXME TESTING
@bp.route('/md_mvo', methods=('GET',))
def md_mvo():
    cor = cov_to_cor(get_covariance_matrix())
    return jsonify(cor)


def back_test_portfolio(portfolio, prices, rebalance=False):
    """
    n = # of assets
    m = # of data points (weekly)
    :param portfolio: n x 1 np array;
        for each asset, the 'shares' of the asset in the portfolio
    :param prices: n x m np array; for each asset, np array of historical prices
    :param rebalance: Set to True if rebalancing should be enabled
    :return: m x 1 np array; back tested caps of the portfolio
    """

    # always backtest using 5 years of data
    pass


# FIXME TESTING
@bp.route('/prices')
def prices():
    start_date = TODAY_DATETIME - relativedelta(years=5)
    prices_all = get_prices(start_date, TODAY_DATETIME, TICKERS)
    return jsonify(prices_all.tolist())


# FIXME TESTING
@bp.route('/mvo', methods=('GET', ))
def mvo_():
    mu_goal = float(request.args.get('mu_goal'))
    if not mu_goal:
        abort(404)
    cov = get_covariance_matrix()
    mu = get_mu_vector()
    print(mu)
    rf = RISK_FREE[-1]
    print(RISK_FREE)

    portfolio, port_var, port_ret = mvo(cov, mu, mu_goal, rf, 0)
    return jsonify({
        'portfolio': portfolio.tolist(),
        'var': port_var,
        'ret': port_ret
    })
