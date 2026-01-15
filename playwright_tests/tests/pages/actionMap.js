/**
 * @fileoverview Centralized selector map for SauceDemo application
 * @description All CSS selectors are defined here to ensure maintainability
 * Uses data-test attributes as primary selectors (most robust)
 * Falls back to semantic selectors when data-test is unavailable
 */

const selectors = {
  // Authentication selectors
  auth: {
    usernameInput: '[data-test="username"]',
    passwordInput: '[data-test="password"]',
    loginButton: '[data-test="login-button"]',
    errorMessage: '[data-test="error"]',
    errorButton: '.error-button'
  },

  // Navigation selectors
  nav: {
    menuButton: '#react-burger-menu-btn',
    logoutLink: '#logout_sidebar_link',
    cartLink: '.shopping_cart_link',
    cartBadge: '.shopping_cart_badge'
  },

  // Product listing selectors
  products: {
    container: '.inventory_list',
    items: '.inventory_item',
    itemName: '.inventory_item_name',
    itemDescription: '.inventory_item_desc',
    itemPrice: '.inventory_item_price',
    addToCartButton: (productName) => `[data-test="add-to-cart-${productName.toLowerCase().replace(/\s+/g, '-')}"]`,
    removeButton: (productName) => `[data-test="remove-${productName.toLowerCase().replace(/\s+/g, '-')}"]`,
    sortDropdown: '[data-test="product-sort-container"]'
  },

  // Cart selectors
  cart: {
    item: '.cart_item',
    itemName: '.inventory_item_name',
    itemPrice: '.inventory_item_price',
    checkoutButton: '[data-test="checkout"]',
    continueShoppingButton: '[data-test="continue-shopping"]',
    removeButton: (productName) => `[data-test="remove-${productName.toLowerCase().replace(/\s+/g, '-')}"]`
  },

  // Checkout form selectors
  checkout: {
    firstNameInput: '[data-test="firstName"]',
    lastNameInput: '[data-test="lastName"]',
    postalCodeInput: '[data-test="postalCode"]',
    continueButton: '[data-test="continue"]',
    cancelButton: '[data-test="cancel"]',
    errorMessage: '[data-test="error"]'
  },

  // Checkout overview selectors
  overview: {
    summaryInfo: '.summary_info',
    itemTotal: '.summary_subtotal_label',
    tax: '.summary_tax_label',
    total: '.summary_total_label',
    finishButton: '[data-test="finish"]',
    cancelButton: '[data-test="cancel"]'
  },

  // Confirmation selectors
  confirmation: {
    header: '.complete-header',
    message: '.complete-text',
    backButton: '[data-test="back-to-products"]',
    ponyExpressImage: '.pony_express'
  }
};

/**
 * Sort options available in product filter
 */
const sortOptions = {
  NAME_ASC: 'az',
  NAME_DESC: 'za',
  PRICE_LOW_HIGH: 'lohi',
  PRICE_HIGH_LOW: 'hilo'
};

module.exports = { selectors, sortOptions };