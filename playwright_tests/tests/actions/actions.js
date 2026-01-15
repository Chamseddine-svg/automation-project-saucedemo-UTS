/**
 * @fileoverview Reusable page actions for SauceDemo application
 * @description Provides high-level actions that can be used across multiple tests
 */

const { expect } = require('@playwright/test');
const { selectors } = require('../pages/actionMap.js');
const path = require('path');

/**
 * Authentication actions
 */
class AuthActions {
  constructor(page) {
    this.page = page;
  }

  /**
   * Performs login with provided credentials
   * @param {string} username - Username for login
   * @param {string} password - Password for login
   */
  async login(username, password) {
    await this.page.fill(selectors.auth.usernameInput, username);
    await this.page.fill(selectors.auth.passwordInput, password);
    await this.page.click(selectors.auth.loginButton);
  }

  /**
   * Verifies error message is displayed
   * @param {string} expectedMessage - Expected error message text
   */
  async verifyErrorMessage(expectedMessage) {
    const errorElement = this.page.locator(selectors.auth.errorMessage);
    await expect(errorElement).toBeVisible();
    await expect(errorElement).toContainText(expectedMessage);
  }

  /**
   * Performs logout from the application
   */
  async logout() {
    await this.page.click(selectors.nav.menuButton);
    await this.page.click(selectors.nav.logoutLink);
  }
}

/**
 * Product listing actions
 */
class ProductActions {
  constructor(page) {
    this.page = page;
  }

  /**
   * Changes the product sort filter
   * @param {string} sortOption - Sort option value
   */
  async selectSortFilter(sortOption) {
    await this.page.selectOption(selectors.products.sortDropdown, sortOption);
    await this.page.waitForTimeout(300);
  }

  /**
   * Gets the current sort filter value
   * @returns {Promise<string>} Current filter value
   */
  async getCurrentSortFilter() {
    return await this.page.locator(selectors.products.sortDropdown).inputValue();
  }

  /**
   * Retrieves all product prices as numbers
   * @returns {Promise<number[]>} Array of product prices
   */
  async getProductPrices() {
    const priceElements = await this.page.locator(selectors.products.itemPrice).all();
    const prices = [];
    
    for (const element of priceElements) {
      const priceText = await element.textContent();
      const price = parseFloat(priceText.replace('$', ''));
      prices.push(price);
    }
    
    return prices;
  }

  /**
   * Gets all product names in current order
   * @returns {Promise<string[]>} Array of product names
   */
  async getProductNames() {
    const nameElements = await this.page.locator(selectors.products.itemName).all();
    const names = [];
    
    for (const element of nameElements) {
      names.push(await element.textContent());
    }
    
    return names;
  }

  /**
   * Verifies products are sorted by price in ascending order
   */
  async verifyPriceSortAscending() {
    const prices = await this.getProductPrices();
    
    for (let i = 0; i < prices.length - 1; i++) {
      expect(prices[i]).toBeLessThanOrEqual(prices[i + 1]);
    }
  }

  /**
   * Verifies products are sorted by price in descending order
   */
  async verifyPriceSortDescending() {
    const prices = await this.getProductPrices();
    
    for (let i = 0; i < prices.length - 1; i++) {
      expect(prices[i]).toBeGreaterThanOrEqual(prices[i + 1]);
    }
  }

  /**
   * Verifies products are sorted by name alphabetically
   * @param {boolean} ascending - True for A-Z, false for Z-A
   */
  async verifyNameSort(ascending) {
    const names = await this.getProductNames();
    const sortedNames = [...names].sort();
    
    if (!ascending) {
      sortedNames.reverse();
    }
    
    expect(names).toEqual(sortedNames);
  }

  /**
   * Adds a product to cart by product name
   * Handles the case where the product might already be in cart
   * @param {string} productName - Full name of the product
   */
  async addProductToCart(productName) {
    const addButtonSelector = selectors.products.addToCartButton(productName);
    const removeButtonSelector = selectors.products.removeButton(productName);
    
    // Check if product is already in cart (Remove button visible)
    const removeButton = this.page.locator(removeButtonSelector);
    const isInCart = await removeButton.isVisible().catch(() => false);
    
    if (isInCart) {
      // Product already in cart, remove it first then add it back
      console.log(`⚠️ Product "${productName}" already in cart, removing first...`);
      await removeButton.click();
      await this.page.waitForTimeout(200); // Wait for button to change
    }
    
    // Now click the Add to Cart button
    const addButton = this.page.locator(addButtonSelector);
    await addButton.waitFor({ state: 'visible', timeout: 5000 });
    await addButton.click();
  }

