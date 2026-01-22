# General
import logging
from typing import Any

# Classes
from src.amazon.selectors import StorefrontSelectors
from src.amazon.pages.reviews_page_crawl import ReviewsPage

# Helper functions
from src.amazon.utils.browsing import get_element
from src.amazon.utils.browsing import click_next_page_products

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement

# Exceptions
from src.amazon.exceptions import ElementNotFoundError

# Configuration
from config.settings import REVIEW_PAGE_URL

logger = logging.getLogger(__name__)

class StorefrontPage():
    def __init__(self, driver: object, seller_name: str):
        self.driver = driver
        self.seller = seller_name

    def crawl_page(self, storefront_element: WebElement) -> dict[str, Any]:
        """
        METHOD:
            Returns a dict with information about the seller:
            {
                "products": {
                    asin: {
                        "reviews": list,
                        "average_rating_product_asin": float
                    }
                },
                "date_original_asin": str | None,
                "average_rating": float | None
            }
        """
        # Enter the storefront
        storefront_element.click()
        logger.info("Entered seller store frontpage: %s", self.seller)

        # Create 
        seller: dict[str,any] = {
            "products": {},
            "date_original_asin": None,
            "average_rating": None
        }

        # Loop trough all products/pages
        page_counter = 1
        while True:

            # Check for body
            storefront_body_element: WebElement = get_element(self.driver, By.TAG_NAME, StorefrontSelectors.BODY_TAG)
            if not storefront_body_element:
                raise ElementNotFoundError("Storefront body element not found")
            
            # Get products
            products_elements: list[WebElement] = get_element(self.driver, By.XPATH, StorefrontSelectors.PRODUCT_ITEMS_XPATH, condition=ec.presence_of_all_elements_located )
            if not products_elements:
                raise ElementNotFoundError("Elements for products not found")

            # Loop over products
            logger.info("Looping over products for page %s", page_counter)
            for product_element in products_elements:
                # Current product
                product_asin = product_element.get_attribute("data-asin")
                if not product_asin:
                    logger.warning("Asin attribute not found for product %s", product_element)
                    return
        
                # Go to reviews page for product
                reviews_page_for_product = ReviewsPage(self.driver, product_asin, REVIEW_PAGE_URL)
                seller["products"][product_asin] = reviews_page_for_product.crawl_page()
                
            # Click next page
            page_counter += 1
            next_page = click_next_page_products(self.driver)
            if not next_page:
                break

        # Return
        return seller