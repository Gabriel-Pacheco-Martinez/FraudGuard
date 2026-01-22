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

# PATHS
ASINS_FILE_PATH = "data/asins/test.txt"
RESULTS_FILE_PATH = "data/results/results.json"
LOGS_PATH = "data/logs/"
LOGS_FILE = "data/logs/app.log"

# URLS
PRODUCT_PAGE_URL = "https://www.amazon.com/dp/"
REVIEW_PAGE_URL = "https://www.amazon.com/product-reviews/"

# PROXIES
proxies = [
    "108.141.130.146:80",
    "108.162.192.0:80",
    "108.162.192.12:80",
    "108.162.192.10:80",
    "101.255.107.85:1111",
    "108.162.192.147:80",
    "1.10.141.115:8080",
    "102.177.176.105:80",
    "101.109.122.174:8180",
    "108.162.192.12:80",
    "108.162.192.113:80",
    "108.141.130.146:80",
    "1.54.172.229:16000",
    "1.52.198.150:16000",
    "170.114.45.108:80",
    "138.68.60.8:80",
    "141.101.113.101:80",
    "138.121.113.179:999",
    "138.124.81.12:8888",
    "170.114.45.109:80",
    "139.59.222.40:3128",
    "138.124.49.149:10808",
    "170.114.45.122:80",
    "14.34.180.21:38157",
    "170.0.11.11:8080",
    "108.162.192.123:80",
    "170.114.45.103:80",
    "138.219.251.28:3128",
    "170.114.45.0:80"
]
proxy_user = ""
proxy_pass = ""