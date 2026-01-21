# General
from typing import Any

# Selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_element(driver, by, value, timeout=10, condition: Any = ec.presence_of_element_located):
    try:
        element = WebDriverWait(driver, timeout).until(condition((by, value)))
        return element
    except(TimeoutException, NoSuchElementException):
        return None