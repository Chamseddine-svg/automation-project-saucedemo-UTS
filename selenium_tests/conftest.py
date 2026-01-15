"""
PYTEST CONFIGURATION AND FIXTURES - CROSS-PLATFORM
This file provides shared fixtures and hooks for the test automation framework.
Designed to work seamlessly on both Linux and Windows platforms.

Key Features:
- Automatic platform detection and configuration
- WebDriver management with automatic driver installation
- Screenshot capture on test failures
- Proper test setup and teardown management
- Integration with configuration from data.py
"""

import pytest  # Pytest testing framework
import sys     # System-specific parameters and functions
import os      # Operating system interface
import time    # Time-related functions
from selenium import webdriver  # Web browser automation
from selenium.webdriver.chrome.options import Options  # Chrome browser options
from selenium.webdriver.chrome.service import Service  # ChromeDriver service management
from webdriver_manager.chrome import ChromeDriverManager  # Automatic ChromeDriver management
from webdriver_manager.core.os_manager import ChromeType  # Chrome type for different platforms

# Import project-specific modules
from data import CONFIG, BROWSER_CONFIG, URLS, USERS  # Configuration and test data
from functions import login, is_logged_in, take_screenshot  # Reusable utility functions


@pytest.fixture(scope="function")
def driver(request):
    """
    CROSS-PLATFORM WebDriver fixture for automated browser testing.
    
    This fixture provides a fully configured WebDriver instance that:
    1. Automatically detects the operating system (Linux/Windows)
    2. Configures browser options appropriately for each platform
    3. Manages ChromeDriver installation automatically
    4. Sets up proper timeouts and window size
    5. Captures screenshots on test failures
    6. Ensures proper cleanup after test execution
    
    Args:
        request: Pytest request object containing test context information
    
    Yields:
        WebDriver: Configured browser automation instance ready for testing
    
    Raises:
        Exception: If WebDriver cannot be initialized on the current platform
    
    Usage:
        def test_example(driver):
            driver.get("https://example.com")
            # Test code here
    """
    
    # ============================================
    # 1. INITIALIZATION AND PLATFORM DETECTION
    # ============================================
    
    # Extract test name for logging and screenshot purposes
    test_name = request.node.name
    
    # Detect current operating system platform
    # sys.platform returns:
    # - 'linux' for Linux systems
    # - 'win32' for Windows systems
    # - 'darwin' for macOS systems
    current_platform = sys.platform
    
    # Log platform information for debugging
    print(f"\n{'='*60}")
    print(f"🚀 SETTING UP WEBSERVER ON {current_platform.upper()}")
    print(f"Test: {test_name}")
    print(f"{'='*60}")
    
    # ============================================
    # 2. BROWSER OPTIONS CONFIGURATION
    # ============================================
    
    # Create Chrome/Chromium options object to configure browser behavior
    options = Options()
    
    # Access platform-specific configuration from data.py
    platform_config = BROWSER_CONFIG["platform_specific"]
    
    # Determine current platform and set appropriate flags
    is_linux = current_platform.startswith('linux')      # Check if running on Linux
    is_windows = current_platform.startswith('win32')    # Check if running on Windows
    
    # Variable to track Chrome type for webdriver-manager
    chrome_type = None
    
    if is_linux:
        # ============================================
        # LINUX-SPECIFIC CONFIGURATION
        # ============================================
        print("📌 Platform: Linux")
        print("   Browser: Chromium")
        
        # Get Linux-specific settings from configuration
        platform_settings = platform_config.get("linux", {})
        
        # Set Chromium binary location (default: /usr/bin/chromium-browser)
        binary_location = platform_settings.get("binary_location")
        if binary_location and os.path.exists(binary_location):
            options.binary_location = binary_location
            print(f"   Binary location: {binary_location}")
        else:
            print(f"   ⚠️  Using default Chromium binary")
        
        # Specify Chrome type as CHROMIUM for webdriver-manager
        chrome_type = ChromeType.CHROMIUM
        
        # Add Linux-specific command-line arguments
        for arg in platform_settings.get("extra_args", []):
            options.add_argument(arg)
            print(f"   Added argument: {arg}")
        
    elif is_windows:
        # ============================================
        # WINDOWS-SPECIFIC CONFIGURATION
        # ============================================
        print("📌 Platform: Windows")
        print("   Browser: Google Chrome")
        
        # Get Windows-specific settings from configuration
        platform_settings = platform_config.get("win32", {})
        
        # Set Chrome binary location if specified in configuration
        binary_location = platform_settings.get("binary_location")
        if binary_location and os.path.exists(binary_location):
            options.binary_location = binary_location
            print(f"   Binary location: {binary_location}")
        else:
            print(f"   ℹ️  Using system default Chrome installation")
        
        # Specify Chrome type as GOOGLE CHROME for webdriver-manager
        chrome_type = ChromeType.GOOGLE
        
        # Add Windows-specific command-line arguments
        for arg in platform_settings.get("extra_args", []):
            options.add_argument(arg)
            print(f"   Added argument: {arg}")
        
    else:
        # ============================================
        # UNSUPPORTED PLATFORM HANDLING
        # ============================================
        print(f"⚠️  WARNING: Unsupported platform detected: {current_platform}")
        print("   Attempting to use default Google Chrome settings")
        
        # Use empty settings as fallback
        platform_settings = {}
        
        # Default to Google Chrome type
        chrome_type = ChromeType.GOOGLE
    
    # ============================================
    # 3. COMMON BROWSER ARGUMENTS (ALL PLATFORMS)
    # ============================================
    
    # Add arguments common to all platforms (from data.py configuration)
    print("\n🔧 Applying common browser arguments:")
    for arg in BROWSER_CONFIG["common_args"]:
        options.add_argument(arg)
        print(f"   Added: {arg}")
    
    # Set browser window size for consistent viewport
    window_size = BROWSER_CONFIG["default_window_size"]
    options.add_argument(f"--window-size={window_size}")
    print(f"   Window size: {window_size}")
    
    # Disable browser logging to reduce console noise
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    print("   Disabled browser logging")
    
    # ============================================
    # 4. WEBDRIVER SETUP WITH AUTOMATIC MANAGEMENT
    # ============================================
    
    try:
        print("\n⚙️ Setting up WebDriver using webdriver-manager...")
        
        # ============================================
        # AUTOMATIC DRIVER MANAGEMENT (RECOMMENDED)
        # ============================================
        # webdriver-manager automatically:
        # 1. Checks for the correct ChromeDriver version
        # 2. Downloads it if not present
        # 3. Manages version compatibility
        # 4. Provides the correct path to the driver
        
        # Create a Service object with automatic driver management
        service = Service(ChromeDriverManager(chrome_type=chrome_type).install())
        
        # Initialize WebDriver with the service and options
        # This creates a new browser instance with our configuration
        driver = webdriver.Chrome(service=service, options=options)
        
        print("   ✅ WebDriver initialized successfully with automatic management")
        
    except Exception as e:
        # ============================================
        # FALLBACK: MANUAL DRIVER SETUP
        # ============================================
        # If automatic setup fails, try using system-installed ChromeDriver
        print(f"   ⚠️  Automatic driver setup failed: {str(e)}")
        print("   Attempting fallback to system ChromeDriver...")
        
        try:
            # Try initializing with system ChromeDriver
            # This assumes ChromeDriver is in PATH or default location
            driver = webdriver.Chrome(options=options)
            print("   ✅ Fallback successful: Using system ChromeDriver")
            
        except Exception as fallback_error:
            # ============================================
            # CRITICAL FAILURE: CANNOT INITIALIZE WEBDRIVER
            # ============================================
            print(f"   ❌ CRITICAL ERROR: Both automatic and fallback methods failed")
            print(f"   Error details: {str(fallback_error)}")
            print("\n💡 TROUBLESHOOTING STEPS:")
            print("   1. Ensure Chrome/Chromium is installed")
            print("   2. Check internet connection for driver download")
            print("   3. Verify ChromeDriver is in PATH (for fallback)")
            print("   4. Check firewall/antivirus settings")
            
            # Raise clear error message for the user
            raise Exception(
                f"Cannot initialize WebDriver on {current_platform}. "
                f"Please ensure Chrome/Chromium is installed and try again. "
                f"Error: {str(fallback_error)}"
            )
    
    # ============================================
    # 5. WEBDRIVER CONFIGURATION
    # ============================================
    
    # Set implicit wait - maximum time to wait for elements to appear
    # This applies globally to all find_element calls
    implicit_wait_time = CONFIG["timeouts"]["implicit_wait"]
    driver.implicitly_wait(implicit_wait_time)
    print(f"\n⏱️  Configured implicit wait: {implicit_wait_time} seconds")
    
    # Maximize browser window for consistent testing environment
    # Even in headless mode, this sets a consistent viewport size
    driver.maximize_window()
    print("   Browser window maximized")
    
    # ============================================
    # 6. BROWSER INFORMATION LOGGING
    # ============================================
    
    # Log browser capabilities for debugging and verification
    capabilities = driver.capabilities
    print(f"\n📊 Browser Information:")
    print(f"   Browser: {capabilities.get('browserName', 'Unknown')}")
    print(f"   Version: {capabilities.get('browserVersion', 'Unknown')}")
    print(f"   Platform: {capabilities.get('platformName', 'Unknown')}")
    
    # Log driver capabilities if available
    if 'chrome' in capabilities:
        chrome_info = capabilities['chrome']
        print(f"   Chromedriver: {chrome_info.get('chromedriverVersion', 'Unknown')}")
    
    print(f"\n✅ WEBSERVER SETUP COMPLETE FOR TEST: {test_name}")
    print(f"{'='*60}")
    
    # ============================================
    # 7. YIELD DRIVER TO TEST FUNCTION
    # ============================================
    # The yield statement provides the driver to the test function
    # Test execution happens here
    yield driver
    
    # ============================================
    # 8. TEARDOWN: POST-TEST CLEANUP
    # ============================================
    # Code after yield runs AFTER the test completes
    # This ensures proper cleanup even if the test fails
    
    print(f"\n{'='*60}")
    print(f"🧹 CLEANING UP AFTER TEST: {test_name}")
    print(f"{'='*60}")
    
    # Check if the test failed by examining the test report
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        print(f"❌ Test execution failed")
        
        # Capture screenshot for debugging failed tests
        screenshot_path = take_screenshot(driver, test_name, "FAIL")
        if screenshot_path:
            print(f"   📸 Failure screenshot saved: {screenshot_path}")
        
        # Log additional debugging information
        print(f"   🔍 Debug information:")
        print(f"      Final URL: {driver.current_url}")
        print(f"      Page title: {driver.title}")
        
        # Optional: Log page source size (for debugging complex failures)
        try:
            page_source_size = len(driver.page_source)
            print(f"      Page source size: {page_source_size:,} characters")
        except Exception:
            print(f"      ⚠️ Could not retrieve page source")
    
    else:
        print(f"✅ Test execution completed successfully")
    
    # ============================================
    # 9. BROWSER CLEANUP
    # ============================================
    
    print(f"\n🔄 Closing browser...")
    
    # Close the browser and terminate the WebDriver session
    # This frees system resources and ensures clean state for next test
    driver.quit()
    
    # Short pause to ensure clean termination
    time.sleep(0.5)
    
    print(f"✅ Browser closed successfully")
    print(f"🎯 TEST COMPLETE: {test_name}")
    print(f"{'='*60}\n")


