# General
import logging
from typing import Any

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

class SellerPage():
    def __init__(self, driver: object):
        self.driver = driver

    def crawl_page(self, seller_element: object, seller_name: str) -> dict[str, Any]:
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
        # Enter product page through seller
        seller_element.click()
        logger.info("Entered seller page: %s", seller_name)
        
        # Visit storefront page
        storefront_element = get_element(self.driver, By.XPATH, ProductPageSelectors.STOREFRONT_XPATH)
        if not storefront_element:
            raise ElementNotFoundError("Storefront element not found")
        storefront_page = StorefrontPage(self.driver, seller_name)
        seller_crawl_information: dict[str, Any] =storefront_page.crawl_page(storefront_element)
        return seller_crawl_information