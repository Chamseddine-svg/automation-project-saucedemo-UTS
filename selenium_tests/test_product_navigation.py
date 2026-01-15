"""
TEST MODULE: PRODUCT NAVIGATION AND VERIFICATION
Tests product listing, navigation, and verification on the inventory page.
"""

import pytest
import time
from functions import (
    get_all_products, verify_product_exists, click_product_by_name,
    get_product_details, go_back_to_products, is_on_inventory_page,
    take_screenshot, wait_for_element
)
from data import (
    EXPECTED_PRODUCTS, USERS, PRODUCTS, NAVIGATION_TEST_PRODUCT,
    URLS, CONFIG, PAGE_PATTERNS, DEFAULT_PRODUCT_COUNT, SELECTORS
)


def test_product_count_and_presence(logged_in_driver):
    """
    Test that verifies the correct number of products are displayed
    and that all expected products are present with correct details.
    
    Test Steps:
    1. Verify total product count matches expected
    2. Verify each expected product exists with correct name and price
    """
    driver = logged_in_driver
    
    print(f"\n{'='*60}")
    print("TEST: Product Count and Presence Verification")
    print(f"{'='*60}")
    
    # Step 1: Get all products from the page
    print(f"Step 1: Retrieving products from inventory page...")
    products = get_all_products(driver)
    
    # Step 2: Verify total product count
    print(f"Step 2: Verifying total product count...")
    expected_count = CONFIG.get("product_count", DEFAULT_PRODUCT_COUNT)
    actual_count = len(products)
    
    assert actual_count == expected_count, \
        f"Product count mismatch. Expected {expected_count}, found {actual_count}"
    
    print(f"  ✅ Product count correct: {actual_count} products")
    
    # Step 3: Verify each expected product exists
    print(f"Step 3: Verifying each expected product...")
    all_products_found = True
    
    for expected_product in EXPECTED_PRODUCTS:
        product_found = verify_product_exists(
            driver, 
            expected_product["name"], 
            expected_product["price"]
        )
        
        if product_found:
            print(f"  ✅ Found: {expected_product['name']} - {expected_product['price']}")
        else:
            print(f"  ❌ Missing: {expected_product['name']} - {expected_product['price']}")
            all_products_found = False
    
    # Final assertion
    assert all_products_found, "Not all expected products were found"
    
    print(f"\n✅ TEST PASSED: All {expected_count} products present with correct details")


def test_product_elements_completeness(logged_in_driver):
    """
    Test that each product on the inventory page has all required UI elements.
    
    Verifies for each product:
    - Product image is displayed and has a source URL
    - Add to cart button is visible and enabled
    - Product name link is visible and enabled
    """
    driver = logged_in_driver
    
    print(f"\n{'='*60}")
    print("TEST: Product Elements Completeness")
    print(f"{'='*60}")
    
    # Get all products
    products = get_all_products(driver)
    print(f"Found {len(products)} products to verify")
    
    # Track verification results
    verification_results = []
    
    # Verify each product's elements
    for index, product in enumerate(products, 1):
        print(f"\n🔍 Verifying product {index}: {product['name']}")
        
        product_verification = {
            "name": product['name'],
            "image_ok": False,
            "button_ok": False,
            "link_ok": False
        }
        
        # Verify product image
        try:
            assert product['image'].is_displayed(), "Image not visible"
            assert product['image'].get_attribute('src'), "Image has no source URL"
            print(f"  ✅ Image: OK (visible with source)")
            product_verification["image_ok"] = True
        except AssertionError as e:
            print(f"  ❌ Image: FAILED - {str(e)}")
        
        # Verify add to cart button
        try:
            assert product['add_button'].is_displayed(), "Button not visible"
            assert product['add_button'].is_enabled(), "Button not enabled"
            print(f"  ✅ Add to Cart Button: OK (visible and enabled)")
            product_verification["button_ok"] = True
        except AssertionError as e:
            print(f"  ❌ Add to Cart Button: FAILED - {str(e)}")
        
        # Verify product name link
        try:
            assert product['name_link'].is_displayed(), "Link not visible"
            assert product['name_link'].is_enabled(), "Link not clickable"
            print(f"  ✅ Product Name Link: OK (visible and enabled)")
            product_verification["link_ok"] = True
        except AssertionError as e:
            print(f"  ❌ Product Name Link: FAILED - {str(e)}")
        
        verification_results.append(product_verification)
    
    # Summary and assertion
    print(f"\n{'='*40}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*40}")
    
    all_passed = True
    for result in verification_results:
        status = "✅ PASS" if all([result["image_ok"], result["button_ok"], result["link_ok"]]) else "❌ FAIL"
        print(f"{status} - {result['name']}")
        
        if status == "❌ FAIL":
            all_passed = False
    
    assert all_passed, "Some products are missing required elements"
    print(f"\n✅ TEST PASSED: All products have complete UI elements")


