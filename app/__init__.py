import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app import db
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "My name Jeff"

    from app.views import auth
    app.register_blueprint(auth.bp)

    from app.views import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from app.views import api
    app.register_blueprint(api.bp)

    return app
