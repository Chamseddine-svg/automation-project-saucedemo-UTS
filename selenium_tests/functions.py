"""
REUSABLE UTILITY FUNCTIONS FOR WEB AUTOMATION
This module contains all shared functions for test automation.
Functions are designed to be generic, reusable, and maintainable.
"""

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import configuration from data module
from data import CONFIG, SELECTORS, PAGE_PATTERNS


def login(driver, username, password):
    """
    Perform login action on the Sauce Demo login page.
    
    Args:
        driver: WebDriver instance
        username (str): Username to enter
        password (str): Password to enter
    
    Returns:
        None
    """
    # Get selectors for login page
    selectors = SELECTORS["login_page"]
    
    # Clear and enter username
    driver.find_element(By.ID, selectors["username_field"]).clear()
    driver.find_element(By.ID, selectors["username_field"]).send_keys(username)
    
    # Clear and enter password
    driver.find_element(By.ID, selectors["password_field"]).clear()
    driver.find_element(By.ID, selectors["password_field"]).send_keys(password)
    
    # Click login button
    driver.find_element(By.ID, selectors["login_button"]).click()
    
    # Log action for debugging
    print(f"Login attempted with username: '{username}'")


def get_error_message(driver):
    """
    Retrieve error message text if present on the page.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        str: Error message text if found, None otherwise
    """
    try:
        # Wait for error message to be visible
        error_element = WebDriverWait(driver, CONFIG["timeouts"]["explicit_wait_short"]).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["login_page"]["error_message"]))
        )
        error_text = error_element.text.strip()
        print(f"Error message found: '{error_text}'")
        return error_text
    except TimeoutException:
        # No error message found within timeout period
        print("No error message found")
        return None


def close_error_message(driver):
    """
    Close error message by clicking the close button.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True if error was closed successfully, False otherwise
    """
    try:
        # Find and click the error close button
        driver.find_element(By.CLASS_NAME, SELECTORS["login_page"]["error_close_button"]).click()
        
        # Short pause to allow UI update
        time.sleep(CONFIG["timeouts"]["short_sleep"])
        
        print("Error message closed successfully")
        return True
    except NoSuchElementException:
        # Close button not found (error might not be present)
        print("Error close button not found")
        return False


def is_logged_in(driver, timeout=None):
    """
    Check if login was successful by verifying inventory page URL.
    
    Args:
        driver: WebDriver instance
        timeout (int, optional): Custom timeout in seconds
    
    Returns:
        bool: True if logged in (on inventory page), False otherwise
    """
    # Use configured timeout if not specified
    if timeout is None:
        timeout = CONFIG["timeouts"]["explicit_wait_long"]
    
    try:
        # Wait for URL to contain inventory page pattern
        WebDriverWait(driver, timeout).until(
            EC.url_contains(PAGE_PATTERNS["inventory_page"])
        )
        print("Login successful - on inventory page")
        return True
    except TimeoutException:
        # Not redirected to inventory page within timeout
        print("Login failed - not on inventory page")
        return False


