"""Accounts REST routes"""
from flask import jsonify, request
from service import app
from service.models import Account, DataValidationError


def check_content_type(media_type):
    if request.headers.get("Content-Type", "").split(";")[0] != media_type:
        return jsonify(error=f"Content-Type must be {media_type}"), 415
    return None


@app.route("/health")
def health():
    return jsonify(status="OK"), 200


@app.route("/")
def index():
    return jsonify(name="Account REST API Service", version="1.0"), 200


@app.route("/accounts", methods=["POST"])
def create_account():
    bad_type = check_content_type("application/json")
    if bad_type:
        return bad_type
    try:
        account = Account().deserialize(request.get_json(silent=True))
    except DataValidationError as err:
        return jsonify(error=str(err)), 400
    account.create()
    return jsonify(account.serialize()), 201, {"Location": f"/accounts/{account.id}"}


@app.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify([a.serialize() for a in Account.all()]), 200


@app.route("/accounts", methods=["DELETE"])
def delete_matching_accounts():
    """Delete the account(s) matching the e-mail in the JSON body"""
    bad_type = check_content_type("application/json")
    if bad_type:
        return bad_type
    email = (request.get_json(silent=True) or {}).get("email")
    if not email:
        return jsonify(error="email is required"), 400
    for account in Account.query.filter(Account.email == email).all():
        account.delete()
    return "", 204


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify(error=f"Account {account_id} not found"), 404
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = Account.find(account_id)
    if not account:
        return jsonify(error=f"Account {account_id} not found"), 404
    bad_type = check_content_type("application/json")
    if bad_type:
        return bad_type
    try:
        account.deserialize(request.get_json(silent=True))
    except DataValidationError as err:
        return jsonify(error=str(err)), 400
    account.update()
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify(error="Method not allowed"), 405
