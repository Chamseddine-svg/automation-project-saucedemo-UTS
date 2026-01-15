/**
 * @fileoverview Product filtering test suite
 * @description Tests product sorting functionality (price and name filters)
 */

const { test, expect } = require('@playwright/test');
const { AuthActions, ProductActions, CommonActions } = require('../actions/actions.js');
const { getUserByType, loadSteps } = require('../utils/loader.js');
const { sortOptions } = require('../pages/actionMap.js');
const fs = require('fs');
const path = require('path');

test.describe('Product Filtering Tests', () => {
  let page;
  let context;
  let authActions;
  let productActions;
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
    commonActions = new CommonActions(page);

    // Étape 1: Se connecter avec l'utilisateur standard
    console.log('Connexion avec l\'utilisateur standard...');
    await page.goto(testData.config.baseURL);
    await authActions.login(standardUser.username, standardUser.password);
    await commonActions.waitForPageLoad();
    
    // Vérifier que la connexion a réussi
    await expect(page).toHaveURL(/.*inventory.html/);
    console.log('✅ Connexion réussie');
  });

  test.afterAll(async () => {
    await context.close();
  });

  test('should display default filter as Name A to Z', async () => {
    // Étape 2: Vérifier que le filtre par défaut est "Name (A to Z)"
    const currentFilter = await productActions.getCurrentSortFilter();
    expect(currentFilter).toBe(sortOptions.NAME_ASC);
    
    // Vérifier aussi visuellement que les produits sont triés A-Z
    await productActions.verifyNameSort(true);
    
    console.log('✅ Filtre par défaut vérifié: Name (A to Z)');
    await commonActions.takeScreenshot('default-filter-name-a-to-z');
  });

  test('should sort products by price from low to high', async () => {
    // Étape 3: Changer le filtre à "Price (low to high)"
    await productActions.selectSortFilter(sortOptions.PRICE_LOW_HIGH);
    console.log('✅ Filtre changé à: Price (low to high)');
    
    // Étape 4: Vérifier que les produits sont bien triés par prix croissant
    await productActions.verifyPriceSortAscending();
    console.log('✅ Produits triés par prix croissant vérifiés');
    
    // Étape 5: Capturer une screenshot après le tri
    await commonActions.takeScreenshot('price-low-to-high');
  });

  test('should sort products by price from high to low', async () => {
    // Étape 6: Changer le filtre à "Price (high to low)"
    await productActions.selectSortFilter(sortOptions.PRICE_HIGH_LOW);
    await productActions.verifyPriceSortDescending();
    console.log('✅ Filtre changé à: Price (high to low)');
    
    // Étape 7: Vérifier que le premier produit a le prix le plus élevé
    const prices = await productActions.getProductPrices();
    expect(prices[0]).toBe(Math.max(...prices));
    console.log(`✅ Premier produit a le prix le plus élevé: $${prices[0]}`);
    
    // Étape 8: Vérifier que le dernier produit a le prix le plus bas
    expect(prices[prices.length - 1]).toBe(Math.min(...prices));
    console.log(`✅ Dernier produit a le prix le plus bas: $${prices[prices.length - 1]}`);
    
    await commonActions.takeScreenshot('price-high-to-low');
  });

  test('should sort products alphabetically A to Z', async () => {
    await productActions.selectSortFilter(sortOptions.NAME_ASC);
    await productActions.verifyNameSort(true);
    console.log('✅ Tri alphabétique A à Z vérifié');
    await commonActions.takeScreenshot('sort-name-a-to-z');
  });

  test('should sort products alphabetically Z to A', async () => {
    await productActions.selectSortFilter(sortOptions.NAME_DESC);
    await productActions.verifyNameSort(false);
    console.log('✅ Tri alphabétique Z à A vérifié');
    await commonActions.takeScreenshot('sort-name-z-to-a');
  });

  test('should maintain filter after adding product to cart', async () => {
    // Remettre le filtre à Price (high to low) pour ce test
    await productActions.selectSortFilter(sortOptions.PRICE_HIGH_LOW);
    
    // Ajouter un produit au panier
    await productActions.addProductToCart(testData.products.backpack);
    console.log('✅ Produit ajouté au panier');
    
    // Vérifier que le filtre est toujours maintenu
    const currentFilter = await productActions.getCurrentSortFilter();
    expect(currentFilter).toBe(sortOptions.PRICE_HIGH_LOW);
    
    await productActions.verifyPriceSortDescending();
    console.log('✅ Filtre maintenu après ajout au panier');
    await commonActions.takeScreenshot('maintain-filter-after-add-to-cart');
  });
});