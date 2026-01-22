# Login Page
class LoginSelectors:
    SIGN_IN_ID = "nav-link-accountList"
    EMAIL_INPUT_ID = "ap_email_login"
    CONTINUE_BUTTON_ID = "continue"
    PASSWORD_INPUT_ID = "ap_password"
    SIGN_IN_BUTTON_ID = "signInSubmit"
    WRONG_PASSWORD_ID = "//div[contains(@class, 'a-alert-container')]//div[contains(@class, 'a-alert-content') and contains(text(), 'Your password is incorrect')]"

class BasePageSelectors:
    MAIN_CONTAINER_ID = "dp-container"
    SELLER_ID = "sellerProfileTriggerId"
    MULTIPLE_SELLERS_BOX_ID = "dynamic-aod-ingress-box"
    MANUFACTURER_XPATH = "//ul[contains(@class, 'detail-bullet-list')]//span[contains(text(),'Manufacturer')]/following-sibling::span"
    BRAND_XPATH = "//ul[contains(@class, 'detail-bullet-list')]//span[contains(text(),'Brand')]/following-sibling::span"    
    STOREFRONT_LINK_XPATH = "//a[contains(@class,'a-link-normal') and contains(text(),'storefront')]"

class ProductPageSelectors:
    STOREFRONT_XPATH = "//a[contains(@class,'a-link-normal') and contains(text(),'storefront')]"

class OffersPageSelectors:
    OFFER_ITEMS_ID = "aod-offer"
    SELLER_CONTAINER_ID = "aod-offer-soldBy"
    SELLER_LINK_TAG = "a"

class StorefrontSelectors:
    BODY_TAG = "body"
    PRODUCT_ITEMS_XPATH = "//div[@role='listitem']"
    PRODUCT_ASIN_ATTR = "data-asin"
    NEXT_PAGE_BUTTON_CSS = ".s-pagination-next"
    PAGINATION_DISABLED_CLASS = "s-pagination-disabled"

class ReviewPageSelectors:
    RATING_CSS = "span[data-hook='rating-out-of-text']"
    TOTAL_REVIEWS_CSS = "div[data-hook='total-review-count'] span"
    REVIEW_ITEMS_XPATH = "//li[@data-hook='review']"
    REVIEW_DATE_XPATH = ".//span[@data-hook='review-date']"
    REVIEW_BODY_XPATH = ".//span[@data-hook='review-body']//span"
    PAGINATION_LAST_CSS = "ul.a-pagination li.a-last"
    PAGINATION_DISABLED_CLASS = "a-disabled"

