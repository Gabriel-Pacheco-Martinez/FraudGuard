# General
import logging
import time
import random
from datetime import datetime

# Classes
from src.amazon.selectors import ReviewPageSelectors
    
# Helper functions
from src.amazon.utils.browsing import open_new_handle_tab
from src.amazon.utils.browsing import get_element
from src.amazon.utils.browsing import click_next_page_reviews

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)

class ReviewsPage():
    def __init__(self, driver: object, asin: str, reviews_page_url: str):
        self.driver = driver
        self.url = reviews_page_url + asin

    def _get_review_information(self, review_element: WebElement):
        # Review id
        review_id = review_element.get_attribute("id")

        # Review location and date
        metadata_text = review_element.find_element(By.XPATH, ReviewPageSelectors.REVIEW_DATE_XPATH).text
        metadata_parts = metadata_text.replace("Reviewed in the","").split("on")
        location, date_str = map(str.strip, metadata_parts)
        if date_str:
            date = datetime.strptime(date_str, "%B %d, %Y").date()

        # Body text
        body_text = review_element.find_element(By.XPATH, ReviewPageSelectors.REVIEW_BODY_XPATH).text.strip()
        if not body_text:
            logger.warning("No body text found for review %s", review_id)

        # Review dict
        review = {
            "id": review_id,
            "location": location,
            "date": date,
            "body": body_text
        }

        return review

    def crawl_page(self):
        # Retain storefront handle to return later
        storefront_handle = self.driver.current_window_handle
        handles = set(self.driver.window_handles)

        # Go to new tab
        self.driver.switch_to.new_window('tab')
        self.driver.get(self.url)
        time.sleep(random.uniform(2,5))
        open_new_handle_tab(self.driver, handles)

        # Grab review metadata
        rating = get_element(self.driver, By.CSS_SELECTOR, ReviewPageSelectors.RATING_CSS).text.strip()
        num_ratings = get_element(self.driver, By.CSS_SELECTOR, ReviewPageSelectors.TOTAL_REVIEWS_CSS).text.strip()
        reviews = []

        # Loop through the pages of reviews
        page_counter = 1
        while True:
            curr_page_review_elements = get_element(self.driver, By.XPATH, ReviewPageSelectors.REVIEW_ITEMS_XPATH, condition=ec.presence_of_all_elements_located)
            if not curr_page_review_elements:
                logger.warning("No reviews found for this product")
                break
            
            logger.info("Looping over reviews for product, page %s", page_counter)
            for review_element in curr_page_review_elements:
                review = self._get_review_information(review_element)
                reviews.append(review)
                            
            # Click next page
            page_counter += 1
            next_page = click_next_page_reviews(self.driver)
            if not next_page:
                break

        # Return to storefront
        self.driver.close()
        self.driver.switch_to.window(storefront_handle)

        # Review data & metadata for a product
        reviews_product = {
            "reviews": reviews,
            "average_ratings": rating,
            "number_of_ratings": num_ratings
        }

        return reviews_product
