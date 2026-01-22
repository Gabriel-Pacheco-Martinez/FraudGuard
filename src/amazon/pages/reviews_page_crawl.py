class ReviewsPage():
    def __init__(self, driver: object, asin: str, reviews_page_url: str):
        self.driver = driver
        self.url = reviews_page_url + asin

    def crawl_page(self):
        self.driver.get(self.url)