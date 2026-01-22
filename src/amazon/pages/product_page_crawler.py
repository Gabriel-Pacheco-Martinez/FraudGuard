# General
import logging

# Classes
from src.amazon.selectors import ProductPageSelectors
from src.amazon.pages.storefront_page_crawler import StorefrontPage

# Helper functions
from src.amazon.utils.browsing import get_element

# Selenium
from selenium.webdriver.common.by import By

# Exceptions
from src.amazon.exceptions import ElementNotFoundError

logger = logging.getLogger(__name__)

class ProductPage():
    def __init__(self, driver: object, sold_by_element: object):
        self.driver = driver
        self.sold_by_element = sold_by_element

    def crawl_page(self):
        # Enter product page through seller
        self.sold_by_element.click()
        seller_name = self.sold_by_element.text.strip()
        logger.info("Entered product page through seller: %s", seller_name)
        
        # Visit storefront page
        storefront_element = get_element(self.driver, By.XPATH, ProductPageSelectors.STOREFRONT_XPATH)
        if not storefront_element:
            raise ElementNotFoundError("Storefront element not found")
        storefront_page = StorefrontPage(self.driver, storefront_element)
        storefront_page.crawl_page()