import unittest 
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

class TestBarbellSetupWeb(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver.get('http://127.0.0.1:5500/html/display_bb_dashboard.html') 

        self.driver.get('http://127.0.0.1:5500/html/nav_bar.html') 
        self.driver.find_element(By.XPATH, "//a[@href='#display_bb']").click()

    def tearDown(self):
        self.driver.quit()

    # def test_page_title(self):
    #     """
    #     TC1: check page title is "Weightlifting Barbell Setup Loader"
    #     """
    #     expected_page_title =  "Weightlifting Barbell Setup Loader"
    #     self.assertIn(expected_page_title, self.driver.title)

    def test_gender_input_exist(self):
        """
        TC2: check exitance of gender input dropdown 
        """
        gender_dropdown_input = self.driver.find_element(By.ID, "gender")
        self.assertIsNotNone(gender_dropdown_input) 

    def test_only_female_and_male_gender_option_exist(self):
        """
        TC: check existance of female and male gender option only 
        """
        gender_input_select = Select(self.driver.find_element(By.ID, "gender") )
        option_values = [option.get_attribute("value") for option in gender_input_select.options if option.get_attribute("value")]
        expected_values = ["FEMALE", "MALE"]
        self.assertCountEqual(option_values, expected_values)

    def test_attempt_weight_input_exist(self):
        """
        TC3: check exitance of attempt weight input  
        """
        attempt_weight_input = self.driver.find_element(By.ID, "weight") 
        self.assertIsNotNone(attempt_weight_input)

    def test_load_barbell_button_exist(self):
        """
        TC4: check exitance of "load barbell" button  
        """
        load_barbell_button = self.driver.find_element(By.ID, "load-barbell-btn") 
        self.assertIsNotNone(load_barbell_button)

    def test_error_message_exist(self):
        """
        TC5: check for container to display error message
        """
        error_message = self.driver.find_element(By.ID, "error-message")
        self.assertIsNotNone(error_message) 

    def test_barbell_display_exist(self):
        """
        TC6: check exitance container for barbell-display
        """
        barbell_display_div = self.driver.find_element(By.ID, "barbell-display")
        self.assertIsNotNone(barbell_display_div) 

    def test_weight_info_exist(self):
        """
        TC7: check exitance container for attempt weight display
        """
        weight_info = self.driver.find_element(By.ID, "weight-info")
        self.assertIsNotNone(weight_info)

    def test_click_enter(self):
        """
        TC8: check if user hit "enter" on keyboard, it is similar as manully clicking the "Load barbell setup" button.
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
        TC9: check initially error message is hidden
        """
        self.assertFalse(self.driver.find_element(By.ID, "error-message").is_displayed())


    def test_female_19kg_order_display_error_message(self):
        """
        TC10: check if user enter invalid input weight (gender = FEMALE, attempt-weight = 19kg), 
        the container for error message will appear to display error message
        """
        self.driver.find_element(By.ID, "gender").send_keys("FEMALE")

        self.driver.find_element(By.ID, "weight").clear()
        self.driver.find_element(By.ID, "weight").send_keys("19")

        self.driver.find_element(By.ID, "load-barbell-btn").click()

        self.assertTrue(self.driver.find_element(By.ID, "error-message").is_displayed())

    def test_female_20kg_order(self):
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

    def test_male_24kg_order_display_error_message(self):
        """
        check if user enter invalid input weight (gender = MALE, attempt-weight = 24kg), 
        the container for error message will appear to display error message
        """
        pass

    def test_male_25kg_order(self):
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
        


    ### CONTINUE THE OTHER MALE BARBELL SETUP ORDER    

# type into terminal:
# python -m unittest tests.test_barbell_setup_web -v 