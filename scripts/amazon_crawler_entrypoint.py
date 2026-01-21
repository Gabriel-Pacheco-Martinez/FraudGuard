# General
from typing import List

# Classes
import src.logger
import logging
from src.amazon.utils.write_results import Writer
from src.amazon.crawler_helpers.driver import DriverManager
from src.amazon.pages.base_page_crawler import BasePage

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
    # Loop through asins
    for index, asin in enumerate(asins_to_process):
        print("===================================")
        print(f"[🔍] Looking into ASIN {index+1}: {asin}")
        print("===================================")
        logger.info("="*50)
        logger.info("Looking into ASIN %s", asin)
        logger.info("="*50)

        # ------
        # Setup driver: new one for each asin
        driver_manager = DriverManager()
        driver = driver_manager.setup_driver()

        # ------
        # Go to main product page
        try:
            base_page = BasePage(driver, asin, PRODUCT_PAGE_URL)
            sold_by_element = base_page.crawl_page()
        except VisitURLError as e:
            logger.error("Error processing product page for ASIN %s", asin)
        except LoginError as e:
            logger.error("Error processing product page for ASIN %s", asin)
        except ElementNotFoundError as e:
            logger.error("Error processing product page for ASIN %s", asin)
        except Exception as e:
            logger.error("Error processing product page for ASIN %s", asin)

        # ------
        # Close driver
        # driver_manager.close_driver()

    # ======
    print("Code finished")
