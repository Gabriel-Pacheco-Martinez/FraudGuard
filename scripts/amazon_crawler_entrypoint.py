# General
from typing import List, Dict

# Classes
import src.logger
import logging
from src.amazon.utils.write_results import Writer
from src.amazon.crawler_helpers.driver import DriverManager
from src.amazon.pages.base_page_crawler import BasePage
from src.amazon.pages.product_page_crawler import ProductPage

# Helper functions
from src.amazon.utils import read_asins

# Exceptions
from src.amazon.exceptions import VisitURLError, LoginError, ElementNotFoundError

# Configuration
from config.settings import ASINS_FILE_PATH
from config.settings import RESULTS_FILE_PATH
from config.settings import PRODUCT_PAGE_URL

logger = logging.getLogger(__name__)

def run():
    logger.info("Crawler started")

    # ======
    # Extract asins to be processed
    asins_to_process: List = read_asins.read_asins_from_file(ASINS_FILE_PATH)

    # ======
    # Initialize results json file
    results_writer = Writer(RESULTS_FILE_PATH)

    # ======
    # Create JSON
    telegram_asins: dict[str, dict] = {} # A dictionary for each ASIN

    # ======
    # Loop through asins
    for index, asin in enumerate(asins_to_process):
        print("===================================")
        print(f"[🔍] Looking into ASIN {index+1}: {asin}")
        print("===================================")
        logger.info("="*50)
        logger.info("[🔍] Looking into telegram ASIN %s: %s ", index+1, asin)
        logger.info("="*50)

        # ------
        # Setup driver: new one for each asin
        driver_manager = DriverManager()
        driver = driver_manager.setup_driver()

        # ------
        # Create dictionary for asin
        telegram_asins[asin] = {
            "brand": None,
            "sellers": {}
        }

        # ------
        # Go to asin base page
        list_of_seller_elements: List = []
        try:
            base_page = BasePage(driver, asin, PRODUCT_PAGE_URL)
            sold_by_element, brand = base_page.crawl_page()
            list_of_seller_elements.append(sold_by_element)

            seller = sold_by_element.text.strip()
            telegram_asins[asin]["brand"] = brand
            telegram_asins[asin]["sellers"][seller] = {}

        except VisitURLError as e:
            logger.error("Error processing base page for ASIN %s", asin)
        except LoginError as e:
            logger.error("Error processing base page for ASIN %s", asin)
        except ElementNotFoundError as e:
            logger.error("Error processing base page for ASIN %s", asin)
        except Exception as e:
            logger.error("Error processing base page for ASIN %s", asin)

        # ------
        # Go to product pages for all sold_by elements
        for seller_element in list_of_seller_elements:
            seller = seller_element.text.strip()
            telegram_asins[asin]["sellers"][seller] = {}
            telegram_asins[asin]["brand"]= brand

            try:
                product_page = ProductPage(driver, sold_by_element)
                product_page.crawl_page()
            except ElementNotFoundError as e:
                logger.error("Error processing product page for ASIN %s", asin)
            except Exception as e:
                logger.error("Error processing product page for ASIN %s", asin)
        
        # ------
        # Close driver
        # driver_manager.close_driver()

    # ======
    print("Code finished")
