"""
MODULAR PRODUCT TEST
Covers all inventory page verifications and product navigation in a single parameterized test.
"""

import pytest
import time
from functions import (
    get_all_products, verify_product_exists, click_product_by_name,
    get_product_details, go_back_to_products, is_on_inventory_page,
    take_screenshot
)
from data import PRODUCTS, EXPECTED_PRODUCTS, NAVIGATION_TEST_PRODUCT, DEFAULT_PRODUCT_COUNT, PAGE_PATTERNS, CONFIG, URLS


# Create test cases for all products
ALL_PRODUCTS_CASES = [
    {"key": key, "name": data["name"], "price": data["price"]}
    for key, data in PRODUCTS.items()
]

@pytest.mark.parametrize("product_case", ALL_PRODUCTS_CASES, ids=lambda x: x["key"])
def test_modular_product_workflow(logged_in_driver, product_case):
    """
    Modular test for product count, UI elements, and navigation.

    Steps for each product:
    1. Verify product exists in inventory
    2. Verify product UI elements (image, add button, link)
    3. Click product and verify detail page
    4. Verify product details match expected
    5. Return to inventory page
    """
    driver = logged_in_driver

    print(f"\n{'='*60}")
    print(f"TEST PRODUCT: {product_case['name']} ({product_case['key']})")
    print(f"{'='*60}")

    # Step 0: Ensure on inventory page
    if not is_on_inventory_page(driver):
        driver.get(URLS["inventory"])
        time.sleep(CONFIG["timeouts"]["medium_sleep"])

    # ============================
    # PHASE 1: PRODUCT PRESENCE
    # ============================
    products = get_all_products(driver)
    expected_count = CONFIG.get("product_count", DEFAULT_PRODUCT_COUNT)

    # Verify product count once (only for first product)
    if product_case == ALL_PRODUCTS_CASES[0]:
        actual_count = len(products)
        assert actual_count == expected_count, \
            f"Product count mismatch. Expected {expected_count}, found {actual_count}"
        print(f"✅ Product count correct: {actual_count} products")

    # Verify product exists
    found = verify_product_exists(driver, product_case["name"], product_case["price"])
    assert found, f"Product not found: {product_case['name']} - {product_case['price']}"
    print(f"✅ Product presence verified: {product_case['name']}")

    # ============================
    # PHASE 2: UI ELEMENTS
    # ============================
    # Locate the product element
    product_element = next((p for p in products if p['name'] == product_case["name"]), None)
    assert product_element, f"Product element not found: {product_case['name']}"

    # Image
    assert product_element['image'].is_displayed() and product_element['image'].get_attribute('src'), \
        f"Product image missing or not visible: {product_case['name']}"
    # Add to cart button
    assert product_element['add_button'].is_displayed() and product_element['add_button'].is_enabled(), \
        f"Add to Cart button missing or disabled: {product_case['name']}"
    # Name link
    assert product_element['name_link'].is_displayed() and product_element['name_link'].is_enabled(), \
        f"Product name link missing or disabled: {product_case['name']}"

    print(f"✅ UI elements verified for product: {product_case['name']}")

    # ============================
    # PHASE 3: NAVIGATION & DETAIL
    # ============================
    clicked = click_product_by_name(driver, product_case["name"])
    assert clicked, f"Failed to click product: {product_case['name']}"

    time.sleep(CONFIG["timeouts"]["long_sleep"])

    is_detail_page = any(
        pattern in driver.current_url 
        for pattern in PAGE_PATTERNS["product_detail_page"]
    )
    assert is_detail_page, f"Not on product detail page: {product_case['name']}"
    print(f"✅ Navigated to detail page for: {product_case['name']}")

    # Verify product details
    details = get_product_details(driver)
    assert details, f"Product details not found: {product_case['name']}"
    assert details["name"] == product_case["name"], \
        f"Name mismatch. Expected {product_case['name']}, got {details['name']}"
    assert details["price"] == product_case["price"], \
        f"Price mismatch. Expected {product_case['price']}, got {details['price']}"
    print(f"✅ Product details verified: {details['name']} - {details['price']}")

    take_screenshot(driver, f"product_{product_case['key']}", "PASS")

    # Return to inventory
    back_success = go_back_to_products(driver)
    assert back_success and is_on_inventory_page(driver), \
        f"Failed to return to inventory page from product: {product_case['name']}"
    print(f"✅ Returned to inventory page successfully")

    print(f"✅ TEST COMPLETE: {product_case['name']}")
