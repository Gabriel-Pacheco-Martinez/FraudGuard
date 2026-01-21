# General
import random
import time

# Selenium
from selenium.common.exceptions import WebDriverException

class ProductPage():
    def __init__(self, driver: object, asin: str, product_page_url: str):
        self.driver = driver
        self.asin = asin
        self.base_url = product_page_url

    def _visit_url(self):
        url = self.base_url + self.asin
        try:
            self.driver.get(url)
            time.sleep(random.randint(1, 5))
        except WebDriverException as e: # e is an instance of WebDriverException
            raise RuntimeError("Failed to open product page URL: {url}") from e # saves the original exception WebDriverException

    def crawl_page(self):
        # Visit URL
        self._visit_url()

        # Log in
        
