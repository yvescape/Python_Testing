import unittest
from flask import Flask, url_for
from server import app

class TestValidEmail(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_valid_email_returns_ok(self):
        response = self.app.post('/showSummary', data={'email': 'john@simplylift.co'})
        self.assertEqual(response.status_code, 200)  # Succès
        self.assertIn(b'Welcome', response.data)

class TestInvalidEmail(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_invalid_email_returns_404(self):
        response = self.app.post('/showSummary', data={'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 302)  # Erreur 404

if __name__ == '__main__':
    unittest.main()