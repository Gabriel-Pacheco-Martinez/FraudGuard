# General
import logging
import time
import random

# Classes
from src.amazon.selectors import OffersPageSelectors


# Helper functions
from src.amazon.utils.browsing import get_element

# Selenium
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Exceptions
from src.amazon.exceptions import VisitURLError, ElementNotFoundError

logger = logging.getLogger(__name__)

class OffersPage():
    def __init__(self, driver: object, asin: str, offers_page_url: str):
        self.driver = driver
        self.asin = asin
        self.url = offers_page_url + asin

    def _visit_url(self):
        try:
            self.driver.get(self.url)
            time.sleep(random.randint(1, 5))
            logger.info("ENTERED offers page for ASIN")
        except WebDriverException as e: # e is an instance of WebDriverException
            raise VisitURLError(f"Failed to open offers page URL: {self.url}") from e # saves the original exception WebDriverException

    def crawl_page(self):
        # Visit URL
        self._visit_url()

        # Check for sellers
        sellers_elements = []

        try:
            # Loop over offer blocks
            offer_blocks = get_element(self.driver, By.ID, OffersPageSelectors.OFFER_ITEMS_ID, condition=ec.presence_of_all_elements_located)
            for offer_block in offer_blocks:
                try:
                    # Grab seller element
                    seller_elem = offer_block.find_element(By.ID, OffersPageSelectors.SELLER_CONTAINER_ID)

                    # Avoid duplicates
                    if seller_elem not in sellers_elements:
                        sellers_elements.append(seller_elem)
                except NoSuchElementException:
                    logger.warning("No main body for sellers found.")
            return sellers_elements

        except NoSuchElementException:
            logger.warning("No main body for sellers found.")
            return []
