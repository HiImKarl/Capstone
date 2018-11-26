from flask import (
    Blueprint, flash, g, session, url_for, jsonify
)
from app.db import get_db
from app.data import STOCK_TICKERS

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/assets', methods=('GET', ))
def assets():
    prices = []
    db = get_db()
    for TICKER in STOCK_TICKERS:
        price = db.execute(
            'SELECT price FROM Asset WHERE ticker = ?', (TICKER, )
        ).fetchone()
        prices.append(price['price'])

    return jsonify(
        tickers=STOCK_TICKERS,
        prices=prices
    )
