# General
import logging

# Classes
from src.amazon.selectors import StorefrontSelectors
from src.amazon.pages.reviews_page_crawl import ReviewsPage

# Helper functions
from src.amazon.utils.browsing import get_element

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

# Exceptions
from src.amazon.exceptions import ElementNotFoundError

# Configuration
from config.settings import REVIEW_PAGE_URL

logger = logging.getLogger(__name__)

class StorefrontPage():
    def __init__(self, driver: object, storefront_element: object):
        self.driver = driver
        self.storefront_element = storefront_element

    def crawl_page(self):
        # Enter the storefront
        self.storefront_element.click()
        logger.info("Entered storefront page")

        # Loop trough all products/pages
        while True:
            # Check for body
            storefront_body_element: object = get_element(self.driver, By.TAG_NAME, StorefrontSelectors.BODY_TAG)
            if not storefront_body_element:
                raise ElementNotFoundError("Storefront body element not found")
            
            # Get products
            products_elements: object = get_element(self.driver, By.XPATH, StorefrontSelectors.PRODUCT_ITEMS_XPATH, condition=ec.presence_of_all_elements_located )
            if not products_elements:
                raise ElementNotFoundError("Product items elements not found")

            # Loop over products
            for product_element in products_elements:
                product_asin = product_element.get_attribute("data-asin")
                reviews_page = ReviewsPage(self.driver, product_asin, REVIEW_PAGE_URL)
                reviews_page.crawl_page() 
                
            # Click next page
