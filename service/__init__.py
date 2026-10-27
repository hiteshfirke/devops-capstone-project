"""Accounts service: Flask app with Talisman security headers and CORS"""
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from service import config
from service.models import db

app = Flask(__name__)
app.config.from_object(config)

# Security headers (CSP, X-Frame-Options, ...) and CORS policies
talisman = Talisman(app, force_https=False)
CORS(app)

db.init_app(app)

# routes must be imported after the app is created
from service import routes  # noqa: E402,F401  pylint: disable=wrong-import-position,cyclic-import

with app.app_context():
    db.create_all()
