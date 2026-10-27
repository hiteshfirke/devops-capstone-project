"""Accounts service tests"""
import os
from unittest import TestCase

os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from service import create_app, db  # noqa: E402
from service.models import Account  # noqa: E402

BASE = "/accounts"
DATA = {"name": "Ada", "email": "ada@example.com", "address": "1 Main St", "phone_number": "555-0100"}


class TestAccountService(TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def _make(self):
        return self.client.post(BASE, json=DATA)

    def test_index(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_create_account(self):
        resp = self._make()
        self.assertEqual(resp.status_code, 201)
        self.assertIn("/accounts/", resp.headers["Location"])
        self.assertEqual(resp.get_json()["name"], "Ada")

    def test_create_bad_payload(self):
        self.assertEqual(self.client.post(BASE, json={"name": "x"}).status_code, 400)

    def test_list_accounts(self):
        self._make()
        self._make()
        self.assertEqual(len(self.client.get(BASE).get_json()), 2)

    def test_read_account(self):
        aid = self._make().get_json()["id"]
        self.assertEqual(self.client.get(f"{BASE}/{aid}").get_json()["email"], DATA["email"])

    def test_read_not_found(self):
        self.assertEqual(self.client.get(f"{BASE}/0").status_code, 404)

    def test_update_account(self):
        aid = self._make().get_json()["id"]
        resp = self.client.put(f"{BASE}/{aid}", json={**DATA, "name": "Grace"})
        self.assertEqual(resp.get_json()["name"], "Grace")

    def test_update_not_found(self):
        self.assertEqual(self.client.put(f"{BASE}/0", json=DATA).status_code, 404)

    def test_update_bad_payload(self):
        aid = self._make().get_json()["id"]
        self.assertEqual(self.client.put(f"{BASE}/{aid}", json={}).status_code, 400)

    def test_delete_account(self):
        aid = self._make().get_json()["id"]
        self.assertEqual(self.client.delete(f"{BASE}/{aid}").status_code, 204)
        self.assertIsNone(db.session.get(Account, aid))
        self.assertEqual(self.client.delete(f"{BASE}/{aid}").status_code, 204)

    def test_security_headers(self):
        headers = self.client.get("/").headers
        self.assertEqual(headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
        self.assertEqual(headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_cors_header(self):
        resp = self.client.get("/", headers={"Origin": "http://example.com"})
        self.assertIn(resp.headers["Access-Control-Allow-Origin"], ("*", "http://example.com"))
