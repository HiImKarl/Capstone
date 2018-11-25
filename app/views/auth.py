import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db
from app.forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        error = None
        db = get_db()

        if db.execute(
            'SELECT * FROM User WHERE username = ?', (username, )
        ).fetchone() is not None:
            error = 'User is already registered!'

        if error is None:
            db.execute(
                'INSERT INTO User (username, password, risk_profile) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), None,)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.jinja2', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        error = None
        db = get_db()

        user = db.execute(
            'SELECT * FROM User WHERE username = ?', (username, )
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = "Incorrect Username or Password."

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            flash("Successfully logged in!")
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.jinja2', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is not None:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM User WHERE user_id = ?', (user_id, )
        ).fetchone()
    else:
        g.user = None


@bp.route('logout', methods=('GET', ))
def logout():
    session.clear()
    logout_message = "Successfully logged out!"
    flash(logout_message)
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
