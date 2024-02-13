import unittest
from flask import Flask, render_template, redirect, url_for, flash
from server import app  # Assurez-vous d'importer correctement votre application Flask et ses dépendances
from datetime import datetime

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_some_other_route_valid(self):
        # Cas où l'e-mail du club existe dans le système
        club_email = "john@simplylift.co"  # Remplacez par un e-mail existant dans votre système
        response = self.app.get(f'/some_other_route/{club_email}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Assurez-vous que la redirection fonctionne correctement
        # Assurez-vous que le contenu du club est présent dans la page rendue
        # Ajoutez d'autres assertions si nécessaire

    def test_some_other_route_invalid_email(self):
        # Cas où l'e-mail du club n'existe pas dans le système
        club_email = "nonexistent@example.com"  # Remplacez par un e-mail non existant dans votre système
        response = self.app.get(f'/some_other_route/{club_email}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Assurez-vous que la redirection fonctionne correctement
        # Assurez-vous que la redirection vers l'index est effectuée
if __name__ == '__main__':
    unittest.main()
