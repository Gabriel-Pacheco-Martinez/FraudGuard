# ===============
# Settings: rules & guarantees. [What is allowed].
#   Eg:paths + env + hard constraints
# ===============
import os
from dotenv import load_dotenv

# Load .env secrets
load_dotenv()
AMAZON_EMAIL = os.getenv("AMAZON_EMAIL")
AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")

# Paths
ASINS_FILE_PATH = "data/asins/test.txt"
RESULTS_FILE_PATH = "data/results/results.json"
LOGS_PATH = "data/logs/"
LOGS_FILE = "data/logs/app.log"

# URLS
PRODUCT_PAGE_URL = "https://www.amazon.com/dp/"