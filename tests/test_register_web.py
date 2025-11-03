import unittest 
from selenium import webdriver 
import json # read localStorage
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

class TestRegisterWeb(unittest.TestCase):

    def setUp(self):
        """
        Method to setup driver to access live server in Chrome.
        Prepare environment for each test.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless") # run Chrome without the popup UI
        chrome_options.add_argument("--no-sandbox") # required for Linux CI
        chrome_options.add_argument("--disable-dev-shm-usage") # prevent resource issues
        chrome_options.add_argument("--window-size=1920,1080") # ensure elements to be clicked are all within window

        self.driver = webdriver.Chrome(options=chrome_options) # launches a new Chrome browser window
        self.driver.implicitly_wait(5) # wait up to 5s for elements to appear befroe throwing an error
        self.driver.get('http://127.0.0.1:5502/D1_WeightliftingManagementSystem/html/homepage.html') # homepage is the single entry point of the WLMS 
        self.driver.find_element(By.XPATH, "//a[@href='#register']").click()

    def tearDown(self):
        """
        Method to teardown / end driver
        """
        try:
            self.driver.execute_script("localStorage.clear()")
            self.driver.delete_all_cookies()
        finally:
            self.driver.quit() # close entire window, end WebDriver session

    def test_name_input_exist(self):
        """
        TC11.1: check existance of name input  
        """
        name_input = self.driver.find_element(By.ID, "participant-name")
        self.assertIsNotNone(name_input) 

    def test_age_input_exist(self):
        """
        TC11.2: check existance of age input  
        """
        age_input = self.driver.find_element(By.ID, "participant-age") 
        self.assertIsNotNone(age_input)

    def test_gender_input_exist(self):
        """
        TC11.3: check existance of gender input  
        """
        gender_input = self.driver.find_element(By.ID, "participant-gender") 
        self.assertIsNotNone(gender_input)

    def test_only_female_and_male_gender_option_exist(self):
        """
        TC11.4: check existance of female and male gender option only 
        """
        gender_input_select = Select(self.driver.find_element(By.ID, "participant-gender") )
        option_values = [option.get_attribute("value") for option in gender_input_select.options if option.get_attribute("value")]
        expected_values = ["FEMALE", "MALE"]
        self.assertCountEqual(option_values, expected_values)

    def test_weight_input_exist(self):
        """
        TC11.5: check existance of weight input  
        """
        weight_input = self.driver.find_element(By.ID, "participant-weight") 
        self.assertIsNotNone(weight_input)

    def test_register_button_exist(self):
        """
        TC11.6: check exitance of "register" button  
        """
        register_button = self.driver.find_element(By.ID, "register-btn") 
        self.assertIsNotNone(register_button)

    def templete_fill_form_and_submit(self, name, age, gender, weight):
        """
        Helper method. 
        Templete for submitting a form by clicking the "Register" button.
        """
        driver = self.driver 

        driver.find_element(By.ID, "participant-name").clear()
        driver.find_element(By.ID, "participant-name").send_keys(name)

        driver.find_element(By.ID, "participant-age").clear()
        driver.find_element(By.ID, "participant-age").send_keys(str(age))
        
        select = Select(driver.find_element(By.ID, "participant-gender"))
        select.select_by_value(gender)

        driver.find_element(By.ID, "participant-weight").clear()
        driver.find_element(By.ID, "participant-weight").send_keys(str(weight))

        driver.find_element(By.ID, "register-btn").click()

    def get_localStorage(self):
        """
        Helper method.
        Method to open local storage so that validation of data storing can be done.
        """
        data = self.driver.execute_script("return localStorage.getItem('participants')")
        return json.loads(data) if data else None 
    
    def test_click_enter(self):
        """
        TC11.7: Test all valid participant input (name = Kelly, age = 30, gender = FEMALE, weight 50) can be stored in localStorage
        upon clicking "enter" instead of clicking button
        """
        name = "Kelly"
        age =  30
        gender = "FEMALE"
        weight = 50

        driver = self.driver 

        driver.find_element(By.ID, "participant-name").clear()
        driver.find_element(By.ID, "participant-name").send_keys(name)

        driver.find_element(By.ID, "participant-age").clear()
        driver.find_element(By.ID, "participant-age").send_keys(str(age))
        
        select = Select(driver.find_element(By.ID, "participant-gender"))
        select.select_by_value(gender)

        driver.find_element(By.ID, "participant-weight").clear()
        driver.find_element(By.ID, "participant-weight").send_keys(str(weight))

        driver.find_element(By.ID, "participant-weight").send_keys(Keys.ENTER)

        storage = self.get_localStorage()
        self.assertIsNotNone(storage)
        self.assertTrue(any(p["name"] == name for p in storage))

    def test_all_valid_input_can_register_and_stored(self):
        """
        TC11.8: Test all valid participant input (name = Kelly, age = 30, gender = FEMALE, weight 50) can be stored in localStorage
        """
        name = "Kelly"
        age =  30
        gender = "FEMALE"
        weight = 50
        self.templete_fill_form_and_submit(name, age, gender, weight)
        storage = self.get_localStorage()
        self.assertIsNotNone(storage)
        self.assertTrue(any(p["name"] == name for p in storage))

    def test_empty_name_input_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.9: Test name input left empty, participant cannot be stored in localStorage and trigger alert
        """
        name = ""
        age =  "50"
        gender = "FEMALE"
        weight = "50"

        self.driver.execute_script("window.alert = function(msg){ window.lastAlert = msg; };")
        self.templete_fill_form_and_submit(name, age, gender, weight)

        actual_alert_message = self.driver.execute_script("return window.lastAlert;")
        expected_alert_message = "Please fill in all fields with correct value"
        self.assertEqual(actual_alert_message, expected_alert_message)

        storage = self.get_localStorage()
        self.assertIsNone(storage)

    def test_empty_age_input_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.10: Test age input left empty, participant cannot be stored in localStorage and trigger alert
        """
        name = "Kelly"
        age =  ""
        gender = "FEMALE"
        weight = 50

        self.driver.execute_script("window.alert = function(msg){ window.lastAlert = msg; };")
        self.templete_fill_form_and_submit(name, age, gender, weight)

        actual_alert_message = self.driver.execute_script("return window.lastAlert;")
        expected_alert_message = "Please fill in all fields with correct value"
        self.assertEqual(actual_alert_message, expected_alert_message)

        storage = self.get_localStorage()
        self.assertIsNone(storage)

    def test_empty_gender_input_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.11: Test gender input left empty, participant cannot be stored in localStorage and trigger alert
        """
        name = "Kelly"
        age =  "50"
        gender = ""
        weight = 50

        self.driver.execute_script("window.alert = function(msg){window.lastAlert = msg;}")
        self.templete_fill_form_and_submit(name, age, gender, weight)
        
        actual_alert_message = self.driver.execute_script("return window.lastAlert;")
        expected_alert_message = "Please fill in all fields with correct value"
        self.assertEqual(actual_alert_message, expected_alert_message)

        storage = self.get_localStorage()
        self.assertIsNone(storage)

    def test_empty_weight_input_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.12: Test weight input left empty, participant cannot be stored in localStorage and trigger alert
        """
        name = "Kelly"
        age =  "50"
        gender = "FEMALE"
        weight = ""

        self.driver.execute_script("window.alert = function(msg){window.lastAlert = msg;}")
        self.templete_fill_form_and_submit(name, age, gender, weight)

        actual_error_message = self.driver.execute_script("return window.lastAlert;") 
        expected_alert_message = "Please fill in all fields with correct value"
        self.assertEqual(actual_error_message, expected_alert_message)
        storage = self.get_localStorage()
        self.assertIsNone(storage)


    def test_age_11_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.13: Test participant age = 11 cannot be stored in localStorage and trigger alert
        """
        name = "Kelly"
        age =  11
        gender = "FEMALE"
        weight = 50

        self.driver.execute_script("window.alert = function(msg){ window.lastAlert = msg; };")
        self.templete_fill_form_and_submit(name, age, gender, weight)

        expected_alert_message = "Please fill in all fields with correct value"
        actual_alert_message = self.driver.execute_script("return window.lastAlert;")
        self.assertEqual(actual_alert_message, expected_alert_message)

        storage = self.get_localStorage()
        self.assertIsNone(storage)

    def test_age_12_can_register_and_stored(self):
        """
        TC11.14: Test valid participant age = 12 can be stored in localStorage 
        """
        name = "Kelly"
        age =  12
        gender = "FEMALE"
        weight = 50

        storage = self.get_localStorage()
        self.templete_fill_form_and_submit(name, age, gender, weight)
        storage = self.get_localStorage()
        self.assertIsNotNone(storage)
        self.assertTrue(any(p["name"] == name for p in storage)) 

    def test_age_13_can_register_and_stored(self):
        """
        TC11.15: Test valid participant age = 13 can be stored in localStorage 
        """
        name = "Kelly"
        age =  13
        gender = "FEMALE"
        weight = 50

        storage = self.get_localStorage()
        self.templete_fill_form_and_submit(name, age, gender, weight)
        storage = self.get_localStorage()
        self.assertIsNotNone(storage)
        self.assertTrue(any(p["name"] == name for p in storage)) 

    def test_negative_weight_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.15: Test participant weight = 0kg cannot be stored in localStorage and trigger alert
        """
        name = "Kelly"
        age =  50
        gender = "FEMALE"
        weight = -1

        self.driver.execute_script("window.alert = function(msg){ window.lastAlert = msg; };")
        self.templete_fill_form_and_submit(name, age, gender, weight)

        expected_alert_message = "Please fill in all fields with correct value"
        actual_alert_message = self.driver.execute_script("return window.lastAlert;")
        self.assertEqual(actual_alert_message, expected_alert_message)

        storage = self.get_localStorage()
        self.assertIsNone(storage)
    
    def test_weight_0kg_cannot_register_not_stored_trigger_alert(self):
        """
        TC11.16: Test participant weight = 0kg cannot be stored in localStorage and trigger alert
        """
        name = "Kelly"
        age =  50
        gender = "FEMALE"
        weight = 0

        self.driver.execute_script("window.alert = function(msg){ window.lastAlert = msg; };")
        self.templete_fill_form_and_submit(name, age, gender, weight)

        expected_alert_message = "Please fill in all fields with correct value"
        actual_alert_message = self.driver.execute_script("return window.lastAlert;")
        self.assertEqual(actual_alert_message, expected_alert_message)

        storage = self.get_localStorage()
        self.assertIsNone(storage)

    def test_weight_1kg_can_register_and_stored(self):
        """
        TC11.17: Test participant weight = 1kg can be stored in localStorage 
        """
        name = "Kelly"
        age =  50
        gender = "FEMALE"
        weight = 1

        storage = self.get_localStorage()
        self.templete_fill_form_and_submit(name, age, gender, weight)
        storage = self.get_localStorage()
        self.assertIsNotNone(storage)
        self.assertTrue(any(p["name"] == name for p in storage)) 




# type into terminal:
# python -m unittest tests.test_register_web -v 


