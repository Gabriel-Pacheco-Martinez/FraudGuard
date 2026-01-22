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
        next_button_elem.click()
        get_element(driver, By.TAG_NAME, StorefrontSelectors.BODY_TAG)
        time.sleep(random.randint(3, 7))
        return True

    except NoSuchElementException as e:
        return False
    except Exception as e:
        return False