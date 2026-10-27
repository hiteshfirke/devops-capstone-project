"""Account model"""
from service import db


class DataValidationError(Exception):
    """Raised when payload is invalid"""


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))

    def serialize(self):
        return {"id": self.id, "name": self.name, "email": self.email,
                "address": self.address, "phone_number": self.phone_number}

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except (KeyError, TypeError) as err:
            raise DataValidationError(f"Invalid account: {err}") from err
        return self