# ============================================
# LOGGED-IN DRIVER FIXTURE
# ============================================
@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Pre-authenticated WebDriver fixture for tests requiring login state.
    
    This fixture extends the base driver fixture by automatically:
    1. Navigating to the login page
    2. Logging in with standard user credentials
    3. Verifying successful authentication
    4. Returning a ready-to-use logged-in driver
    
    This eliminates repetitive login code in tests that require authentication.
    
    Args:
        driver: WebDriver instance from the base driver fixture
    
    Returns:
        WebDriver: Authenticated WebDriver instance on the inventory page
    
    Raises:
        Exception: If login process fails with detailed error information
    """
    
    print(f"\n{'='*60}")
    print(f"🔐 CONFIGURING LOGGED-IN DRIVER")
    print(f"{'='*60}")
    
    # Step 1: Navigate to application login page
    print(f"Step 1: Navigating to login page...")
    driver.get(URLS["login"])
    print(f"   ✅ Navigated to: {URLS['login']}")
    
    # Step 2: Retrieve standard user credentials from configuration
    print(f"Step 2: Retrieving credentials...")
    user_credentials = USERS["standard"]
    username = user_credentials["username"]
    password = user_credentials["password"]
    
    # Mask password for security in logs (show only first and last character)
    masked_password = password[0] + "*" * (len(password) - 2) + password[-1] if len(password) > 1 else "***"
    print(f"   Username: {username}")
    print(f"   Password: {masked_password}")
    
    # Step 3: Execute login using reusable function
    print(f"Step 3: Attempting login...")
    login(driver, username, password)
    print(f"   ✅ Login attempt completed")
    
    # Step 4: Verify successful authentication
    print(f"Step 4: Verifying login success...")
    if is_logged_in(driver):
        print(f"   ✅ Authentication successful")
        print(f"   Current URL: {driver.current_url}")
        print(f"{'='*60}")
        print(f"🎉 LOGGED-IN DRIVER READY FOR USE")
        print(f"{'='*60}")
        
        # Return the authenticated driver to the test
        return driver
    else:
        # ============================================
        # LOGIN FAILURE HANDLING
        # ============================================
        print(f"   ❌ Authentication failed")
        
        # Capture screenshot for debugging login issues
        take_screenshot(driver, "login_fixture_failure", "AUTH_FAIL")
        
        # Gather detailed error information
        print(f"\n🔍 LOGIN FAILURE DIAGNOSTICS:")
        print(f"   Current URL: {driver.current_url}")
        print(f"   Page title: {driver.title}")
        
        # Attempt to extract error message if present
        try:
            # Look for error message element on page
            error_element = driver.find_element("css selector", "[data-test='error']")
            if error_element and error_element.text:
                print(f"   Error message: {error_element.text}")
            else:
                print(f"   No error message displayed")
        except Exception:
            print(f"   ⚠️ Could not find error message element")
        
        print(f"{'='*60}")
        
        # Raise informative exception with troubleshooting guidance
        raise Exception(
            f"Login fixture failed for user '{username}'. "
            f"The application did not redirect to the inventory page. "
            f"Current location: {driver.current_url}. "
            f"Check credentials and application status."
        )


# ============================================
# PYTEST HOOKS FOR ENHANCED TEST REPORTING
# ============================================
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture and store test results at different phases.
    
    This hook intercepts test execution to:
    1. Capture results of setup, test execution, and teardown phases
    2. Store results as attributes on the test item
    3. Enable fixtures to access test results (e.g., for conditional screenshots)
    
    The hook is triggered three times per test:
    - During setup (rep_setup)
    - During test execution (rep_call) 
    - During teardown (rep_teardown)
    
    Args:
        item: Pytest test item object representing the test
        call: Pytest call object containing phase information
    
    Yields:
        Test report object containing phase results
    """
    
    # Execute the test phase and capture the result
    outcome = yield  # Pytest executes the test phase here
    rep = outcome.get_result()  # Get the result of the test phase
    
    # Store the result as an attribute on the test item
    # Format: item.rep_setup, item.rep_call, item.rep_teardown
    # This allows fixtures to check if a test phase passed or failed
    setattr(item, f"rep_{rep.when}", rep)
    
    # Log phase completion for debugging (optional, can be verbose)
    # print(f"📝 Test phase '{rep.when}' completed with result: {rep.outcome}")


