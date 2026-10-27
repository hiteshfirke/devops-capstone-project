"""Account Service Tests"""
import os
from unittest import TestCase

os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from service import app  # noqa: E402
from service.models import Account, db  # noqa: E402

BASE = "/accounts"
DATA = {"name": "Ada", "email": "ada@example.com", "address": "1 Main St", "phone_number": "555-0100"}


class TestAccountService(TestCase):
    """Account Service Tests"""

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def _make(self):
        return self.client.post(BASE, json=DATA)

    def test_create_bad_data(self):
        """It should not Create an Account when sending the wrong data"""
        self.assertEqual(self.client.post(BASE, json={"name": "x"}).status_code, 400)

    def test_cors_security(self):
        """It should return a CORS header"""
        resp = self.client.get("/", headers={"Origin": "http://example.com"})
        self.assertIn(resp.headers["Access-Control-Allow-Origin"], ("*", "http://example.com"))

    def test_create_account(self):
        """It should Create a new Account"""
        resp = self._make()
        self.assertEqual(resp.status_code, 201)
        self.assertIn("/accounts/", resp.headers["Location"])

    def test_delete_account(self):
        """It should Delete an Account"""
        aid = self._make().get_json()["id"]
        self.assertEqual(self.client.delete(f"{BASE}/{aid}").status_code, 204)
        self.assertIsNone(Account.find(aid))

    def test_delete_account_by_email(self):
        """It should Delete an Account matching the e-mail in the request body"""
        self._make()
        self.assertEqual(self.client.delete(BASE, json=DATA).status_code, 204)
        self.assertEqual(Account.all(), [])

    def test_read_account(self):
        """It should Read a single Account"""
        aid = self._make().get_json()["id"]
        self.assertEqual(self.client.get(f"{BASE}/{aid}").get_json()["email"], DATA["email"])

    def test_list_accounts(self):
        """It should Get a list of Accounts"""
        self._make()
        self._make()
        self.assertEqual(len(self.client.get(BASE).get_json()), 2)

    def test_read_account_not_found(self):
        """It should not Read an Account that is not found"""
        self.assertEqual(self.client.get(f"{BASE}/0").status_code, 404)

    def test_health(self):
        """It should be healthy"""
        self.assertEqual(self.client.get("/health").get_json()["status"], "OK")

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        self.assertEqual(self.client.put(BASE, json=DATA).status_code, 405)

    def test_security_headers(self):
        """It should return security headers"""
        headers = self.client.get("/").headers
        self.assertEqual(headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
        self.assertEqual(headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_create_wrong_media_type(self):
        """It should not Create an Account when sending the wrong media type"""
        resp = self.client.post(BASE, data="x", headers={"Content-Type": "text/plain"})
        self.assertEqual(resp.status_code, 415)

    def test_update_account(self):
        """It should Update an existing Account"""
        aid = self._make().get_json()["id"]
        resp = self.client.put(f"{BASE}/{aid}", json={**DATA, "name": "Grace"})
        self.assertEqual(resp.get_json()["name"], "Grace")

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        self.assertEqual(self.client.put(f"{BASE}/0", json=DATA).status_code, 404)
