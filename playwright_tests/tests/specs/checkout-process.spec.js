/**
 * @fileoverview Checkout process test suite
 * @description Tests complete purchase flow from cart to order confirmation
 */

const { test, expect } = require('@playwright/test');
const { AuthActions, ProductActions, CartActions, CheckoutActions, CommonActions } = require('../actions/actions.js');
const { getUserByType, loadSteps } = require('../utils/loader.js');
const fs = require('fs');
const path = require('path');

test.describe('Checkout Process Tests', () => {
  let page;
  let context;
  let authActions;
  let productActions;
  let cartActions;
  let checkoutActions;
  let commonActions;
  const testData = loadSteps();
  const standardUser = getUserByType('standard');

  test.beforeAll(async ({ browser }) => {
    // Créer le dossier screenshots s'il n'existe pas
    const screenshotsDir = path.join(process.cwd(), 'screenshots');
    if (!fs.existsSync(screenshotsDir)) {
      fs.mkdirSync(screenshotsDir, { recursive: true });
      console.log('📁 Screenshots directory created');
    }

    // Créer le contexte et la page qui seront réutilisés
    context = await browser.newContext();
    page = await context.newPage();
    
    // Initialiser les actions
    authActions = new AuthActions(page);
    productActions = new ProductActions(page);
    cartActions = new CartActions(page);
    checkoutActions = new CheckoutActions(page);
    commonActions = new CommonActions(page);

    // Étape 1: Se connecter avec l'utilisateur standard (beforeAll)
    console.log('Préparation des tests de checkout...');
    await page.goto(testData.config.baseURL);
    await authActions.login(standardUser.username, standardUser.password);
    await commonActions.waitForPageLoad();
    
    // Vérifier que la connexion a réussi
    await expect(page).toHaveURL(/.*inventory.html/);
    console.log('✅ Connexion utilisateur standard réussie');
  });

  test.afterAll(async () => {
    await context.close();
  });

  // Hook pour nettoyer le panier avant chaque test
  test.beforeEach(async () => {
    // Retourner à la page des produits
    await page.goto(`${testData.config.baseURL}/inventory.html`);
    
    // Vérifier si le badge du panier existe (indique des produits dans le panier)
    const cartBadge = page.locator('.shopping_cart_badge');
    const hasBadge = await cartBadge.isVisible().catch(() => false);
    
    if (hasBadge) {
      console.log('⚠️ Nettoyage du panier avant le test...');
      await cartActions.clearCart();
      await page.goto(`${testData.config.baseURL}/inventory.html`);
      console.log('✅ Panier nettoyé');
    }
  });

  test('should complete full purchase flow successfully', async () => {
    // Étape 2: Ajouter un produit au panier
    const productToAdd = testData.products.backpack;
    await productActions.addProductToCart(productToAdd);
    console.log(`✅ Étape 2: Produit ajouté au panier - ${productToAdd}`);
    
    // Vérifier que le badge du panier affiche "1"
    await productActions.verifyCartBadgeCount(1);
    await commonActions.takeScreenshot('checkout-product-added-to-cart');
    
    // Étape 3: Aller dans le panier
    await cartActions.goToCart();
    await expect(page).toHaveURL(/.*cart.html/);
    console.log('✅ Étape 3: Navigation vers le panier réussie');
    
    // Vérifier que le produit est bien dans le panier
    await cartActions.verifyProductInCart(productToAdd);
    const cartItemCount = await cartActions.getCartItemCount();
    expect(cartItemCount).toBe(1);
    await commonActions.takeScreenshot('checkout-cart-page');
    
    // Étape 4: Cliquer sur "Checkout"
    await cartActions.proceedToCheckout();
    await expect(page).toHaveURL(/.*checkout-step-one.html/);
    console.log('✅ Étape 4: Page de checkout ouverte');
    await commonActions.takeScreenshot('checkout-information-page');
    
    // Étape 5: Remplir le formulaire avec les informations spécifiées
    const checkoutInfo = testData.checkout.testCustomer;
    await checkoutActions.fillCheckoutInfo(checkoutInfo);
    console.log('✅ Étape 5: Formulaire rempli - First Name: Test, Last Name: User, ZIP: 12345');
    await commonActions.takeScreenshot('checkout-form-filled');
    
    // Étape 6: Cliquer sur "Continue"
    await checkoutActions.continueToOverview();
    await expect(page).toHaveURL(/.*checkout-step-two.html/);
    console.log('✅ Étape 6: Bouton Continue cliqué');
    
    // Étape 7: Vérifier la page de récapitulatif
    await checkoutActions.verifyCheckoutOverview();
    
    // Vérifier que le produit est dans le récapitulatif
    const summaryItemName = await page.textContent('.inventory_item_name');
    expect(summaryItemName).toBe(productToAdd);
    
    // Vérifier que le total est affiché
    const totalText = await page.textContent('.summary_total_label');
    expect(totalText).toContain('Total');
    console.log('✅ Étape 7: Page de récapitulatif vérifiée');
    await commonActions.takeScreenshot('checkout-overview-page');
    
    // Étape 8: Cliquer sur "Finish"
    await checkoutActions.finishPurchase();
    await expect(page).toHaveURL(/.*checkout-complete.html/);
    console.log('✅ Étape 8: Bouton Finish cliqué - Commande finalisée');
    
    // Étape 9: Vérifier le message de confirmation "Thank you for your order!"
    await checkoutActions.verifyOrderConfirmation(testData.checkout.confirmationMessage);
    const confirmHeader = await page.textContent('.complete-header');
    expect(confirmHeader).toBe(testData.checkout.confirmationMessage);
    console.log('✅ Étape 9: Message de confirmation vérifié - "Thank you for your order!"');
    await commonActions.takeScreenshot('checkout-confirmation-page');
    
    // Étape 10: Vérifier que le badge du panier n'est plus visible
    await productActions.verifyCartBadgeCount(0);
    const cartBadge = page.locator('.shopping_cart_badge');
    await expect(cartBadge).not.toBeVisible();
    console.log('✅ Étape 10: Badge du panier n\'est plus visible');
    
    // Vérifications supplémentaires
    const ponyImage = page.locator('.pony_express');
    await expect(ponyImage).toBeVisible();
    
    const confirmationText = await page.textContent('.complete-text');
    expect(confirmationText).toContain('Your order has been dispatched');
    
    await commonActions.takeScreenshot('checkout-complete-success');
    console.log('✅ TEST COMPLET RÉUSSI - Flux d\'achat complet terminé avec succès');
  });

  test('should display error when checkout form fields are empty', async () => {
    // Ajouter un produit au panier
    await productActions.addProductToCart(testData.products.bikeLight);
    
    // Aller au checkout
    await cartActions.goToCart();
    await cartActions.proceedToCheckout();
    await expect(page).toHaveURL(/.*checkout-step-one.html/);
    
    // Essayer de continuer sans remplir le formulaire
    await checkoutActions.continueToOverview();
    
    // Vérifier le message d'erreur
    const errorMessage = page.locator('[data-test="error"]');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('Error: First Name is required');
    
    console.log('✅ Message d\'erreur affiché pour formulaire vide');
    await commonActions.takeScreenshot('checkout-error-empty-form');
  });

  test('should allow user to cancel checkout and return to cart', async () => {
    // Ajouter un produit au panier
    await productActions.addProductToCart(testData.products.onesie);
    
    // Aller au checkout
    await cartActions.goToCart();
    await cartActions.proceedToCheckout();
    await expect(page).toHaveURL(/.*checkout-step-one.html/);
    await commonActions.takeScreenshot('checkout-before-cancel');
    
    // Annuler le checkout
    await page.click('[data-test="cancel"]');
    await expect(page).toHaveURL(/.*cart.html/);
    
    // Vérifier que le produit est toujours dans le panier
    await cartActions.verifyProductInCart(testData.products.onesie);
    
    console.log('✅ Annulation du checkout réussie');
    await commonActions.takeScreenshot('checkout-after-cancel');
  });

  test('should verify total price calculation in checkout overview', async () => {
    // Ajouter plusieurs produits au panier
    await productActions.addProductToCart(testData.products.backpack);
    await productActions.addProductToCart(testData.products.bikeLight);
    
    // Aller au checkout et remplir le formulaire
    await cartActions.goToCart();
    await cartActions.proceedToCheckout();
    await checkoutActions.fillCheckoutInfo(testData.checkout.testCustomer);
    await checkoutActions.continueToOverview();
    
    // Vérifier que tous les éléments de prix sont présents
    await checkoutActions.verifyCheckoutOverview();
    
    // Récupérer le prix total
    const totalPrice = await checkoutActions.getTotalPrice();
    expect(totalPrice).toBeGreaterThan(0);
    
    console.log(`✅ Prix total vérifié: $${totalPrice}`);
    await commonActions.takeScreenshot('checkout-price-verification');
  });
});