# ============================================
# AUTOMATIC FAILURE DETECTION FIXTURE
# ============================================
@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(request):
    """
    Automatic fixture for comprehensive failure detection and reporting.
    
    This fixture runs automatically for EVERY test (autouse=True) and:
    1. Monitors test execution across all phases (setup, test, teardown)
    2. Detects failures in any phase
    3. Triggers appropriate debugging actions (screenshots, logging)
    
    Unlike the screenshot logic in the driver fixture (which only handles
    test execution failures), this fixture catches ALL failure types.
    
    Args:
        request: Pytest request object containing test context
    """
    
    # Yield control to let the test execute
    # All test phases (setup, execution, teardown) happen here
    yield
    
    # After test completion, check for failures in any phase
    test_name = request.node.name
    
    # ============================================
    # CHECK FOR SETUP FAILURES
    # ============================================
    # Setup failures occur before the test function runs
    # Examples: Fixture failures, resource unavailability
    if hasattr(request.node, 'rep_setup') and request.node.rep_setup.failed:
        print(f"\n{'!'*60}")
        print(f"⚠️  TEST SETUP FAILED: {test_name}")
        print(f"{'!'*60}")
        
        # Attempt to capture screenshot for setup failures
        _capture_failure_screenshot(request, test_name, "SETUP_FAIL")
    
    # ============================================
    # CHECK FOR TEST EXECUTION FAILURES
    # ============================================
    # Test execution failures are handled in the driver fixture teardown
    # This avoids duplicate screenshot capture
    elif hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        # Already handled in driver fixture - no action needed here
        pass
    
    # ============================================
    # CHECK FOR TEARDOWN FAILURES
    # ============================================
    # Teardown failures occur after test execution
    # Examples: Cleanup errors, resource release failures
    elif hasattr(request.node, 'rep_teardown') and request.node.rep_teardown.failed:
        print(f"\n{'!'*60}")
        print(f"⚠️  TEST TEARDOWN FAILED: {test_name}")
        print(f"{'!'*60}")
        
        # Attempt to capture screenshot for teardown failures
        _capture_failure_screenshot(request, test_name, "TEARDOWN_FAIL")