def get_all_products(driver):
    """
    Retrieve all products from the inventory page.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        list: List of product dictionaries, each containing:
            - name: Product name
            - price: Product price
            - image: Product image WebElement
            - add_button: Add to cart button WebElement
            - name_link: Product name link WebElement
    """
    try:
        # Wait for products to load on the page
        WebDriverWait(driver, CONFIG["timeouts"]["explicit_wait_long"]).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, SELECTORS["inventory_page"]["product_items"]))
        )
        
        # Short pause to ensure all elements are fully loaded
        time.sleep(CONFIG["timeouts"]["short_sleep"])
        
        products = []
        selectors = SELECTORS["inventory_page"]
        
        # Find all product item containers
        items = driver.find_elements(By.CLASS_NAME, selectors["product_items"])
        print(f"Found {len(items)} product items")
        
        # Extract information from each product
        for index, item in enumerate(items, 1):
            try:
                product = {
                    'name': item.find_element(By.CLASS_NAME, selectors["product_name"]).text,
                    'price': item.find_element(By.CLASS_NAME, selectors["product_price"]).text,
                    'image': item.find_element(By.CSS_SELECTOR, selectors["product_image"]),
                    'add_button': item.find_element(By.CSS_SELECTOR, selectors["add_to_cart_button"]),
                    'name_link': item.find_element(By.CLASS_NAME, selectors["product_name"]),
                    'index': index  # Position in the list (1-based)
                }
                products.append(product)
                
                # Log each product found (debug level)
                # print(f"  Product {index}: {product['name']} - {product['price']}")
                
            except Exception as e:
                # Skip products that can't be parsed (log error for debugging)
                print(f"Warning: Could not parse product at index {index}: {str(e)}")
                continue
        
        return products
        
    except Exception as e:
        print(f"Error getting products: {str(e)}")
        return []  # Return empty list on failure


def verify_product_exists(driver, product_name, expected_price):
    """
    Verify if a specific product exists with the correct price.
    
    Args:
        driver: WebDriver instance
        product_name (str): Expected product name
        expected_price (str): Expected product price
    
    Returns:
        bool: True if product exists with correct price, False otherwise
    """
    products = get_all_products(driver)
    
    # Search for product with matching name and price
    for product in products:
        if product['name'] == product_name and product['price'] == expected_price:
            print(f"Product verified: {product_name} - {expected_price}")
            return True
    
    print(f"Product not found: {product_name} - {expected_price}")
    return False


def click_product_by_name(driver, product_name, retry_count=2):
    """
    Click on a product by its name. Includes retry logic for flaky clicks.
    
    Args:
        driver: WebDriver instance
        product_name (str): Name of the product to click
        retry_count (int): Number of retry attempts
    
    Returns:
        bool: True if click was successful, False otherwise
    """
    for attempt in range(1, retry_count + 1):
        print(f"Attempt {attempt}/{retry_count} to click product: {product_name}")
        
        products = get_all_products(driver)
        
        for product in products:
            if product['name'] == product_name:
                try:
                    # Try standard click first
                    product['name_link'].click()
                    
                    # Wait for page to respond
                    time.sleep(CONFIG["timeouts"]["medium_sleep"])
                    
                    print(f"Successfully clicked product: {product_name}")
                    return True
                    
                except Exception as e:
                    print(f"Standard click failed, trying JavaScript click: {str(e)}")
                    
                    try:
                        # Fall back to JavaScript click
                        driver.execute_script("arguments[0].click();", product['name_link'])
                        
                        # Wait for page to respond
                        time.sleep(CONFIG["timeouts"]["medium_sleep"])
                        
                        print(f"Successfully clicked product with JavaScript: {product_name}")
                        return True
                        
                    except Exception as js_error:
                        print(f"JavaScript click also failed: {str(js_error)}")
                        # Continue to next product or retry
    
    print(f"Failed to click product after {retry_count} attempts: {product_name}")
    return False


def get_product_details(driver):
    """
    Get product details from the product detail page.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        dict: Dictionary containing product name and price, None if not found
    """
    try:
        selectors = SELECTORS["product_detail_page"]
        
        # Extract product details from detail page
        name = driver.find_element(By.CLASS_NAME, selectors["product_detail_name"]).text
        price = driver.find_element(By.CLASS_NAME, selectors["product_detail_price"]).text
        
        print(f"Product details retrieved: {name} - {price}")
        return {"name": name, "price": price}
        
    except NoSuchElementException:
        print("Could not find product details on current page")
        return None


def go_back_to_products(driver):
    """
    Navigate back to products list from product detail page.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True if navigation successful, False otherwise
    """
    try:
        # Click the back button
        driver.find_element(By.ID, SELECTORS["product_detail_page"]["back_button"]).click()
        
        # Wait for navigation to complete
        time.sleep(CONFIG["timeouts"]["medium_sleep"])
        
        print("Successfully navigated back to products list")
        return True
        
    except NoSuchElementException:
        print("Back button not found")
        return False


