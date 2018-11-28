from flask import (
    Blueprint, flash, g, session, url_for, request, jsonify
)
from app.db import get_db
from app.data import STOCK_TICKERS, ETF_TICKERS

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/assets', methods=('GET', ))
def assets():
    prices = []
    db = get_db()
    tickers = STOCK_TICKERS + ETF_TICKERS
    for ticker in tickers:
        price = db.execute(
            'SELECT price FROM Asset WHERE ticker = ?', (ticker, )
        ).fetchone()
        prices.append(price['price'])

    return jsonify(
        tickers=tickers,
        prices=prices
    )


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