# ============================================
# HELPER FUNCTION FOR FAILURE HANDLING
# ============================================
def _capture_failure_screenshot(request, test_name, failure_type):
    """
    Internal helper function to capture screenshots on various failure types.
    
    This function attempts to locate a WebDriver instance from test fixtures
    and capture a screenshot for debugging purposes.
    
    Args:
        request: Pytest request object for accessing fixtures
        test_name: Name of the failing test (for screenshot filename)
        failure_type: Type of failure (SETUP_FAIL, TEARDOWN_FAIL, etc.)
    
    Returns:
        str or None: Path to captured screenshot, or None if capture failed
    """
    
    print(f"   Attempting to capture failure screenshot...")
    
    # Iterate through all fixture names used by the test
    # Look for fixtures containing 'driver' (e.g., 'driver', 'logged_in_driver')
    for fixture_name in request.fixturenames:
        if 'driver' in fixture_name:
            try:
                # Attempt to retrieve the driver fixture instance
                driver = request.getfixturevalue(fixture_name)
                
                # Verify the driver is valid and has screenshot capability
                if driver and hasattr(driver, 'save_screenshot'):
                    print(f"   Found WebDriver in fixture: {fixture_name}")
                    
                    # Capture screenshot using the shared utility function
                    screenshot_path = take_screenshot(driver, test_name, failure_type)
                    
                    if screenshot_path:
                        print(f"   ✅ Screenshot captured: {screenshot_path}")
                        return screenshot_path
                    else:
                        print(f"   ⚠️  Screenshot capture failed")
                        
                break  # Stop after finding first valid driver
                
            except Exception as e:
                # Log error but continue searching for other driver fixtures
                print(f"   ⚠️  Could not access driver from fixture '{fixture_name}': {str(e)}")
                continue
    
    # If no driver found or screenshot failed
    print(f"   ⚠️  Could not capture screenshot: No accessible WebDriver found")
    return None


