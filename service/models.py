"""Account model"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when payload is invalid"""


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {"id": self.id, "name": self.name, "email": self.email,
                "address": self.address, "phone_number": self.phone_number}

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError(f"Invalid account: missing {error.args[0]}") from error
        except TypeError as error:
            raise DataValidationError("Invalid account: bad or missing data") from error
        return self

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        return db.session.get(cls, account_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name).all()
