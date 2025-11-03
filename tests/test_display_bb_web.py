import unittest 
from selenium import webdriver 
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys

class TestBarbellSetupWeb(unittest.TestCase):

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
        self.driver.find_element(By.XPATH, "//a[@href='#display_bb']").click()

    def tearDown(self):
        """
        Method to teardown / end driver
        """
        self.driver.quit() # close entire window, end WebDriver session

    def test_gender_input_exist(self):
        """
        TC10.1: check exitance of gender input dropdown 
        """
        gender_dropdown_input = self.driver.find_element(By.ID, "gender")
        self.assertIsNotNone(gender_dropdown_input)

    def test_only_female_and_male_gender_option_exist(self):
        """
        TC10.2: check existance of female and male gender option only 
        """
        gender_input_select = Select(self.driver.find_element(By.ID, "gender") )
        option_values = [option.get_attribute("value") for option in gender_input_select.options if option.get_attribute("value")]
        expected_values = ["FEMALE", "MALE"]
        self.assertCountEqual(option_values, expected_values) 

    def test_attempt_weight_input_exist(self):
        """
        TC10.3: check exitance of attempt weight input  
        """
        attempt_weight_input = self.driver.find_element(By.ID, "weight") 
        self.assertIsNotNone(attempt_weight_input)

    def test_load_barbell_button_exist(self):
        """
        TC10.4: check exitance of "load barbell" button  
        """
        load_barbell_button = self.driver.find_element(By.ID, "load-barbell-btn") 
        self.assertIsNotNone(load_barbell_button)

    def test_error_message_exist(self):
        """
        TC10.5: check for container to display error message
        """
        error_message = self.driver.find_element(By.ID, "error-message")
        self.assertIsNotNone(error_message) 

    def test_barbell_display_exist(self):
        """
        TC10.6: check exitance container for barbell-display
        """
        barbell_display_div = self.driver.find_element(By.ID, "barbell-display")
        self.assertIsNotNone(barbell_display_div) 

    def test_weight_info_exist(self):
        """
        TC10.7: check exitance container for attempt weight display
        """
        weight_info = self.driver.find_element(By.ID, "weight-info")
        self.assertIsNotNone(weight_info)

    def test_click_enter(self):
        """
        TC10.8: check if user hit "enter" on keyboard, it is similar as manully clicking the "Load barbell setup" button.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("20")
        self.driver.find_element(By.ID, "weight").send_keys(Keys.ENTER)

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment bar",
            "equipment clip"
        ]

        self.assertEqual(classes, expected)

    def test_initial_error_message_hidden(self):
        """
        TC10.9: check initially error message is hidden
        """
        self.assertFalse(self.driver.find_element(By.ID, "error-message").is_displayed())


    def test_female_19kg_order_display_error_message(self):
        """
        TC10.10: check if user enter invalid input weight (gender = FEMALE, attempt-weight = 19kg), 
        the container for error message will appear to display error message
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("19")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        self.assertTrue(self.driver.find_element(By.ID, "error-message").is_displayed())

    def test_female_20kg_order(self):
        """
        TC10.11: test barbell is displayed in correct order of:
        clip > barbell > clip
        when input is female lifting 20kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("20")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment bar",
            "equipment clip"
        ]

        self.assertEqual(classes, expected)

    def test_female_21kg_order(self):
        """
        TC10.12: test barbell is displayed in correct order of:
        clip > small white plate > barbell> small white plate  > clip
        when input is female lifting 21kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("21")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-white-plate",
            "equipment bar",
            "equipment small-white-plate",
            "equipment clip"
        ]

        self.assertEqual(classes, expected)

    def test_female_54kg_order(self):
        """
        TC10.13: test barbell is displayed in correct order of:
        clip > small blue plate > yellow plate > barbell > yellow plate > small blue plate  > clip
        when input is female lifting 54kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("54")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-blue-plate",
            "equipment yellow-plate",
            "equipment bar",
            "equipment yellow-plate",
            "equipment small-blue-plate",
            "equipment clip"
        ]

        self.assertEqual(classes, expected)

    def test_female_63kg_order(self):
        """
        TC10.14: test barbell is displayed in correct order of:
        clip > small yellow plate > blue plate > barbell > blue plate > small yellow plate  > clip
        when input is female lifting 63kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("63")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-yellow-plate",
            "equipment blue-plate",
            "equipment bar",
            "equipment blue-plate",
            "equipment small-yellow-plate",
            "equipment clip"
        ]

        self.assertEqual(classes, expected)

    def test_female_70kg_order(self):
        """
        TC10.15: test barbell is displayed in correct order of:
        clip > red plate > barbell > red plate > clip
        when input is female lifting 70kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("70")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment red-plate",
            "equipment bar",
            "equipment red-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected) 

    def test_female_95kg_order(self):
        """
        TC10.16: test barbell is displayed in correct order of:
        clip > small red plate > green plate > red plate > barbell > red plate > green plate > small red plate  > clip
        when input is female lifting 95kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("95")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-red-plate",
            "equipment green-plate",
            "equipment red-plate",
            "equipment bar",
            "equipment red-plate",
            "equipment green-plate",
            "equipment small-red-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)

    def test_male_25kg_order(self):
        """
        TC10.17: test barbell is displayed in correct order of:
        clip > barbell > clip
        when input is male lifting 25kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("MALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("25") 

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment bar",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)

    def test_male_26kg_order(self):
        """
        TC10.18: test barbell is displayed in correct order of:
        clip > small white plate > barbell > small white plate > clip
        when input is male lifting 26kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("MALE")
        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("26")
        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-white-plate",
            "equipment bar",
            "equipment small-white-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)

    def test_male_49kg_order(self):
        """
        TC10.19: test barbell is displayed in correct order of:
        clip > small blue plate > green plate > barbell > green plate > small blue plate > clip
        when input is male lifting 49kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("MALE")
        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("49")
        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-blue-plate",
            "equipment green-plate",
            "equipment bar",
            "equipment green-plate",
            "equipment small-blue-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)

    def test_male_69kg_order(self):
        """
        TC10.20: test barbell is displayed in correct order of:
        clip > small blue plate > blue plate > barbell > blue plate > small blue plate > clip
        when input is male lifting 69kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("MALE")
        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("69")
        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-blue-plate",
            "equipment blue-plate",
            "equipment bar",
            "equipment blue-plate",
            "equipment small-blue-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)
        
    def test_male_90kg_order(self):
        """
        TC10.21: test barbell is displayed in correct order of:
        clip > small red plate > white plate > red plate > barbell > red plate > white plate > small red plate > clip
        when input is male lifting 90kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("MALE")
        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("90")
        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment small-red-plate",
            "equipment white-plate",
            "equipment red-plate",
            "equipment bar",
            "equipment red-plate",
            "equipment white-plate",
            "equipment small-red-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)

    def test_male_155kg_order(self):
        """
        TC10.22: test barbell is displayed in correct order of:
        clip > yellow plate > red plate > red plate > barbell > red plate > red plate > yellow plate > clip
        when input is male lifting 90kg.
        """
        self.driver.find_element(By.ID, "gender").send_keys("MALE")
        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("155")
        self.driver.find_element(By.ID, "load-barbell-btn").click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, "#barbell-container .equipment")
        classes = [el.get_attribute("class") for el in elements]

        expected = [
            "equipment clip",
            "equipment yellow-plate",
            "equipment red-plate",
            "equipment red-plate",
            "equipment bar",
            "equipment red-plate",
            "equipment red-plate",
            "equipment yellow-plate",
            "equipment clip",
        ]

        self.assertEqual(classes, expected)
        

# type into terminal:
# python -m unittest tests.test_display_bb_web -v 