# ============================================
# ADDITIONAL CONFIGURATION HOOKS (OPTIONAL)
# ============================================
# Uncomment and customize these hooks as needed for advanced configuration

# @pytest.fixture(autouse=True)
# def setup_test_environment():
#     """
#     Global setup that runs before every test.
#     Useful for environment preparation, logging, etc.
#     """
#     print(f"\n📋 Setting up test environment...")
#     # Add global setup code here
#     yield
#     print(f"📋 Cleaning up test environment...")
#     # Add global teardown code here

# def pytest_configure(config):
#     """
#     Called at the start of the test run for overall configuration.
#     """
#     print(f"\n{'#'*60}")
#     print(f"STARTING TEST SESSION")
#     print(f"{'#'*60}")

# def pytest_sessionfinish(session, exitstatus):
#     """
#     Called at the end of the test run for final reporting.
#     """
#     print(f"\n{'#'*60}")
#     print(f"TEST SESSION COMPLETE")
#     print(f"Exit status: {exitstatus}")
#     print(f"{'#'*60}")


# ============================================
# MODULE DOCUMENTATION SUMMARY
# ============================================
"""
USAGE EXAMPLES:

1. Basic test with driver fixture:
   def test_example(driver):
       driver.get("https://example.com")
       assert "Example" in driver.title

2. Test requiring authentication:
   def test_authenticated_action(logged_in_driver):
       # Already logged in and on inventory page
       # Perform authenticated actions here

3. Running tests:
   - Basic: pytest test_file.py -v -s
   - With HTML report: pytest --html=report.html
   - Cross-platform: Same command works on Linux and Windows

KEY FEATURES PROVIDED:
- Automatic WebDriver management (downloads, versions, paths)
- Cross-platform compatibility (Linux/Windows)
- Screenshot capture on failures
- Pre-authenticated driver for login-required tests
- Comprehensive test phase monitoring
- Clean resource management

TROUBLESHOOTING:
1. WebDriver issues: Check Chrome/Chromium installation
2. Login failures: Verify credentials in data.py
3. Screenshot issues: Check write permissions in current directory
4. Platform issues: Verify platform detection in logs
"""