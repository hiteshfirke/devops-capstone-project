"""Accounts service: Flask app factory with Talisman security headers and CORS"""
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
talisman = Talisman()


def create_app():
    app = Flask(__name__)
    app.config.from_object("service.config")

    db.init_app(app)
    talisman.init_app(app, force_https=False)
    CORS(app)

    with app.app_context():
        from service import routes  # noqa: F401  pylint: disable=import-outside-toplevel
        app.register_blueprint(routes.bp)
        db.create_all()
    return app
