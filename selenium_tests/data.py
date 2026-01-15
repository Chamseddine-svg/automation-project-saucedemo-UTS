"""
CONFIGURATION AND TEST DATA FILE
Contains all test data, configurations, and constants for the test suite.
Centralized location for easy maintenance and updates.
"""

# ============================
# TEST CONFIGURATION SETTINGS
# ============================
CONFIG = {
    # Timeout settings (in seconds) for different scenarios
    "timeouts": {
        "implicit_wait": 5,           # Default implicit wait for WebDriver
        "explicit_wait_short": 5,     # Short explicit wait for quick elements
        "explicit_wait_long": 10,     # Long explicit wait for slow elements
        "explicit_wait_very_long": 15,# Very long wait for page transitions
        "short_sleep": 0.5,           # Short pause for UI updates
        "medium_sleep": 1,            # Medium pause for page interactions
        "long_sleep": 2,              # Long pause for page loads
        "page_load": 3                # Page load timeout
    },
    
    # Test execution settings
    "product_count": 6,               # Expected number of products on inventory page
    "screenshot_dir": "screenshots",  # Directory to save screenshots
    "retry_attempts": 2,              # Number of retry attempts for flaky tests
    "retry_delay": 1                  # Delay between retry attempts (seconds)
}

# ============================
# APPLICATION URLS
# ============================
URLS = {
    "login": "https://www.saucedemo.com/",               # Login page URL
    "inventory": "https://www.saucedemo.com/inventory.html",  # Inventory page URL
    "base_url": "https://www.saucedemo.com"              # Base URL for navigation
}

# ============================
# PAGE URL PATTERNS
# Used for verifying current page or URL patterns
# ============================
PAGE_PATTERNS = {
    "inventory_page": "/inventory.html",                 # Pattern for inventory page
    "product_detail_page": ["inventory-item.html", "?id="]  # Patterns for product detail page
}

# ============================
# LOGIN TEST DATA
# Test cases for login functionality testing
# Each case includes input data and expected results
# ============================
LOGIN_ERRORS = [
    {
        "case": "empty_username",     # Test case identifier
        "username": "",               # Username input (empty)
        "password": "secret_sauce",   # Password input
        "expected_error": "Epic sadface: Username is required"  # Expected error message
    },
    {
        "case": "empty_password",
        "username": "standard_user",
        "password": "",  # Empty password
        "expected_error": "Epic sadface: Password is required"
    },
    {
        "case": "invalid_user",
        "username": "wrong_user",     # Non-existent username
        "password": "wrong_pass",     # Wrong password
        "expected_error": "Epic sadface: Username and password do not match any user in this service"
    },
    {
        "case": "locked_out_user",
        "username": "locked_out_user",  # Locked out user account
        "password": "secret_sauce",
        "expected_error": "Epic sadface: Sorry, this user has been locked out.",
        "error_contains": "locked out"  # Substring to verify in error message
    },
    {
        "case": "special_char_user",
        "username": "!@#$%^",         # Username with special characters
        "password": "secret_sauce",
        "expected_error": "Epic sadface: Username and password do not match any user in this service"
    },
    {
        "case": "valid_user",         # Valid login test case
        "username": "standard_user",  # Standard valid user
        "password": "secret_sauce",
        "expected_error": None,       # No error expected for valid login
        "should_succeed": True        # Flag indicating this is a success case
    }
]

# ============================
# USER ACCOUNT DATA
# All available user accounts for testing
# ============================
USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked": {"username": "locked_out_user", "password": "secret_sauce", "should_fail": True},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance": {"username": "performance_glitch_user", "password": "secret_sauce"},
    "error": {"username": "error_user", "password": "secret_sauce"},
    "visual": {"username": "visual_user", "password": "secret_sauce"}
}

