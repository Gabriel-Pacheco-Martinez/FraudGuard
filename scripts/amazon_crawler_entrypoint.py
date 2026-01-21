# General
from typing import List

# Classes
import src.logger
import logging
from src.amazon.utils.write_results import Writer
from src.amazon.crawler_helpers.driver import DriverManager
from src.amazon.pages.product_page_scraper import ProductPage

# Helper functions
from src.amazon.utils import read_asins

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
        print(f"[🔍] Looking into ASIN {index}: {asin}")
        print("===================================")

        # ------
        # Setup driver: new one for each asin
        driver_manager = DriverManager()
        driver = driver_manager.setup_driver()

        # ------
        # Go to main product page
        try:
            product_page = ProductPage(driver, asin, PRODUCT_PAGE_URL)
            product_page.crawl_page()
        except Exception as e:
            logger.exception(f"Error processing product page for ASIN {asin}. Error: {e}")


        
