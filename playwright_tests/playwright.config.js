/**
 * @fileoverview Playwright test configuration
 * @description Global configuration for test execution on Chrome only
 */

// @ts-check
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  /* 🔹 Test directory */
  testDir: './tests/specs',

  /* 🔹 Output directory for test results */
  outputDir: 'test-results',

  /* 🔹 Global timeout (90 seconds) */
  timeout: 90 * 1000,

  /* 🔹 Expect timeout */
  expect: {
    timeout: 15000,
  },

  /* 🔹 Test execution settings - Chrome only, sequential */
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: 1,

  /* 🔹 Reporter configuration */
  reporter: [
    ['list'],
    ['html', {
      outputFolder: 'playwright-report',
      open: 'never'
    }],
    ['json', {
      outputFile: 'test-results/results.json'
    }],
    ['junit', {
      outputFile: 'test-results/junit.xml'
    }]
  ],

  /* 🔹 Shared settings for all tests */
  use: {
    // Base URL for navigation
    baseURL: 'https://www.saucedemo.com',

    // Run in headless mode (set to false for debugging)
    headless: true,

    // Capture screenshot on success and failure (change to 'only-on-failure' if needed)
    screenshot: 'on',

    // Record video only on failure
    video: 'retain-on-failure',

    // Trace on first retry
    trace: 'on-first-retry',

    // Viewport size
    viewport: { width: 1280, height: 720 },

    // Ignore HTTPS errors
    ignoreHTTPSErrors: true,

    // Action timeout
    actionTimeout: 15000,

    // Navigation timeout
    navigationTimeout: 30000,

    // Launch options
    launchOptions: {
      // Slow down actions when debugging
      slowMo: process.env.DEBUG ? 500 : 0
    }
  },

  /* 🔹 Chrome project only */
  projects: [
    {
      name: 'Chrome',
      use: {
        ...devices['Desktop Chrome'],
        channel: 'chrome',
        locale: 'en-US',
        timezoneId: 'America/New_York'
      },
    }
  ]
});