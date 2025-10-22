import unittest 
from selenium import webdriver 
import json # read localStorage
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class TestEditParticipantWeb(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.get()

    def tearDown(self):
        try:
            self.driver.execute_script("localStorage.clear()")
            self.driver.delete_all_cookies()
        finally:
            self.driver.quit()

    def test_page_title(self):
        expected_page_title = "Participants"
        self.assertIn(expected_page_title, self.driver.title) 

