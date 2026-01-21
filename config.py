import os
from pathlib import Path
from dotenv import load_dotenv


# ======
# Amazon credentials
# ======
load_dotenv()
AMAZON_EMAIL = os.getenv("AMAZON_EMAIL")
AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")

if not AMAZON_EMAIL or not AMAZON_PASSWORD:
    raise ValueError("Amazon credentials not in .env file")

# =======
# URLS
# =======
AMAZON_BASE_URL = "https://www.amazon.com"

# Get product URL for a given ASIN
def get_product_url(asin: str) -> str:
    return f"{AMAZON_BASE_URL}/dp/{asin}"

# Get reviews page URL for a given ASIN
def get_product_reviews_url(asin: str) -> str:
    return f"{AMAZON_BASE_URL}/product-reviews/{asin}"

# Get offers listing URL for a given ASIN
def get_product_offers_url(asin: str) -> str:
    return f"{AMAZON_BASE_URL}/gp/offer-listing/{asin}"

# ======
# TIMEOUTS & DELAYS
# ======
LOGIN_WAIT_TIME = 15                # Wait after successful login
PAGE_LOAD_TIMEOUT = 30              # Seconds to wait for page load
ELEMENT_WAIT_TIMEOUT = 10           # Seconds to wait for elements
MIN_DELAY_BETWEEN_REQUESTS = 2.0    # Seconds between requests (anti-detection)
MAX_DELAY_BETWEEN_REQUESTS = 5.0

# ======
# RETRY CONFIGURATION
# ======
MAX_RETRIES = 3
RETRY_DELAY = 2.0                   # Initial delay (doubles with each retry)
RETRY_BACKOFF_MULTIPLIER = 2.0

# ======
# BROWSER SETTINGS
# ======
HEADLESS_MODE = False           # Set to True to hide browser window
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"

# =======
# FILE PATHS
# =======
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE_ASINS = INPUT_DIR / "telegram_asins.txt"
OUTPUT_FILE_RESULTS = OUTPUT_DIR / "products.json"
LOGS_FILE = LOGS_DIR / "scraper.log"

# ======
# CSS/XPATH SELECTORS - Organized by Page Type
# ======


# ======
# LOGGING CONFIGURATION
# ======
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)-8s | %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOGS_FILE),
            'maxBytes': 10_000_000,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed',
            'encoding': 'utf-8'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console']
    }
}