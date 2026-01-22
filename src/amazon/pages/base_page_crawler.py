# General
import random
import time
import logging

# Classes
from src.amazon.selectors import BasePageSelectors
from src.amazon.selectors import LoginSelectors

# Helper functions
from src.amazon.utils.browsing import get_element

# Selenium
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# Exceptions
from src.amazon.exceptions import VisitURLError, LoginError, ElementNotFoundError

# Configuration
from config.settings import AMAZON_EMAIL
from config.settings import AMAZON_PASSWORD

logger = logging.getLogger(__name__)

class BasePage():
    def __init__(self, driver: object, asin: str, product_page_url: str):
        self.driver = driver
        self.asin = asin
        self.url = product_page_url + asin


    def _visit_url(self):
        try:
            self.driver.get(self.url)
            time.sleep(random.randint(1, 5))
            logger.info("ENTERED base page for ASIN")
        except WebDriverException as e: # e is an instance of WebDriverException
            raise VisitURLError(f"Failed to open product page URL: {self.url}") from e # saves the original exception WebDriverException
        
    def _log_in(self):
        wait = WebDriverWait(self.driver, 2)

        try:
            # Click sign in element
            sign_in_link = wait.until(ec.element_to_be_clickable((By.ID, LoginSelectors.SIGN_IN_ID)))
            sign_in_link.click()

            # Enter email and continue
            email_box = wait.until(ec.presence_of_element_located((By.ID, LoginSelectors.EMAIL_INPUT_ID)))
            email_box.send_keys(AMAZON_EMAIL)

            continue_button = self.driver.find_element(By.ID, LoginSelectors.CONTINUE_BUTTON_ID)
            continue_button.click()

            # Enter password and sign in
            password_box = wait.until(ec.presence_of_element_located((By.ID, LoginSelectors.PASSWORD_INPUT_ID)))
            password_box.send_keys(AMAZON_PASSWORD)

            sign_in_button = self.driver.find_element(By.ID, LoginSelectors.SIGN_IN_BUTTON_ID)
            sign_in_button.click()
            time.sleep(random.randint(3, 7))
            
            wrong_password_element = bool(get_element(self.driver, By.XPATH, LoginSelectors.WRONG_PASSWORD_ID))
            if wrong_password_element:
                raise LoginError("Wrong password")
            logger.info("Logged in successfully")

        except Exception as e:
            raise LoginError(f"Failed to log in from product page: {self.url}") from e

    def crawl_page(self) -> tuple[object, str]:
        # Visit URL
        self._visit_url()

        # Log in
        # self._log_in()

        # Check for multiple sellers
        multiple_sellers = bool(get_element(self.driver, By.ID, BasePageSelectors.MULTIPLE_SELLERS_BOX_ID))
        if not multiple_sellers:
            logger.warning("No multiple sellers for this asin %s", self.asin)

        # Check product main body element
        product_main_body_element = get_element(self.driver, By.ID, BasePageSelectors.MAIN_CONTAINER_ID)
        if not product_main_body_element:
            raise ElementNotFoundError("Product's main body element not found")
        
        # Get brand of the product
        brand_element = get_element(self.driver, By.XPATH, BasePageSelectors.BRAND_XPATH)
        if brand_element:
            brand = brand_element.text.strip()
        else:
            logger.warning("No brand found for asin %s", self.asin)
            brand = None

        # Get current page seller information
        seller_element = get_element(self.driver, By.ID, BasePageSelectors.SELLER_ID)
        if seller_element:
            logger.info("BASE SELLER ELEMENT found for asin %s", self.asin)
            return seller_element, brand
        else:
            raise ElementNotFoundError("Seller element not found")
        