# ============================
# PRODUCT DATA
# Expected products and their details on the inventory page
# ============================
EXPECTED_PRODUCTS = [
    {"name": "Sauce Labs Backpack", "price": "$29.99"},
    {"name": "Sauce Labs Bike Light", "price": "$9.99"},
    {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"},
    {"name": "Sauce Labs Fleece Jacket", "price": "$49.99"},
    {"name": "Sauce Labs Onesie", "price": "$7.99"},
    {"name": "Test.allTheThings() T-Shirt (Red)", "price": "$15.99"}
]

# ============================
# PRODUCT REFERENCE DICTIONARY
# Easily reference specific products by key name
# ============================
PRODUCTS = {
    "backpack": {"name": "Sauce Labs Backpack", "price": "$29.99"},
    "bike_light": {"name": "Sauce Labs Bike Light", "price": "$9.99"},
    "bolt_tshirt": {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"},
    "fleece_jacket": {"name": "Sauce Labs Fleece Jacket", "price": "$49.99"},
    "onesie": {"name": "Sauce Labs Onesie", "price": "$7.99"},
    "red_tshirt": {"name": "Test.allTheThings() T-Shirt (Red)", "price": "$15.99"}
}

# ============================
# TEST SELECTION CONFIGURATION
# ============================
NAVIGATION_TEST_PRODUCT = "backpack"   # Default product for navigation tests
DEFAULT_PRODUCT_COUNT = 6              # Default expected product count

# ============================
# PAGE TITLES
# Expected page titles for verification
# ============================
PAGE_TITLES = {
    "login": "Swag Labs",
    "inventory": "Swag Labs",
    "product_detail": "Swag Labs"
}

# ============================
# ERROR MESSAGE PATTERNS
# Substrings to look for in error messages
# ============================
ERROR_PATTERNS = {
    "locked_out": "locked out",
    "username_required": "username is required",
    "password_required": "password is required",
    "no_match": "do not match any user"
}

# ============================
# WEB ELEMENT SELECTORS/LOCATORS
# CSS selectors and element identifiers for page interaction
# Organized by page/component for easy maintenance
# ============================
SELECTORS = {
    # Login page elements
    "login_page": {
        "username_field": "user-name",              # Username input field ID
        "password_field": "password",               # Password input field ID
        "login_button": "login-button",             # Login button ID
        "error_message": "[data-test='error']",     # Error message container
        "error_close_button": "error-button"        # Error close button
    },
    
    # Inventory page elements
    "inventory_page": {
        "product_items": "inventory_item",          # Product item container
        "product_name": "inventory_item_name",      # Product name element
        "product_price": "inventory_item_price",    # Product price element
        "product_image": ".inventory_item_img img", # Product image
        "add_to_cart_button": "button.btn_inventory",  # Add to cart button
        "shopping_cart_badge": "shopping_cart_badge"   # Cart item count badge
    },
    
    # Product detail page elements
    "product_detail_page": {
        "product_detail_name": "inventory_details_name",    # Product name on detail page
        "product_detail_price": "inventory_details_price",  # Product price on detail page
        "product_detail_image": ".inventory_details_img",   # Product image on detail page
        "back_button": "back-to-products"                   # Back to products button
    },
    
    # Common elements (appear on multiple pages)
    "common": {
        "title": "title",      # Page title element
        "header": ".header_container"  # Page header
    }
}

# ============================
# BROWSER CONFIGURATION
# Settings for WebDriver and browser options
# ============================
BROWSER_CONFIG = {
    "default_window_size": "1920,1080",  # Default browser window size
    "headless": True,                    # Run browser in headless mode
    "common_args": [                     # Common Chrome/Chromium arguments
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu"
    ],
    
    # Platform-specific configurations
    "platform_specific": {
        "linux": {
            "binary_location": "/usr/bin/chromium-browser",  # Chromium binary path on Linux
            "extra_args": ["--headless"]  # Additional args for Linux
        },
        "win32": {
            "binary_location": None,      # Use default Chrome on Windows
            "extra_args": ["--headless"]  # Additional args for Windows
        }
        
    }

}