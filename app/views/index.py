from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db
from app.views.auth import login_required
from app.data import STOCK_TICKERS

bp = Blueprint('index', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index/index.jinja2')


@bp.route('/backtesting')
@login_required
def backtesting():
    return render_template('index/backtesting.jinja2')


@bp.route('/tutorial')
@login_required
def tutorial():
    return render_template('index/tutorial.jinja2')


@bp.route('/preferences', methods=('GET', 'POST'))
@login_required
def preferences():
    return render_template('index/preferences.jinja2')


@bp.route('/set_portfolio', methods=('GET', 'POST'))
@login_required
def set_portfolio():
    if request.method == 'POST':
        portfolio = request.json
        print(portfolio)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO Portfolio (user_id) VALUES (?)', (g.user['user_id'], )
        )

        portfolio_id = cursor.lastrowid

        for ticker, amount in portfolio.items():
            if amount == 0:
                continue

            db.execute(
                'INSERT INTO PortfolioAsset (portfolio_id, ticker, amount)'
                'VALUES (?, ?, ?)',
                (portfolio_id, ticker, amount, )
            )

        db.commit()

    return render_template('index/set_portfolio.jinja2')


@bp.route('/generate_better', methods=('GET', 'POST'))
@login_required
def generate_better():
    return render_template('index/generate_better.jinja2')


@bp.before_request
def load_stocks():
    session['tickers'] = STOCK_TICKERS
    prices = []
    db = get_db()
    for TICKER in STOCK_TICKERS:
        price = db.execute(
            'SELECT price FROM Asset WHERE ticker = ?', (TICKER, )
        ).fetchone()
        prices.append(price['price'])
    session['prices'] = prices

