import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
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

@bp.route('/preferences', methods=('GET', 'POST'))
@login_required
def preferences():
    return render_template('index/preferences.jinja2')

@bp.route('/portfolios', methods=('GET', 'POST'))
@login_required
def portfolios():
    return render_template('index/portfolios.jinja2')

@bp.before_request
def load_stock_tickers():
    session['tickers'] = STOCK_TICKERS