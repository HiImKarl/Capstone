import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from app.views.auth import login_required

bp = Blueprint('index', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index/index.jinja2')


@bp.route('/reports')
@login_required
def reports():
    return render_template('index/reports.jinja2')


@bp.route('/preferences', methods=('GET', 'POST'))
@login_required
def preferences():
    return render_template('index/preferences.jinja2')


@bp.route('/portfolios', methods=('GET', 'POST'))
@login_required
def portfolios():
    return render_template('index/portfolios.jinja2')
