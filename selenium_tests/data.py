"""
MODULAR TEST CONFIGURATION
Centralized configuration and test data for modular login and product tests.
"""

# ============================
# TEST CONFIGURATION SETTINGS
# ============================
CONFIG = {
    "timeouts": {
        "implicit_wait": 5,
        "explicit_wait_short": 3,
        "explicit_wait_medium": 5,
        "explicit_wait_long": 10,
        "short_sleep": 0.5,
        "medium_sleep": 1,
        "long_sleep": 2,
    },
    "product_count": 6,               # Expected number of products
    "screenshot_dir": "screenshots",  # Screenshot save directory
}

# ============================
# APPLICATION URLS
# ============================
URLS = {
    "login": "https://www.saucedemo.com/",
    "inventory": "https://www.saucedemo.com/inventory.html",
}

# ============================
# PAGE PATTERNS
# ============================
PAGE_PATTERNS = {
    "inventory_page": "/inventory.html",
    "product_detail_page": ["inventory-item.html", "?id="],
}

# ============================
# LOGIN TEST DATA
# ============================
LOGIN_ERRORS = [
    {"case": "empty_username", "username": "", "password": "secret_sauce", 
     "expected_error": "Epic sadface: Username is required"},
    {"case": "empty_password", "username": "standard_user", "password": "", 
     "expected_error": "Epic sadface: Password is required"},
    {"case": "invalid_user", "username": "wrong_user", "password": "wrong_pass", 
     "expected_error": "Epic sadface: Username and password do not match any user in this service"},
    {"case": "locked_out_user", "username": "locked_out_user", "password": "secret_sauce",
     "expected_error": "Epic sadface: Sorry, this user has been locked out.", "error_contains": "locked out"},
    {"case": "special_char_user", "username": "!@#$%^", "password": "secret_sauce",
     "expected_error": "Epic sadface: Username and password do not match any user in this service"},
    {"case": "valid_user", "username": "standard_user", "password": "secret_sauce",
     "expected_error": None, "should_succeed": True},
]
# ============================
# BROWSER CONFIGURATION
# ============================
BROWSER_CONFIG = {
    "default_window_size": "1920,1080",
    "headless": True,
    "common_args": [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu"
    ],
    "platform_specific": {
        "linux": {
            "binary_location": "/usr/bin/chromium-browser",
            "extra_args": ["--headless"]
        },
        "win32": {
            "binary_location": None,
            "extra_args": ["--headless"]
        }
    }
}


# ============================
# USERS
# ============================
USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked": {"username": "locked_out_user", "password": "secret_sauce", "should_fail": True},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance": {"username": "performance_glitch_user", "password": "secret_sauce"},
}

# ============================
# ERROR PATTERNS
# ============================
ERROR_PATTERNS = {
    "locked_out": "locked out",
    "username_required": "username is required",
    "password_required": "password is required",
    "no_match": "do not match any user",
}

# ============================
# PRODUCTS
# Keyed dictionary for product data
# ============================
PRODUCTS = {
    "backpack": {"name": "Sauce Labs Backpack", "price": "$29.99"},
    "bike_light": {"name": "Sauce Labs Bike Light", "price": "$9.99"},
    "bolt_tshirt": {"name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"},
    "fleece_jacket": {"name": "Sauce Labs Fleece Jacket", "price": "$49.99"},
    "onesie": {"name": "Sauce Labs Onesie", "price": "$7.99"},
    "red_tshirt": {"name": "Test.allTheThings() T-Shirt (Red)", "price": "$15.99"},
}

# ============================
# EXPECTED PRODUCTS
# List for verification of inventory page
# ============================
EXPECTED_PRODUCTS = [{"name": p["name"], "price": p["price"]} for p in PRODUCTS.values()]

# ============================
# NAVIGATION TEST PRODUCT
# Default product for navigation test
# ============================
NAVIGATION_TEST_PRODUCT = "backpack"

# ============================
# DEFAULT PRODUCT COUNT
# ============================
DEFAULT_PRODUCT_COUNT = len(PRODUCTS)

# ============================
# PAGE TITLES
# ============================
PAGE_TITLES = {
    "login": "Swag Labs",
    "inventory": "Swag Labs",
    "product_detail": "Swag Labs",
}

# ============================
# SELECTORS (element locators)
# ============================
SELECTORS = {
    "login_page": {
        "username_field": "user-name",
        "password_field": "password",
        "login_button": "login-button",
        "error_message": "[data-test='error']",
        "error_close_button": "error-button",
    },
    "inventory_page": {
        "product_items": "inventory_item",
        "product_name": "inventory_item_name",
        "product_price": "inventory_item_price",
        "product_image": ".inventory_item_img img",
        "add_to_cart_button": "button.btn_inventory",
    },
    "product_detail_page": {
        "product_detail_name": "inventory_details_name",
        "product_detail_price": "inventory_details_price",
        "product_detail_image": ".inventory_details_img",
        "back_button": "back-to-products",
    },
}
