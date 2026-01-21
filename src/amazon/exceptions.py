class VisitURLError(Exception):
    """Custom exception for errors during URL visits."""
    pass

class LoginError(Exception):
    """Custom exception for errors during login."""
    pass

class PageParsingError(Exception):
    """Custom exception for errors during page parsing."""
    pass

class ElementNotFoundError(Exception):
    """Custom exception when a required element is not found on the page."""
    pass