# General
import logging
from typing import Any
import time
import random

# Classes
from src.amazon.selectors import StorefrontSelectors

# Selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

def get_element(driver, by, value, timeout=10, condition: Any = ec.presence_of_element_located):
    try:
        element = WebDriverWait(driver, timeout).until(condition((by, value)))
        return element
    except(TimeoutException, NoSuchElementException):
        return None
    
def click_next_page_products(driver):
    try:
        # Get button element
        next_button_elem = get_element(driver, By.CSS_SELECTOR, StorefrontSelectors.NEXT_PAGE_BUTTON_CSS, condition=ec.element_to_be_clickable)
        if StorefrontSelectors.PAGINATION_DISABLED_CLASS in next_button_elem.get_attribute("class"):
            logger.info("No next page in storefront")
            return False

        # Click button
        time.sleep(random.randint(3, 7))
        next_button_elem.click()
        get_element(driver, By.TAG_NAME, StorefrontSelectors.BODY_TAG)
        time.sleep(random.randint(1, 3))
        return True

    except NoSuchElementException:
        return False
    except Exception:
        return False
    
def click_next_page_reviews(driver):
    try:
        # Get button element
        pagination_elem = driver.find_element(By.CSS_SELECTOR, "ul.a-pagination li.a-last")

        # Button disabled
        if "a-disabled" in pagination_elem.get_attribute("class"):
            return False

        # Click button
        next_link = pagination_elem.find_element(By.TAG_NAME, "a")
        time.sleep(random.randint(3, 7))
        next_link.click()
        # get_element(driver, By.TAG_NAME, "body")
        time.sleep(random.randint(1, 3))
        return True

    except NoSuchElementException:
        return False
    except TimeoutException:
        return False

def open_new_handle_tab(driver, listing_handles):
    # Get new handles
    wait = WebDriverWait(driver, 5)
    wait.until(lambda d: len(d.window_handles) > len(listing_handles))
    new_handles = set(driver.window_handles) - listing_handles
    if not new_handles:
        logging.warning("Reviews window not detected")

    # Switch to new handle
    new_handle = new_handles.pop()
    driver.switch_to.window(new_handle)