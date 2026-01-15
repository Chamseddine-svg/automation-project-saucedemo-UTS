"""
TEST MODULE: LOGIN ERROR SCENARIOS
Tests various login scenarios including valid and invalid credentials.
Uses parameterized tests for data-driven testing approach.
"""

import pytest
import time
from functions import login, get_error_message, close_error_message, is_logged_in, take_screenshot
from data import LOGIN_ERRORS, USERS, URLS, CONFIG, ERROR_PATTERNS, PAGE_PATTERNS


def test_login_success_basic(driver):
    """
    Basic test for successful login with valid credentials.
    
    This test verifies that a standard user can successfully log in
    and is redirected to the inventory page.
    
    Test Steps:
    1. Navigate to login page
    2. Enter valid credentials
    3. Verify redirection to inventory page
    """
    print(f"\n{'='*60}")
    print("TEST: Basic Successful Login")
    print(f"{'='*60}")
    
    # Step 1: Navigate to login page
    driver.get(URLS["login"])
    print(f"Step 1: Navigated to login page")
    
    # Step 2: Login with valid credentials
    user_credentials = USERS["standard"]
    login(driver, user_credentials["username"], user_credentials["password"])
    print(f"Step 2: Attempted login with user: {user_credentials['username']}")
    
    # Step 3: Verify successful login
    time.sleep(CONFIG["timeouts"]["medium_sleep"])  # Allow page to load
    
    # Check if on inventory page
    is_success = PAGE_PATTERNS["inventory_page"] in driver.current_url
    assert is_success, f"Login failed. Expected inventory page, got: {driver.current_url}"
    
    print(f"Step 3: Login successful - Redirected to: {driver.current_url}")
    print(f"✅ TEST PASSED: Basic login successful")


@pytest.mark.parametrize("test_case", LOGIN_ERRORS, ids=lambda tc: tc["case"])
def test_login_scenarios(driver, test_case):
    """
    Comprehensive login scenario test using parameterized data.
    
    This test runs multiple login scenarios from the LOGIN_ERRORS data:
    - Invalid credentials (empty username, empty password, wrong credentials)
    - Locked out user
    - Special character username
    - Valid user (success case)
    
    Args:
        driver: WebDriver instance
        test_case: Dictionary containing test case data from LOGIN_ERRORS
    """
    print(f"\n{'='*60}")
    print(f"TESTING LOGIN SCENARIO: {test_case['case'].upper()}")
    print(f"{'='*60}")
    
    # Step 1: Navigate to login page
    driver.get(URLS["login"])
    print(f"Step 1: Navigated to login page")
    
    # Clear any existing error messages from previous tests
    close_error_message(driver)
    
    # Step 2: Attempt login with test case credentials
    login(driver, test_case["username"], test_case["password"])
    print(f"Step 2: Attempted login")
    print(f"  Username: '{test_case['username']}'")
    print(f"  Password: {'*' * len(test_case['password']) if test_case['password'] else '(empty)'}")
    
    # Step 3: Allow page to process login attempt
    time.sleep(CONFIG["timeouts"]["medium_sleep"])
    
    # Step 4: Get results
    current_url = driver.current_url
    error_text = get_error_message(driver)
    logged_in = is_logged_in(driver, timeout=CONFIG["timeouts"]["explicit_wait_short"])
    
    # Step 5: Validate results based on test case type
    is_success_case = test_case.get("should_succeed", False)
    failures = []  # Collect validation failures
    
    if is_success_case:
        # ============================
        # VALID USER TEST CASE
        # ============================
        print(f"Step 3: Validating successful login...")
        
        # Should not have error message
        if error_text is not None:
            failures.append(f"Valid user should not show error, but got: '{error_text}'")
        
        # Should be logged in
        if not logged_in:
            failures.append(f"Valid user should be logged in, but URL is: {current_url}")
        
        # Should be on inventory page
        if PAGE_PATTERNS["inventory_page"] not in current_url:
            failures.append(f"Should redirect to inventory page, but URL is: {current_url}")
        
        # Report results
        if not failures:
            print(f"  ✅ SUCCESS: Valid user logged in correctly")
            print(f"     URL: {current_url}")
        else:
            print(f"  ❌ FAILED: Valid user test")
            for fail in failures:
                print(f"     - {fail}")
    
    else:
        # ============================
        # ERROR CASE TEST SCENARIO
        # ============================
        print(f"Step 3: Validating error scenario...")
        
        # Should have error message
        if error_text is None:
            failures.append(f"Error message should appear for {test_case['case']}")
        
        # Error message should match expected
        elif error_text != test_case["expected_error"]:
            failures.append(f"Expected: '{test_case['expected_error']}', Got: '{error_text}'")
        
        # Should not be logged in
        if logged_in:
            failures.append(f"Error case should not be logged in, but URL is: {current_url}")
        
        # Report results
        if not failures:
            print(f"  ✅ SUCCESS: Error case handled correctly")
            print(f"     Error message: {error_text}")
            
            # Test closing the error message (optional verification)
            print(f"Step 4: Testing error message closure...")
            if close_error_message(driver):
                time.sleep(CONFIG["timeouts"]["short_sleep"])
                error_after_close = get_error_message(driver)
                if error_after_close is None:
                    print(f"     ✅ Error message closed successfully")
                else:
                    print(f"     ⚠️ Error message still present: '{error_after_close}'")
            else:
                print(f"     ⚠️ Could not close error message (button might not be present)")
        else:
            print(f"  ❌ FAILED: Error case validation")
            for fail in failures:
                print(f"     - {fail}")
    
    # Step 6: Handle test failures
    if failures:
        # Take screenshot for debugging
        take_screenshot(driver, f"login_{test_case['case']}", "FAIL")
        
        # Fail the test with all collected failure messages
        pytest.fail(f"Test case '{test_case['case']}' failed: {'; '.join(failures)}")
    
    print(f"✅ SCENARIO COMPLETE: {test_case['case']}")


