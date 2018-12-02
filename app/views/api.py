import numpy as np
import math
from flask import (
    Blueprint, abort, request, jsonify, render_template
)
from app.db import (
    get_db, get_covariance_matrix, get_mu_vector, get_views, get_portfolio_id,
    get_market_caps, get_prices, get_portfolio, get_returns
)
from app.data import TICKERS, RISK_FREE, TODAY_DATETIME
from app.util import first_item_in_list
from business_logic.black_litterman import black_litterman
from business_logic.md_mvo import cov_to_cor, md_mvo
from business_logic.mvo import mvo
from business_logic.var import p_metrics
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
    portfolio_id = get_portfolio_id(user_id)
    portfolio = get_portfolio(portfolio_id)
    return jsonify(portfolio)


# FIXME TESTING
@bp.route('/black_litterman', methods=('GET',))
def black_litterman_test():
    cov = get_covariance_matrix(TICKERS)
    mu = get_mu_vector()
    market_caps = get_market_caps()
    rf = RISK_FREE[-1]
    return jsonify(black_litterman(mu, cov, rf, market_caps).tolist())


# FIXME TESTING
@bp.route('/md_mvo', methods=('GET',))
def md_mvo_test():
    cardinality = float(request.args.get('cardinality'))
    cor = cov_to_cor(get_covariance_matrix(TICKERS))
    buckets = md_mvo(cor, cardinality)
    return jsonify(buckets.tolist())


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


def map_view(view):
    if view == -2:
        return 1.2
    elif view == -1:
        return 1.1
    elif view == 0:
        return 1.0
    elif view == 1:
        return 0.9
    elif view == 2:
        return 0.8
    else:
        assert 0


@bp.route('/improve_portfolio', methods=('GET', ))
def improve_portfolio():
    user_id = request.args.get('user_id')
    if not user_id:
        abort(404)

    user_id = int(user_id)
    portfolio_id = get_portfolio_id(user_id)
    portfolio = get_portfolio(portfolio_id)
    tickers = portfolio['ticker']
    returns = get_returns(tickers)
    views = portfolio['views']

    market_caps = get_market_caps(tickers)
    cov = get_covariance_matrix(tickers)
    risk_free_rate = RISK_FREE[-1]
    views = [map_view(view) for view in views]

    portfolio = black_litterman(returns, cov, risk_free_rate, market_caps, views)
    mu_p, sd_p, sharpe_p = p_metrics(portfolio, views * returns, cov, risk_free_rate)
    return jsonify(
        {
            'ticker': tickers,
            'weights': portfolio.tolist(),
            'return': mu_p,
            'sigma': sd_p,
            'sharpe_p': sharpe_p
        }
    )


# FIXME TESTING
@bp.route('/mvo', methods=('GET', ))
def mvo_test():
    mu_goal = request.args.get('mu_goal')
    cardinality = request.args.get('cardinality')
    if not mu_goal or not cardinality:
        abort(404)
    mu_goal = float(mu_goal)
    mu_goal = (1 + mu_goal)**(1 / 52) - 1
    cardinality = float(cardinality)
    cov = get_covariance_matrix(TICKERS)
    mu = get_mu_vector()
    rf = RISK_FREE[-1]

    cor = cov_to_cor(cov)
    buckets = md_mvo(cor, cardinality)

    md_tickers = []
    md_mu = []

    assert len(TICKERS) == len(buckets)
    for i in range(len(TICKERS)):
        if buckets[i] == 0:
            continue

        md_tickers.append(TICKERS[i])
        md_mu.append(mu[i])

    md_cov = get_covariance_matrix(md_tickers)
    portfolio, port_var, port_ret = mvo(md_cov, md_mu, mu_goal, rf)

    port_ret = (1 + port_ret)**52 - 1
    sigma = math.pow(52 * port_var, 0.5)

    return jsonify({
        'tickers': md_tickers,
        'portfolio': portfolio.tolist(),
        'sigma': sigma,
        'ret': port_ret
    })
