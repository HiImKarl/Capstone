import numpy as np
from flask import (
    Blueprint, abort, request, jsonify, render_template
)
from app.db import (
    get_db, get_covariance_matrix, get_mu_vector, get_market_caps, get_prices, get_user_portfolio
)
from app.data import TICKERS, RISK_FREE, TODAY_DATETIME
from app.util import first_item_in_list
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
    user_id = float(request.args.get('user_id'))
    portfolio = get_user_portfolio(user_id)
    return jsonify(portfolio)


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
def md_mvo_test():
    cor = cov_to_cor(get_covariance_matrix())
    return jsonify(cor)


@bp.route('/back_test_user', methods=('GET',))
def back_test_user_portfolio():
    """
    n = # of assets
    m = # of data points (weekly)
    :param portfolio: n x 1 np array;
    :return: m x 1 np array; back tested caps of the portfolio
    """

    # always backtest using 5 years of data
    user_id = float(request.args.get('user_id'))
    portfolio = get_user_portfolio(user_id)
    start_date = TODAY_DATETIME - relativedelta(years=5)
    prices_all = get_prices(start_date, TODAY_DATETIME, portfolio['ticker'])

    assert len(prices_all) == len(portfolio['ticker'])
    assert len(prices_all) == len(portfolio['amount'])
    market_caps = []

    for i in range(len(first_item_in_list(prices_all))):
        market_cap = 0
        for j in range(len(prices_all)):
            market_cap += prices_all[j][i] * portfolio['amount'][j]
        market_caps.append(market_cap)

    return jsonify(market_caps)


# FIXME TESTING
@bp.route('/prices')
def prices_test():
    start_date = TODAY_DATETIME - relativedelta(years=5)
    prices_all = get_prices(start_date, TODAY_DATETIME, TICKERS)
    return jsonify(prices_all.tolist())


# FIXME TESTING
@bp.route('/mvo', methods=('GET', ))
def mvo_test():
    mu_goal = float(request.args.get('mu_goal'))
    if not mu_goal:
        abort(404)
    cov = get_covariance_matrix()
    mu = get_mu_vector()
    rf = RISK_FREE[-1]

    portfolio, port_var, port_ret = mvo(cov, mu, mu_goal, rf, 0)
    return jsonify({
        'portfolio': portfolio.tolist(),
        'var': port_var,
        'ret': port_ret
    })
