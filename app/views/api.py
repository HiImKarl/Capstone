import math
import numpy as np
from flask import (
    Blueprint, abort, request, jsonify
)
from app.db import (
    get_db, get_covariance_matrix, get_mu_vector, get_portfolio_id,
    get_market_caps, get_prices, get_portfolio, get_returns, get_current_prices
)
from app.data import TICKERS, RISK_FREE, TODAY_DATETIME, FF_FACTORS
from app.util import first_item_in_list, limit_list_size
from business_logic.black_litterman import black_litterman
from business_logic.md_mvo import cov_to_cor, md_mvo
from business_logic.mvo import mvo
from business_logic.var import p_metrics, monte_carlo, var_calc
from business_logic.farma_french import (
    ff3_cov_est, ff3_return_estimates, ff3_ols
)
from dateutil.relativedelta import relativedelta

bp = Blueprint('api', __name__, url_prefix='/api')
MONTE_CARLO_SIMULATIONS = 1000


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


@bp.route('/portfolios', methods=('GET', ))
def portfolios():
    user_id = request.args.get('user_id')
    if user_id is None:
        abort(404)
    portfolio_id = get_portfolio_id(float(user_id))
    if portfolio_id is None:
        return jsonify({})
    portfolio = get_portfolio(portfolio_id)
    return jsonify(portfolio)


@bp.route('/portfolio_statistics', methods=('GET',))
def portfolio_statistics():
    user_id = request.args.get('user_id')
    if user_id is None:
        abort(404)
    portfolio_id = get_portfolio_id(user_id)
    portfolio = get_portfolio(portfolio_id)
    tickers = portfolio['ticker']
    amounts = portfolio['amount']
    returns = get_returns(tickers)
    print(returns)
    covariance = get_covariance_matrix(tickers)
    prices = get_current_prices(tickers)

    total_value = 0
    for i in range(len(amounts)):
        total_value += amounts[i] * prices[i]

    weights = [(amounts[i] * prices[i]) / total_value
               for i in range(len(amounts))]

    mu_p = 0
    for i in range(len(weights)):
        mu_p += weights[i] * returns[i]

    weights = np.array(weights, dtype=np.float64)
    covariance = np.array(covariance, dtype=np.float64)

    cov_p = np.matmul(np.matmul(np.transpose(weights), covariance), weights)
    cov_p *= 52
    cov_p = math.pow(cov_p, 0.5)
    monte_carlo_simulations = monte_carlo(mu_p, cov_p, 52, MONTE_CARLO_SIMULATIONS)
    var, cvar = var_calc(monte_carlo_simulations, 0.01)

    mu_p = (1 + mu_p)**52 - 1
    yearly_rf = (1 + RISK_FREE[-1])**52 - 1
    sharpe_ratio = (mu_p - yearly_rf) / cov_p

    return jsonify({
        'sigma': cov_p,
        'sharpe_ratio': sharpe_ratio,
        'ret': mu_p,
        'var': var,
        'cvar': cvar
    })


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


def rebalance_portfolio(start_date, end_date, tickers, return_goal):
    """
    :param start_date:
    :param end_date:
    :param tickers:
    :return: new rebalancing weights
    """
    prices = get_prices(start_date, end_date, tickers)
    returns = [prices[i] / prices[i - 1] for i in range(len(prices))]
    factors = limit_list_size(FF_FACTORS, len(returns[0]))
    factors = np.array(factors, dtype=np.float64)
    risk_free = limit_list_size(RISK_FREE, len(returns[0]))
    risk_free = np.array(risk_free, dtype=np.float64)
    returns = np.array(returns, dtype=np.float64)
    returns = np.transpose(returns)

    coefficients = ff3_ols(returns, factors, risk_free)
    ff_returns = ff3_return_estimates(returns, factors, risk_free, coefficients)
    ff_covariances = ff3_cov_est(returns, factors, risk_free, coefficients)
    p_weights, p_var, p_return = mvo(ff_covariances,
                                     ff_returns, return_goal)

    return p_weights


def calculate_transaction_costs(shares, rebalanced_shares, prices):
    """
    n = # of tickers in portfolio
    :param shares: n x 1 array of shares before rebalancing
    :param rebalanced_shares: n x 1 array of shares after rebalancing
    :param prices: n x 1 array of asset costs
    :return: total cost of rebalancing
    """

    # FIXME isn't this too ligma?
    return 5 * len(shares)


