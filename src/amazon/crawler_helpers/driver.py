# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Seleniumwire
from seleniumwire import webdriver

# Helpers
from src.amazon.crawler_helpers.rotator import ProxyRotator

class DriverManager():
    def __init__(self):
        self.proxy_rotator = ProxyRotator()

    # =======================
    # Proxy with no auth
    def setup_driver(self):
        options = Options()
        # options.add_argument("--headless=new")
        # options.add_argument("--auto-open-devtools-for-tabs")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15")
       
        # Proxy
        random_proxy = self.proxy_rotator.get_proxy()
        options.add_argument(f"--proxy-server={random_proxy['ip']}:{random_proxy['port']}")
        
        # Performance
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "webauthn.allow_autofill": False
        })

        # Driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_cdp_cmd("Network.enable", {})
        
        return driver
    
    # # =======================
    # # Proxy with auth
    # def setup_driver_with_auth_proxy(self):
    #     options = Options()
    #     # options.add_argument("--headless=new")
    #     # options.add_argument("--auto-open-devtools-for-tabs")
    #     options.add_argument("--start-maximized")
    #     options.add_argument("--disable-gpu")
    #     options.add_argument("--no-sandbox")
    #     options.add_argument("--disable-dev-shm-usage")
    #     options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15")

    #     # Proxy
    #     random_proxy = self.proxy_rotator.get_proxy()

    #     seleniumwire_options = {
    #         "proxy": {
    #             "http": f"http://{random_proxy['user']}:{random_proxy['pass']}@{random_proxy['ip']}:{random_proxy['port']}",
    #             "https": f"https://{random_proxy['user']}:{random_proxy['pass']}@{random_proxy['ip']}:{random_proxy['port']}",
    #             "no_proxy": "localhost,127.0.0.1",
    #         }
    #     }

    #     # Performance
    #     options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    #     options.add_experimental_option("prefs", {
    #         "credentials_enable_service": False,
    #         "profile.password_manager_enabled": False,
    #         "webauthn.allow_autofill": False
    #     })

    #     # Driver
    #     service = Service(ChromeDriverManager().install())
    #     driver = webdriver.Chrome(service=service, options=options, seleniumwire_options=seleniumwire_options)
    #     driver.execute_cdp_cmd("Network.enable", {})
        
    #     return driver