def test_all_user_types_comprehensive(driver):
    """
    Comprehensive test for all user types defined in USERS dictionary.
    
    Tests each user account type and verifies expected behavior:
    - Standard user: Should login successfully
    - Locked user: Should show locked out error
    - Other users: Should login successfully
    
    This test provides a summary report of all user type tests.
    """
    print(f"\n{'='*60}")
    print("COMPREHENSIVE USER TYPE TESTING")
    print(f"{'='*60}")
    
    results = {}  # Store test results for summary
    
    # Test each user type
    for user_type, credentials in USERS.items():
        print(f"\n🔍 Testing user type: {user_type}")
        print(f"   Username: {credentials['username']}")
        
        # Navigate to login page
        driver.get(URLS["login"])
        time.sleep(CONFIG["timeouts"]["short_sleep"])
        
        # Clear any previous errors
        close_error_message(driver)
        
        # Attempt login
        login(driver, credentials["username"], credentials["password"])
        time.sleep(CONFIG["timeouts"]["medium_sleep"])
        
        # Get test results
        error_text = get_error_message(driver)
        logged_in = is_logged_in(driver, timeout=CONFIG["timeouts"]["explicit_wait_short"])
        
        # Determine expected behavior
        should_fail = credentials.get("should_fail", False) or user_type == "locked"
        
        if should_fail:
            # ============================
            # EXPECTED FAILURE (Locked user)
            # ============================
            expected_error_substring = ERROR_PATTERNS.get("locked_out", "locked out")
            
            if error_text and expected_error_substring in error_text.lower():
                results[user_type] = {"status": "PASS", "message": "Correctly locked out"}
                print(f"   ✅ PASS: Locked out as expected")
                print(f"      Error: {error_text}")
            else:
                results[user_type] = {"status": "FAIL", "message": "Should show locked out error"}
                print(f"   ❌ FAIL: Should be locked out")
                if error_text:
                    print(f"      Error: {error_text}")
                else:
                    print(f"      No error message displayed")
                
                # Capture screenshot for debugging
                take_screenshot(driver, f"user_{user_type}", "FAIL")
        
        else:
            # ============================
            # EXPECTED SUCCESS (Other users)
            # ============================
            if logged_in and error_text is None:
                results[user_type] = {"status": "PASS", "message": "Successfully logged in"}
                print(f"   ✅ PASS: Login successful")
                print(f"      URL: {driver.current_url}")
            else:
                results[user_type] = {"status": "FAIL", "message": "Should login successfully"}
                print(f"   ❌ FAIL: Login unsuccessful")
                if error_text:
                    print(f"      Error: {error_text}")
                print(f"      Logged in: {logged_in}")
                
                # Capture screenshot for debugging
                take_screenshot(driver, f"user_{user_type}", "FAIL")
    
    # ============================
    # TEST SUMMARY REPORT
    # ============================
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed_count = 0
    failed_count = 0
    
    for user_type, result in results.items():
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"{status_icon} {user_type:15} : {result['status']} - {result['message']}")
        
        if result["status"] == "PASS":
            passed_count += 1
        else:
            failed_count += 1
    
    print(f"\n📊 SUMMARY: {passed_count} passed, {failed_count} failed")
    
    # Fail the overall test if any user type failed
    if failed_count > 0:
        pytest.fail(f"{failed_count} user type(s) failed to login as expected")


def test_page_title_verification(driver):
    """
    Test to verify page title on login page.
    
    Simple test that ensures the application loads correctly
    with the expected page title.
    """
    print(f"\n{'='*60}")
    print("TEST: Page Title Verification")
    print(f"{'='*60}")
    
    # Navigate to login page
    driver.get(URLS["login"])
    print(f"Step 1: Navigated to login page")
    
    # Get page title
    actual_title = driver.title
    expected_title = "Swag Labs"
    
    print(f"Step 2: Verifying page title")
    print(f"  Expected title: '{expected_title}'")
    print(f"  Actual title:   '{actual_title}'")
    
    # Verify title
    assert actual_title == expected_title, \
        f"Page title mismatch. Expected '{expected_title}', got '{actual_title}'"
    
    print(f"✅ TEST PASSED: Page title is correct")


# ============================
# TEST EXECUTION MAIN BLOCK
# ============================
if __name__ == "__main__":
    """
    Allow direct execution of this test file.
    Run with: python test_login_errors.py
    """
    print(f"\n{'='*60}")
    print("DIRECT TEST EXECUTION MODE")
    print(f"{'='*60}")
    
    # Run tests with pytest
    pytest.main([
        __file__,           # This file
        "-v",               # Verbose output
        "-s",               # Show print statements
        "--tb=short",       # Short traceback format
        "--disable-warnings",  # Suppress warnings
        "--color=yes"       # Colored output
    ])