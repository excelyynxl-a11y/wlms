import unittest 
from selenium import webdriver 
import json 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

class TestNavbarWeb(unittest.TestCase):

    def setUp(self):
        """
        Method to setup driver to access live server in Chrome.
        Prepare environment for each test.
        """
        self.driver = webdriver.Chrome() # launches a new Chrome crowser window
        self.driver.implicitly_wait(5) # wait up to 5s for elements to appear befroe throwing an error
        self.driver.get('http://127.0.0.1:5500/html/nav_bar.html') 

    def tearDown(self):
        """
        Method to teardown / end driver
        """
        try:
            self.driver.execute_script("localStorage.clear()")
            self.driver.delete_all_cookies()
        finally:
            self.driver.quit() # close entire window, end WebDriver session

    def test_page_title(self):
        expected_page_title =  "WLMS"
        self.assertIn(expected_page_title, self.driver.title)

    def test_register_button_exist(self):
        register_button = self.driver.find_element(By.XPATH, "//a[@href='#register']")
        self.assertIsNotNone(register_button)

    def test_display_bb_button_exist(self):
        display_bb_button = self.driver.find_element(By.XPATH, "//a[@href='#display_bb']")
        self.assertIsNotNone(display_bb_button)

    def test_view_button_exist(self):
        view_button = self.driver.find_element(By.XPATH, "//a[@href='#view']")
        self.assertIsNotNone(view_button)

    def test_quit_button_exist(self):
        quit_button = self.driver.find_element(By.XPATH, "//a[@href='#quit']")
        self.assertIsNotNone(quit_button)

    def test_content_container_exist(self):
        content_container = self.driver.find_element(By.ID, "content")
        self.assertIsNotNone(content_container)

    def test_popup_quit_confiramation_initially_hidden(self):
        self.assertFalse(self.driver.find_element(By.ID, "popupquitconfiramation").is_displayed())

    def wait_for_content_to_load(self, expected_h1):
        """
        Method to wait for content to load before checking the main content displayed html.
        Use the displayed dashboard "h1" as identifier.
        Wait up to 10s for web to load the content.
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h1[text()='{expected_h1}']"))
        )

    def test_click_register_button_direct_to_register_dashboard(self):
        self.driver.find_element(By.XPATH, "//a[@href='#register']").click()
        expected_h1 = "Register" 
        self.wait_for_content_to_load(expected_h1)
        actual_h1 = self.driver.find_element(By.XPATH, "//h1").text
        self.assertIn(actual_h1, expected_h1)

    def test_click_display_bb_button_direct_to_display_bb_dashboard(self):
        self.driver.find_element(By.XPATH, "//a[@href='#display_bb']").click()
        expected_h1 = "Barbell Setup Loader"
        self.wait_for_content_to_load(expected_h1)
        actual_h1 = self.driver.find_element(By.XPATH, "//h1").text 
        self.assertIn(actual_h1, expected_h1)

    def test_click_view_button_direct_to_view_dashboard(self):
        self.driver.find_element(By.XPATH, "//a[@href='#view']").click()
        expected_h1 = "Participants"
        self.wait_for_content_to_load(expected_h1) 
        actual_h1 = self.driver.find_element(By.XPATH, "//h1").text
        self.assertIn(actual_h1, expected_h1)

    def test_click_quit_button_popup_quitconfiramation_displayed(self):
        self.driver.find_element(By.XPATH, "//a[@href='#quit']").click()
        self.assertTrue(self.driver.find_element(By.ID, "popupquitconfiramation").is_displayed())

    def test_click_yes_popup_quitconfiramation_web_closes(self):
        self.driver.find_element(By.XPATH, "//a[@href='#quit']").click()
        # wait for "are you sure you want to quit this session" popup to appear
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "popupquitconfiramation"))
        )
        self.driver.find_element(By.ID, "quit-session-btn").click()
        expected_about_blank_url = "about:blank"
        actual_url = self.driver.current_url
        self.assertEqual(expected_about_blank_url, actual_url)

    def test_click_no_popup_quitconfiramation_popup_closes(self): 
        self.driver.find_element(By.XPATH, "//a[@href='#quit']").click()
        # wait for "are you sure you want to quit this session" popup to appear
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "popupquitconfiramation"))
        )
        self.driver.find_element(By.ID, "stay-session-btn").click()
        self.assertFalse(self.driver.find_element(By.ID, "popupquitconfiramation").is_displayed())





# type into terminal:
# python -m unittest tests.test_navbar_web -v 