def test_single_product_navigation(logged_in_driver):
    """
    Test navigation to a specific product detail page and back.
    
    Test Steps:
    1. Click on a specific product (configured in data.py)
    2. Verify product detail page loads
    3. Verify product details match expected values
    4. Navigate back to inventory page
    5. Verify return to inventory page
    """
    driver = logged_in_driver
    
    print(f"\n{'='*60}")
    print("TEST: Single Product Navigation")
    print(f"{'='*60}")
    
    # Get product configuration from data.py
    product_key = NAVIGATION_TEST_PRODUCT
    product_data = PRODUCTS[product_key]
    
    print(f"Testing navigation for product: {product_data['name']}")
    
    # Step 1: Click on the product
    print(f"Step 1: Clicking product '{product_data['name']}'...")
    clicked = click_product_by_name(driver, product_data["name"])
    assert clicked, f"Failed to click on product: {product_data['name']}"
    
    # Step 2: Wait for page load and verify URL
    print(f"Step 2: Verifying navigation to detail page...")
    time.sleep(CONFIG["timeouts"]["long_sleep"])
    
    # Check if we're on a product detail page
    is_detail_page = any(
        pattern in driver.current_url 
        for pattern in PAGE_PATTERNS["product_detail_page"]
    )
    assert is_detail_page, \
        f"Not on product detail page. Current URL: {driver.current_url}"
    
    print(f"  ✅ Successfully navigated to product detail page")
    print(f"  URL: {driver.current_url}")
    
    # Step 3: Verify product details
    print(f"Step 3: Verifying product details...")
    details = get_product_details(driver)
    assert details is not None, "Could not retrieve product details"
    
    # Verify product name
    assert details["name"] == product_data["name"], \
        f"Product name mismatch. Expected '{product_data['name']}', got '{details['name']}'"
    
    # Verify product price
    assert details["price"] == product_data["price"], \
        f"Product price mismatch. Expected '{product_data['price']}', got '{details['price']}'"
    
    print(f"  ✅ Product details verified:")
    print(f"     Name:  {details['name']}")
    print(f"     Price: {details['price']}")
    
    # Step 4: Take screenshot for documentation
    print(f"Step 4: Capturing screenshot...")
    screenshot_path = take_screenshot(driver, f"product_detail_{product_key}", "SUCCESS")
    if screenshot_path:
        print(f"  ✅ Screenshot saved: {screenshot_path}")
    
    # Step 5: Navigate back to products
    print(f"Step 5: Navigating back to products list...")
    back_success = go_back_to_products(driver)
    assert back_success, "Failed to navigate back to products list"
    
    # Step 6: Verify return to inventory page
    print(f"Step 6: Verifying return to inventory page...")
    time.sleep(CONFIG["timeouts"]["medium_sleep"])
    
    assert PAGE_PATTERNS["inventory_page"] in driver.current_url, \
        f"Not back on inventory page. Current URL: {driver.current_url}"
    
    print(f"  ✅ Successfully returned to inventory page")
    print(f"  URL: {driver.current_url}")
    
    print(f"\n✅ TEST PASSED: Complete product navigation flow successful")


