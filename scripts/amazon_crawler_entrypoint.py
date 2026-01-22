# General
from typing import Any
import json
from colorama import Fore, Style

# Classes
import src.logger
import logging
from src.amazon.utils.write_results import Writer
from src.amazon.crawler_helpers.driver import DriverManager
from src.amazon.pages.base_page_crawler import BasePage
from src.amazon.pages.seller_page_crawler import SellerPage

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
    asins_to_process: list = read_asins.read_asins_from_file(ASINS_FILE_PATH)

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
        logger.info(Fore.GREEN + "="*50)
        logger.info("[🔍] Looking into telegram ASIN %s: %s ", index+1, asin)
        logger.info("="*50 + Style.RESET_ALL)

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
        list_of_seller_elements: list = []
        try:
            base_page = BasePage(driver, asin, PRODUCT_PAGE_URL)
            sold_by_element, brand = base_page.crawl_page()
            list_of_seller_elements.append(sold_by_element)

            seller = sold_by_element.text.strip()
            telegram_asins[asin]["brand"] = brand
            telegram_asins[asin]["sellers"][seller] = {}

        except VisitURLError as e:
            logger.error(Fore.RED + "Error processing base page for ASIN %s. Error: %s" + Style.RESET_ALL, asin, e)
        except LoginError as e:
            logger.error(Fore.RED + "Error processing base page for ASIN %s. Error: %s" + Style.RESET_ALL, asin, e)
        except ElementNotFoundError as e:
            logger.error(Fore.RED + "Error processing base page for ASIN %s. Error: %s" + Style.RESET_ALL, asin, e)
        except Exception as e:
            logger.error(Fore.RED + "Error processing base page for ASIN %s. Error: %s" + Style.RESET_ALL, asin, e)

        # ------
        # Go to product pages for all sold_by elements
        for seller_element in list_of_seller_elements:
            seller_name = seller_element.text.strip()
            telegram_asins[asin]["sellers"][seller_name] = {}
            telegram_asins[asin]["brand"]= brand

            try:
                seller_page = SellerPage(driver)
                seller_crawl_information: dict[str, Any] = seller_page.crawl_page(seller_element, seller_name)
                telegram_asins[asin]["sellers"][seller_name] = seller_crawl_information
            except ElementNotFoundError as e:
                logger.error(Fore.RED + "Error processing product pages for ASIN %s. Error: %s" + Style.RESET_ALL, asin, e)
            except Exception as e:
                logger.error(Fore.RED +"Error processing product pages for ASIN %s. Error: %s" + Style.RESET_ALL, asin, e)
        
        # ------
        # Write results to file
        results_writer.write_results(telegram_asins)

        # ------
        # Close driver
        driver.quit()

    # ======
    print("Code finished")
