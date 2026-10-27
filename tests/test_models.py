"""Test Cases for Account Model"""
import os
from unittest import TestCase

os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from service import app  # noqa: E402
from service.models import Account, DataValidationError, db  # noqa: E402

DATA = {"name": "Ada", "email": "ada@example.com", "address": "1 Main St", "phone_number": "555-0100"}


class TestAccountModel(TestCase):
    """Test Cases for Account Model"""

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_create_an_account(self):
        """It should Create an account and add it to the database"""
        account = Account().deserialize(DATA)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_create_an_account_exists(self):
        """It should Create an Account and assert that it exists"""
        account = Account().deserialize(DATA)
        account.create()
        self.assertIsNotNone(account.id)

    def test_delete_an_account(self):
        """It should Delete an account from the database"""
        account = Account().deserialize(DATA)
        account.create()
        account.delete()
        self.assertEqual(Account.all(), [])

    def test_deserialize_an_account(self):
        """It should Deserialize an account"""
        account = Account().deserialize(DATA)
        self.assertEqual(account.name, "Ada")

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an account with a KeyError"""
        self.assertRaises(DataValidationError, Account().deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an account with a TypeError"""
        self.assertRaises(DataValidationError, Account().deserialize, [])

    def test_find_by_name(self):
        """It should Find an Account by name"""
        Account().deserialize(DATA).create()
        self.assertEqual(Account.find_by_name("Ada")[0].email, DATA["email"])

    def test_list_all_accounts(self):
        """It should List all Accounts in the database"""
        Account().deserialize(DATA).create()
        Account().deserialize(DATA).create()
        self.assertEqual(len(Account.all()), 2)

    def test_read_an_account(self):
        """It should Read an account"""
        account = Account().deserialize(DATA)
        account.create()
        self.assertEqual(Account.find(account.id).name, "Ada")

    def test_serialize_an_account(self):
        """It should Serialize an account"""
        account = Account().deserialize(DATA)
        self.assertEqual(account.serialize()["email"], DATA["email"])

    def test_update_an_account(self):
        """It should Update an account"""
        account = Account().deserialize(DATA)
        account.create()
        account.name = "Grace"
        account.update()
        self.assertEqual(Account.find(account.id).name, "Grace")

    def test_update_no_id(self):
        """It should not Update an account with no id"""
        self.assertRaises(DataValidationError, Account().deserialize(DATA).update)
