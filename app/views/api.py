import numpy as np
from flask import (
    Blueprint, abort, request, jsonify, render_template
)
from app.db import get_db
from app.data import TICKERS
from business_logic.md_mvo import cov_to_cor, md_mvo

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


# FIXME SECURITY ISSUE
@bp.route('/correlations', methods=('GET',))
def correlations():
    cov_matrix = np.zeros((len(TICKERS), len(TICKERS)), dtype=np.float64)
    db = get_db()
    cov_data = db.execute('SELECT * FROM Covariance').fetchall()
    cov_dict = {}
    for TICKER in TICKERS:
        cov_dict[TICKER] = {}

    for row in cov_data:
        cov_dict[row['ticker1']][row['ticker2']] = row['covariance']

    for i in range(len(TICKERS)):
        for j in range(len(TICKERS)):
            cov_matrix[i][j] = cov_dict[TICKERS[i]][TICKERS[j]]

    cor_matrix = cov_to_cor(cov_matrix)
    return jsonify(
        md_mvo(cor_matrix, 20)
    )