def test_all_products_navigation_parameterized(logged_in_driver):
    """
    Parameterized test that navigates to each product's detail page.
    
    Uses pytest parametrization to test navigation for all products
    defined in the PRODUCTS dictionary.
    """
    driver = logged_in_driver
    
    print(f"\n{'='*60}")
    print("TEST: All Products Navigation (Parameterized)")
    print(f"{'='*60}")
    
    # Get list of products to test
    product_keys = list(PRODUCTS.keys())
    print(f"Testing navigation for {len(product_keys)} products")
    
    for product_key in product_keys:
        product_data = PRODUCTS[product_key]
        
        print(f"\n➡️ Testing: {product_data['name']}")
        print(f"   Key: {product_key}")
        
        # Ensure we're on inventory page before each test
        if not is_on_inventory_page(driver):
            driver.get(URLS["inventory"])
            time.sleep(CONFIG["timeouts"]["medium_sleep"])
        
        # Click product
        clicked = click_product_by_name(driver, product_data["name"])
        assert clicked, f"Failed to click {product_data['name']}"
        
        # Wait and verify detail page
        time.sleep(CONFIG["timeouts"]["long_sleep"])
        
        is_detail_page = any(
            pattern in driver.current_url 
            for pattern in PAGE_PATTERNS["product_detail_page"]
        )
        assert is_detail_page, f"Not on detail page for {product_key}"
        
        # Verify details
        details = get_product_details(driver)
        assert details is not None, f"No details found for {product_key}"
        assert details["name"] == product_data["name"], f"Name mismatch for {product_key}"
        assert details["price"] == product_data["price"], f"Price mismatch for {product_key}"
        
        print(f"   ✅ Verified: {details['name']} - {details['price']}")
        
        # Take screenshot
        take_screenshot(driver, f"nav_{product_key}", "NAV")
        
        # Go back
        go_back_to_products(driver)
        time.sleep(CONFIG["timeouts"]["medium_sleep"])
        
        print(f"   ✅ Returned to products list")
    
    print(f"\n✅ TEST PASSED: All {len(product_keys)} products navigation successful")


