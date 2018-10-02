"""
import pytest

import sys
sys.path.append("../")

from flask import Flask, url_for
from flask_testing import TestCase
from selenium import webdriver

from grandpy import app

class TestUserTakesTheTest(TestCase):
    def create_app(self):
        # Fichier de config uniquement pour les tests.
        return app

    # Méthode exécutée avant chaque test
    def setUp(self):
        # Le navigateur est Firefox
        chromeOptions = webdriver.ChromeOptions()
        userProfile = "C:/Users/Flokami/AppData/Local/Google/Chrome/AutomationProfile"
        chromeOptions.add_argument("user-data-dir="+userProfile)
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument("test-type");
        self.driver = webdriver.Chrome(executable_path="D:/ChromeDriver/chromedriver.exe",options=chromeOptions)

    def test_views_adress(self):
    	with app.test_request_context():
    		assert url_for('index') == "/"

    def test_views_return(self):
    	self.driver.get('http://localhost:5000/')
    	assert self.driver.title == "GrandPy Bot"

    # Méthode exécutée après chaque test
    def tearDown(self):
        self.driver.quit()


"""