def is_on_inventory_page(driver):
    """
    Check if currently on the inventory page.
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True if on inventory page, False otherwise
    """
    is_inventory = PAGE_PATTERNS["inventory_page"] in driver.current_url
    print(f"On inventory page: {is_inventory} (URL: {driver.current_url})")
    return is_inventory


def take_screenshot(driver, test_name, screenshot_type=""):
    """
    Take a screenshot and save it with a descriptive filename.
    
    Args:
        driver: WebDriver instance
        test_name (str): Name of the test (used in filename)
        screenshot_type (str): Type of screenshot (e.g., "fail", "success", "debug")
    
    Returns:
        str: Path to the saved screenshot, None if failed
    """
    try:
        # Create screenshots directory if it doesn't exist
        screenshot_dir = CONFIG["screenshot_dir"]
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            print(f"Created directory: {screenshot_dir}")
        
        # Clean test name for use in filename
        clean_name = test_name.replace("[", "_").replace("]", "_").replace("/", "_").replace("\\", "_")
        
        # Generate timestamp for unique filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Construct filename
        if screenshot_type:
            filename = f"{screenshot_dir}/{clean_name}_{screenshot_type}_{timestamp}.png"
        else:
            filename = f"{screenshot_dir}/{clean_name}_{timestamp}.png"
        
        # Take screenshot
        driver.save_screenshot(filename)
        
        # Verify file was created
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"Screenshot saved: {filename} ({file_size} bytes)")
            return filename
        else:
            print(f"Warning: Screenshot file not created: {filename}")
            return None
            
    except Exception as e:
        print(f"Error taking screenshot: {str(e)}")
        return None


def wait_for_element(driver, locator_type, locator_value, timeout=None):
    """
    Generic function to wait for an element to be present and visible.
    
    Args:
        driver: WebDriver instance
        locator_type (By): Selenium By locator type (By.ID, By.CLASS_NAME, etc.)
        locator_value (str): Locator value
        timeout (int, optional): Custom timeout in seconds
    
    Returns:
        WebElement: The found element, raises exception if not found
    """
    if timeout is None:
        timeout = CONFIG["timeouts"]["explicit_wait_short"]
    
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((locator_type, locator_value))
    )


def is_element_present(driver, locator_type, locator_value, timeout=None):
    """
    Check if an element is present on the page without throwing exception.
    
    Args:
        driver: WebDriver instance
        locator_type (By): Selenium By locator type
        locator_value (str): Locator value
        timeout (int, optional): Custom timeout in seconds
    
    Returns:
        bool: True if element is present, False otherwise
    """
    try:
        wait_for_element(driver, locator_type, locator_value, timeout)
        return True
    except TimeoutException:
        return False


def safe_find_element(driver, locator_type, locator_value, parent=None):
    """
    Safely find an element, returning None if not found instead of throwing exception.
    
    Args:
        driver: WebDriver instance
        locator_type (By): Selenium By locator type
        locator_value (str): Locator value
        parent (WebElement, optional): Parent element to search within
    
    Returns:
        WebElement: Found element or None if not found
    """
    try:
        if parent:
            return parent.find_element(locator_type, locator_value)
        else:
            return driver.find_element(locator_type, locator_value)
    except NoSuchElementException:
        return None


def refresh_page_and_wait(driver, wait_time=None):
    """
    Refresh the current page and wait for it to reload.
    
    Args:
        driver: WebDriver instance
        wait_time (int, optional): Time to wait after refresh
    
    Returns:
        None
    """
    if wait_time is None:
        wait_time = CONFIG["timeouts"]["page_load"]
    
    print("Refreshing page...")
    driver.refresh()
    time.sleep(wait_time)