  /**
   * Verifies cart badge shows correct item count
   * @param {number} expectedCount - Expected number of items
   */
  async verifyCartBadgeCount(expectedCount) {
    const badge = this.page.locator(selectors.nav.cartBadge);
    
    if (expectedCount === 0) {
      await expect(badge).not.toBeVisible();
    } else {
      await expect(badge).toBeVisible();
      await expect(badge).toHaveText(expectedCount.toString());
    }
  }
}

/**
 * Shopping cart actions
 */
class CartActions {
  constructor(page) {
    this.page = page;
  }

  /**
   * Navigates to the shopping cart
   */
  async goToCart() {
    await this.page.click(selectors.nav.cartLink);
  }

  /**
   * Proceeds to checkout from cart
   */
  async proceedToCheckout() {
    await this.page.click(selectors.cart.checkoutButton);
  }

  /**
   * Verifies a product is in the cart
   * @param {string} productName - Name of the product to verify
   */
  async verifyProductInCart(productName) {
    const cartItem = this.page.locator(selectors.cart.itemName, { hasText: productName });
    await expect(cartItem).toBeVisible();
  }

  /**
   * Gets the number of items in cart
   * @returns {Promise<number>} Number of cart items
   */
  async getCartItemCount() {
    return await this.page.locator(selectors.cart.item).count();
  }

  /**
   * Clears all items from the cart
   */
  async clearCart() {
    await this.goToCart();
    const removeButtons = await this.page.locator('[id^="remove-"]').all();
    
    for (const button of removeButtons) {
      await button.click();
      await this.page.waitForTimeout(100);
    }
  }
}

/**
 * Checkout process actions
 */
class CheckoutActions {
  constructor(page) {
    this.page = page;
  }

  /**
   * Fills checkout information form
   * @param {Object} info - Checkout information
   */
  async fillCheckoutInfo(info) {
    await this.page.fill(selectors.checkout.firstNameInput, info.firstName);
    await this.page.fill(selectors.checkout.lastNameInput, info.lastName);
    await this.page.fill(selectors.checkout.postalCodeInput, info.postalCode);
  }

  /**
   * Continues to checkout overview
   */
  async continueToOverview() {
    await this.page.click(selectors.checkout.continueButton);
  }

  /**
   * Completes the purchase
   */
  async finishPurchase() {
    await this.page.click(selectors.overview.finishButton);
  }

  /**
   * Verifies the order confirmation message
   * @param {string} expectedMessage - Expected confirmation header text
   */
  async verifyOrderConfirmation(expectedMessage) {
    const confirmHeader = this.page.locator(selectors.confirmation.header);
    await expect(confirmHeader).toBeVisible();
    
    if (expectedMessage) {
      await expect(confirmHeader).toHaveText(expectedMessage);
    } else {
      await expect(confirmHeader).toContainText('Thank you');
    }
  }

  /**
   * Gets the total price from checkout overview
   * @returns {Promise<number>} Total price
   */
  async getTotalPrice() {
    const totalText = await this.page.locator(selectors.overview.total).textContent();
    return parseFloat(totalText.replace('Total: $', ''));
  }

  /**
   * Verifies checkout overview contains expected elements
   */
  async verifyCheckoutOverview() {
    await expect(this.page.locator(selectors.overview.summaryInfo)).toBeVisible();
    await expect(this.page.locator(selectors.overview.itemTotal)).toBeVisible();
    await expect(this.page.locator(selectors.overview.tax)).toBeVisible();
    await expect(this.page.locator(selectors.overview.total)).toBeVisible();
  }
}

/**
 * Utility actions used across multiple page objects
 */
class CommonActions {
  constructor(page) {
    this.page = page;
  }

  /**
   * Takes a screenshot with a descriptive name
   * @param {string} name - Screenshot filename (without extension)
   */
  async takeScreenshot(name) {
    const screenshotPath = path.join('screenshots', `${name}.png`);
    await this.page.screenshot({ 
      path: screenshotPath,
      fullPage: true 
    });
    console.log(`📸 Screenshot saved: ${screenshotPath}`);
  }

  /**
   * Waits for page to be fully loaded
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }
}

module.exports = {
  AuthActions,
  ProductActions,
  CartActions,
  CheckoutActions,
  CommonActions
};