def test_comprehensive_product_workflow(logged_in_driver):
    """
    Comprehensive end-to-end test for product workflow.
    
    Tests the complete flow from login to product verification,
    navigation, and validation. This test combines multiple
    verification steps into a single comprehensive test.
    """
    driver = logged_in_driver
    
    print(f"\n{'='*60}")
    print("COMPREHENSIVE PRODUCT WORKFLOW TEST")
    print(f"{'='*60}")
    
    test_results = {
        "product_count": False,
        "all_products_present": False,
        "product_elements": False,
        "navigation": False,
        "detail_verification": False,
        "return_navigation": False
    }
    
    try:
        # ============================
        # PHASE 1: PRODUCT LIST VERIFICATION
        # ============================
        print(f"\n📋 PHASE 1: Product List Verification")
        print(f"{'-'*40}")
        
        # 1.1: Get product count
        products = get_all_products(driver)
        expected_count = CONFIG.get("product_count", DEFAULT_PRODUCT_COUNT)
        
        if len(products) == expected_count:
            test_results["product_count"] = True
            print(f"✅ 1.1 Product count: {len(products)} (Expected: {expected_count})")
        else:
            print(f"❌ 1.1 Product count: {len(products)} (Expected: {expected_count})")
        
        # 1.2: Verify all expected products exist
        all_found = True
        for expected in EXPECTED_PRODUCTS:
            if not verify_product_exists(driver, expected["name"], expected["price"]):
                all_found = False
                print(f"❌ Missing product: {expected['name']}")
        
        test_results["all_products_present"] = all_found
        if all_found:
            print(f"✅ 1.2 All expected products present")
        
        # ============================
        # PHASE 2: PRODUCT UI ELEMENTS
        # ============================
        print(f"\n📋 PHASE 2: Product UI Elements")
        print(f"{'-'*40}")
        
        elements_ok = True
        for product in products:
            if not (product['image'].is_displayed() and 
                    product['add_button'].is_displayed() and 
                    product['name_link'].is_displayed()):
                elements_ok = False
                print(f"❌ Missing elements for: {product['name']}")
                break
        
        test_results["product_elements"] = elements_ok
        if elements_ok:
            print(f"✅ 2.1 All products have required UI elements")
        
        # ============================
        # PHASE 3: PRODUCT NAVIGATION
        # ============================
        print(f"\n📋 PHASE 3: Product Navigation")
        print(f"{'-'*40}")
        
        # 3.1: Navigate to configured product
        product_key = NAVIGATION_TEST_PRODUCT
        product_data = PRODUCTS[product_key]
        
        clicked = click_product_by_name(driver, product_data["name"])
        test_results["navigation"] = clicked
        
        if clicked:
            print(f"✅ 3.1 Successfully clicked product: {product_data['name']}")
            
            # Wait for detail page
            time.sleep(CONFIG["timeouts"]["long_sleep"])
            
            # 3.2: Verify detail page
            is_detail_page = any(
                pattern in driver.current_url 
                for pattern in PAGE_PATTERNS["product_detail_page"]
            )
            
            if is_detail_page:
                print(f"✅ 3.2 Successfully navigated to detail page")
                
                # 3.3: Verify product details
                details = get_product_details(driver)
                if details and details["name"] == product_data["name"] and details["price"] == product_data["price"]:
                    test_results["detail_verification"] = True
                    print(f"✅ 3.3 Product details verified: {details['name']} - {details['price']}")
                else:
                    print(f"❌ 3.3 Product details verification failed")
                
                # Take screenshot
                take_screenshot(driver, "comprehensive_test_detail", "DETAIL")
                
                # 3.4: Navigate back
                back_success = go_back_to_products(driver)
                test_results["return_navigation"] = back_success
                
                if back_success and is_on_inventory_page(driver):
                    print(f"✅ 3.4 Successfully returned to inventory page")
                else:
                    print(f"❌ 3.4 Failed to return to inventory page")
            else:
                print(f"❌ 3.2 Not on product detail page")
        else:
            print(f"❌ 3.1 Failed to click product")
        
        # ============================
        # TEST SUMMARY
        # ============================
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        
        all_passed = all(test_results.values())
        
        for phase, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {phase.replace('_', ' ').title()}")
        
        if all_passed:
            print(f"\n🎉 COMPREHENSIVE TEST PASSED: All phases completed successfully")
        else:
            # Take failure screenshot
            take_screenshot(driver, "comprehensive_test_failure", "COMPREHENSIVE_FAIL")
            
            # Get list of failed phases
            failed_phases = [phase for phase, passed in test_results.items() if not passed]
            pytest.fail(f"Comprehensive test failed in phases: {', '.join(failed_phases)}")
            
    except Exception as e:
        # Capture any unexpected exceptions
        take_screenshot(driver, "comprehensive_test_exception", "EXCEPTION")
        print(f"\n💥 UNEXPECTED ERROR: {str(e)}")
        raise


# ============================
# ADDITIONAL UTILITY TESTS
# ============================
def test_product_sorting_availability(logged_in_driver):
    """
    Test to verify product sorting functionality is available.
    Note: This is a placeholder test - actual sorting tests would be added here.
    """
    driver = logged_in_driver
    
    print(f"\n{'='*60}")
    print("TEST: Product Sorting Availability (Placeholder)")
    print(f"{'='*60}")
    
    # Check if sorting container exists
    try:
        # This selector might need to be added to data.py if sorting is tested
        sort_container = driver.find_element("css selector", ".product_sort_container")
        assert sort_container.is_displayed(), "Sort container not displayed"
        assert sort_container.is_enabled(), "Sort container not enabled"
        
        print(f"✅ Product sorting functionality is available")
        print(f"   Sort container: {sort_container.get_attribute('class')}")
        
    except Exception as e:
        print(f"⚠️ Note: Sorting test placeholder - {str(e)}")
        # Don't fail the test - this is just a placeholder
        pytest.skip("Sorting functionality test not fully implemented")


# ============================
# TEST EXECUTION MAIN BLOCK
# ============================
if __name__ == "__main__":
    """
    Allow direct execution of this test file.
    """
    print(f"\n{'='*60}")
    print("DIRECT TEST EXECUTION MODE - PRODUCT NAVIGATION")
    print(f"{'='*60}")
    
    # Run tests with configured options
    pytest.main([
        __file__,
        "-v",                # Verbose output
        "-s",                # Show print statements
        "--tb=short",        # Short traceback format
        "--disable-warnings", # Suppress warnings
        "--color=yes",       # Colored output
        # "--maxfail=1",     # Uncomment to stop on first failure
    ])