"""
MODULAR LOGIN TEST
Covers all login scenarios (valid, invalid, locked users) in a single parameterized test.
"""

import pytest
import time
from functions import login, get_error_message, close_error_message, is_logged_in, take_screenshot
from data import URLS, USERS, LOGIN_ERRORS, ERROR_PATTERNS, PAGE_PATTERNS, CONFIG

# Combine all test cases: LOGIN_ERRORS + USERS info for success/failure
ALL_TEST_CASES = []

# Add login error scenarios
for case in LOGIN_ERRORS:
    ALL_TEST_CASES.append({
        "case": case["case"],
        "username": case["username"],
        "password": case["password"],
        "expected_error": case.get("expected_error"),
        "should_succeed": case.get("should_succeed", False)
    })

# Add user type scenarios from USERS dictionary
for user_type, credentials in USERS.items():
    ALL_TEST_CASES.append({
        "case": f"user_{user_type}",
        "username": credentials["username"],
        "password": credentials["password"],
        "expected_error": ERROR_PATTERNS.get("locked_out") if user_type == "locked" else None,
        "should_succeed": not (credentials.get("should_fail", False) or user_type == "locked")
    })


@pytest.mark.parametrize("test_case", ALL_TEST_CASES, ids=lambda tc: tc["case"])
def test_login_modular(driver, test_case):
    """
    Modular login test covering:
    - Standard/other users
    - Locked users
    - Invalid credentials
    """
    print(f"\n{'='*60}")
    print(f"TEST SCENARIO: {test_case['case']}")
    print(f"{'='*60}")

    # Navigate to login page
    driver.get(URLS["login"])
    close_error_message(driver)
    
    # Attempt login
    login(driver, test_case["username"], test_case["password"])
    time.sleep(CONFIG["timeouts"]["medium_sleep"])
    
    # Capture results
    error_text = get_error_message(driver)
    logged_in = is_logged_in(driver, timeout=CONFIG["timeouts"]["explicit_wait_short"])
    current_url = driver.current_url
    
    failures = []

    if test_case["should_succeed"]:
        # Successful login checks
        if error_text:
            failures.append(f"Unexpected error for valid user: '{error_text}'")
        if not logged_in:
            failures.append(f"User should be logged in, but URL is: {current_url}")
        if PAGE_PATTERNS["inventory_page"] not in current_url:
            failures.append(f"Should redirect to inventory page, got: {current_url}")
        if not failures:
            print(f"✅ SUCCESS: User logged in correctly - {current_url}")
    else:
        # Error scenario checks
        if error_text is None:
            failures.append(f"Error message expected but not shown for {test_case['case']}")
        elif test_case["expected_error"] and test_case["expected_error"] not in error_text:
            failures.append(f"Expected error: '{test_case['expected_error']}', got: '{error_text}'")
        if logged_in:
            failures.append(f"User should not be logged in, but URL is: {current_url}")
        if not failures:
            print(f"✅ SUCCESS: Error handled correctly - '{error_text}'")
            # Optional: test closing error
            if close_error_message(driver):
                time.sleep(CONFIG["timeouts"]["short_sleep"])
                error_after_close = get_error_message(driver)
                if error_after_close is None:
                    print(f"   ✅ Error message closed successfully")
    
    # Handle failures
    if failures:
        take_screenshot(driver, f"{test_case['case']}", "FAIL")
        pytest.fail(f"Test case '{test_case['case']}' failed: {'; '.join(failures)}")
    
    print(f"✅ SCENARIO COMPLETE: {test_case['case']}")