@bp.route('/back_test_rebalancing_portfolio', methods=('GET', ))
def back_test_rebalancing_portfolio():
    """
    m = # of data points (weekly)
    :return: m x 1 np array; back tested capitalizations of
    the portfolio as a percentage of the initial value of the portfolio
    This will perform rebalancing
    """
    tickers = request.args.getlist('tickers[]')
    weights = request.args.getlist('weights[]')
    return_goal = request.args.get('return_goal')

    if not tickers or not weights or not return_goal:
        abort(404)

    weights = [float(weight) for weight in weights]
    return_goal = (1 + float(return_goal))**(1 / 52) - 1
    start_date = TODAY_DATETIME - relativedelta(years=5)
    curr_date = start_date
    prices_all = get_prices(start_date, TODAY_DATETIME, tickers)

    assert len(prices_all) == len(weights)

    # current and historical market cap,
    # assume the initial portfolio value is 1 dollar
    market_caps = []
    shares = [weights[j] / prices_all[j][0] for j in range(len(weights))]

    transaction_costs = []
    curr_transaction_cost = 0

    rebalance_interval = int(len(first_item_in_list(prices_all)) / 5)
    for i in range(len(first_item_in_list(prices_all))):

        market_cap = 0
        for j in range(len(tickers)):
            market_cap += prices_all[j][i] * shares[j]
        market_caps.append(market_cap)

        if rebalance_interval == 0:
            curr_date += relativedelta(years=1)
            rebalanced_weights = rebalance_portfolio(
                curr_date - relativedelta(years=1), curr_date, tickers, return_goal)

            assert len(prices_all) == len(rebalanced_weights)
            rebalanced_shares = [market_cap * rebalanced_weights[j] / prices_all[j][i]
                                 for j in range(len(rebalanced_weights))]

            rebalance_interval = int(len(first_item_in_list(prices_all)) / 5)
            curr_transaction_cost += 5 * calculate_transaction_costs(
                shares, rebalanced_shares, [prices[i] for prices in prices_all]
            )

            shares = rebalanced_shares
        else:
            rebalance_interval -= 1

        transaction_costs.append(curr_transaction_cost)

    return jsonify({
        'portfolio_value': market_caps,
        'transaction_costs': transaction_costs
    })


@bp.route('/back_test_user', methods=('GET',))
def back_test_user_portfolio():
    """
    m = # of data points (weekly)
    :return: m x 1 np array; back tested caps of the portfolio
    This will not perform rebalancing
    """
    # always backtest using 5 years of data
    user_id = float(request.args.get('user_id'))
    portfolio_id = get_portfolio_id(user_id)
    portfolio = get_portfolio(portfolio_id)
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


@bp.route('/back_test_portfolio', methods=('GET', ))
def back_test_portfolio():
    """
    m = # of data points (weekly)
    :return: m x 1 np array; back tested caps of the portfolio
    This will not perform rebalancing
    """
    weights = request.args.getlist('weights[]')
    tickers = request.args.getlist('tickers[]')

    if weights is None or tickers is None:
        abort(404)

    # always backtest using 5 years of data
    start_date = TODAY_DATETIME - relativedelta(years=5)
    prices_all = get_prices(start_date, TODAY_DATETIME, tickers)
    shares = [float(weights[j]) / prices_all[j][0] for j in range(len(weights))]

    assert len(prices_all) == len(tickers)
    assert len(prices_all) == len(shares)
    market_caps = []

    for i in range(len(first_item_in_list(prices_all))):
        market_cap = 0
        for j in range(len(prices_all)):
            market_cap += prices_all[j][i] * shares[j]
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
    mu_p, sd_p = p_metrics(portfolio, views * returns, cov)
    print(mu_p)
    print(returns)
    mu_p = (1 + mu_p)**52 - 1
    print(mu_p)
    sd_p *= math.pow(52, 0.5)
    yearly_rf = (1 + risk_free_rate)**52 - 1
    sharpe_p = (mu_p - yearly_rf) / sd_p
    monte_carlo_simulations = monte_carlo(mu_p, sd_p, 52, MONTE_CARLO_SIMULATIONS)
    var, cvar = var_calc(monte_carlo_simulations, 0.01)
    return jsonify(
        {
            'ticker': tickers,
            'weights': portfolio.tolist(),
            'return': mu_p,
            'sigma': sd_p,
            'sharpe_ratio': sharpe_p,
            'var': var,
            'cvar': cvar
        }
    )


@bp.route('/mvo', methods=('GET', ))
def get_mvo():
    mu_goal = request.args.get('mu_goal')
    cardinality = request.args.get('cardinality')
    if not mu_goal or not cardinality:
        abort(404)
    print(mu_goal)
    print(cardinality)
    mu_goal = (1 + float(mu_goal))**(1 / 52) - 1
    print(mu_goal)
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
    portfolio, port_var, port_ret = mvo(md_cov, md_mu, mu_goal)
    port_ret = (1 + port_ret)**52 - 1
    sigma = math.pow(52 * port_var, 0.5)
    yearly_rf = (1 + RISK_FREE[-1])**52 - 1
    sharpe_ratio = (port_ret - yearly_rf) / sigma
    # 1000 simulations with
    monte_carlo_simulations = monte_carlo(port_ret, sigma, 52, MONTE_CARLO_SIMULATIONS)
    var, cvar = var_calc(monte_carlo_simulations, 0.01)

    return jsonify({
        'tickers': md_tickers,
        'portfolio': portfolio.tolist(),
        'sigma': sigma,
        'sharpe_ratio': sharpe_ratio,
        'ret': port_ret,
        'var': var,
        'cvar': cvar
    })
