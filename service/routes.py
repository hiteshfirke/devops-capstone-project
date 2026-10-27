"""Accounts REST routes"""
from flask import Blueprint, jsonify, request
from service import db
from service.models import Account, DataValidationError

bp = Blueprint("accounts", __name__)


@bp.route("/")
def index():
    return jsonify(name="Account REST API Service", version="1.0"), 200


@bp.route("/accounts", methods=["POST"])
def create_account():
    try:
        account = Account().deserialize(request.get_json(silent=True))
    except DataValidationError as err:
        return jsonify(error=str(err)), 400
    db.session.add(account)
    db.session.commit()
    return jsonify(account.serialize()), 201, {"Location": f"/accounts/{account.id}"}


@bp.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify([a.serialize() for a in Account.query.all()]), 200


@bp.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = db.session.get(Account, account_id)
    if not account:
        return jsonify(error=f"Account {account_id} not found"), 404
    return jsonify(account.serialize()), 200


@bp.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = db.session.get(Account, account_id)
    if not account:
        return jsonify(error=f"Account {account_id} not found"), 404
    try:
        account.deserialize(request.get_json(silent=True))
    except DataValidationError as err:
        return jsonify(error=str(err)), 400
    db.session.commit()
    return jsonify(account.serialize()), 200


@bp.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = db.session.get(Account, account_id)
    if account:
        db.session.delete(account)
        db.session.commit()
    return "", 204
