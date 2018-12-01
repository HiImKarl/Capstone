from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db, get_prices
from app.views.auth import login_required
from app.data import STOCK_TICKERS, TODAY_DATETIME
bp = Blueprint('index', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index/index.jinja2')


@bp.route('/back_testing')
@login_required
def back_testing():
    return render_template('index/back_testing.jinja2')


@bp.route('/tutorial')
@login_required
def tutorial():
    return render_template('index/tutorial.jinja2')


@bp.route('/about')
@login_required
def about():
    return render_template('index/about.jinja2')


@bp.route('/preferences', methods=('GET', 'POST'))
@login_required
def preferences():
    return render_template('index/preferences.jinja2')


@bp.route('/set_portfolio', methods=('GET', 'POST'))
@login_required
def set_portfolio():
    if request.method == 'POST':
        portfolio = request.json['how_many']
        views = request.json['views']
        print(portfolio)
        db = get_db()

        # FIXME limiting to one portfolio
        # remove previous portfolios
        # we are only considering one portfolio

        portfolio_ids = db.execute(
            'SELECT portfolio_id FROM Portfolio WHERE user_id = ?',
            (g.user['user_id'], )
        ).fetchall()

        for row in portfolio_ids:
            print(row['portfolio_id'])
            db.execute(
                'DELETE FROM PortfolioAsset WHERE portfolio_id = ?',
                (row['portfolio_id'], )
            )

        db.execute(
            'DELETE FROM Portfolio WHERE user_id = ?',
            (g.user['user_id'], )
        )

        # Insert the new portfolio into the database
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO Portfolio (user_id) VALUES (?)', (g.user['user_id'], )
        )

        portfolio_id = cursor.lastrowid
        for ticker in portfolio.keys():
            # FIXME this should realistically never happen
            # with frontend validation
            amount = portfolio[ticker]

            if amount == 0 or amount is None:
                continue

            db.execute(
                'INSERT INTO PortfolioAsset (portfolio_id, ticker, amount, views)'
                'VALUES (?, ?, ?, ?)',
                (portfolio_id, ticker, portfolio[ticker], views[ticker])
            )

        db.commit()
        flash("Successfully Submitted Portfolio")

    return render_template('index/set_portfolio.jinja2')


@bp.route('/generate_better', methods=('GET', 'POST'))
@login_required
def generate_better():
    return render_template('index/generate_better.jinja2')


@bp.route('/generate_target', methods=('GET', 'POST'))
@login_required
def generate_target():
    return render_template('index/generate_target.jinja2')


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

