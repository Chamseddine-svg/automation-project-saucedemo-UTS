/**
 * @fileoverview Authentication test suite
 * @description Tests login functionality with various user types and error scenarios
 */

const { test, expect } = require('@playwright/test');
const { AuthActions, CommonActions } = require('../actions/actions.js');
const { getUserByType, loadSteps } = require('../utils/loader.js');
const fs = require('fs');
const path = require('path');

test.describe('Login Tests', () => {
  let page;
  let authActions;
  let commonActions;
  const testData = loadSteps();

  test.beforeAll(async ({ browser }) => {
    // Créer le dossier screenshots s'il n'existe pas
    const screenshotsDir = path.join(process.cwd(), 'screenshots');
    if (!fs.existsSync(screenshotsDir)) {
      fs.mkdirSync(screenshotsDir, { recursive: true });
      console.log('📁 Screenshots directory created');
    }
  });

  test.beforeEach(async ({ browser }) => {
    const context = await browser.newContext();
    page = await context.newPage();
    
    authActions = new AuthActions(page);
    commonActions = new CommonActions(page);
    
    await page.goto(testData.config.baseURL);
  });

  test('should successfully login with standard user', async () => {
    const standardUser = getUserByType('standard');
    
    await authActions.login(standardUser.username, standardUser.password);
    await expect(page).toHaveURL(/.*inventory.html/);
    await expect(page.locator('.inventory_list')).toBeVisible();
    // Capture d'écran de la connexion réussie avec l'utilisateur standard
    await commonActions.takeScreenshot('login-success-standard-user');
  });

  test('should display error for locked out user', async () => {
    const lockedUser = getUserByType('locked');
    
    await authActions.login(lockedUser.username, lockedUser.password);
    await authActions.verifyErrorMessage(testData.errorMessages.lockedUser);
    await expect(page).toHaveURL(testData.config.baseURL + '/');
    // Capture d'écran de l'erreur utilisateur verrouillé
    await commonActions.takeScreenshot('login-error-locked-user');
  });

  test('should display error for invalid credentials', async () => {
    await authActions.login('invalid_user', 'wrong_password');
    await authActions.verifyErrorMessage(testData.errorMessages.invalidCredentials);
    // Capture d'écran de l'erreur identifiants invalides
    await commonActions.takeScreenshot('login-error-invalid-credentials');
  });

  test('should display error when username is missing', async () => {
    await authActions.login('', testData.credentials.validPassword);
    await authActions.verifyErrorMessage(testData.errorMessages.missingUsername);
    // Capture d'écran de l'erreur nom d'utilisateur manquant
    await commonActions.takeScreenshot('login-error-missing-username');
  });

  test('should display error when password is missing', async () => {
    const standardUser = getUserByType('standard');
    
    await authActions.login(standardUser.username, '');
    await authActions.verifyErrorMessage(testData.errorMessages.missingPassword);
    // Capture d'écran de l'erreur mot de passe manquant
    await commonActions.takeScreenshot('login-error-missing-password');
  });

  test('should allow dismissing error message', async () => {
    await authActions.login('invalid', 'invalid');
    
    const errorElement = page.locator('[data-test="error"]');
    await expect(errorElement).toBeVisible();
    // Capture d'écran avant de fermer le message d'erreur
    await commonActions.takeScreenshot('login-error-before-dismiss');
    
    await page.click('.error-button');
    await expect(errorElement).not.toBeVisible();
    // Capture d'écran après fermeture du message d'erreur
    await commonActions.takeScreenshot('login-error-after-dismiss');
  });

  test('should successfully logout after login', async () => {
    const standardUser = getUserByType('standard');
    
    await authActions.login(standardUser.username, standardUser.password);
    await expect(page).toHaveURL(/.*inventory.html/);
    // Capture d'écran avant déconnexion
    await commonActions.takeScreenshot('before-logout');
    
    await authActions.logout();
    await expect(page).toHaveURL(testData.config.baseURL + '/');
    await expect(page.locator('[data-test="username"]')).toBeVisible();
    // Capture d'écran après déconnexion
    await commonActions.takeScreenshot('after-logout');
  });

  test('should handle problem user login', async () => {
    const problemUser = getUserByType('problem');
    
    await authActions.login(problemUser.username, problemUser.password);
    await expect(page).toHaveURL(/.*inventory.html/);
    await expect(page.locator('.inventory_list')).toBeVisible();
    // Capture d'écran de la connexion avec l'utilisateur problématique
    await commonActions.takeScreenshot('login-problem-user');
  });

  test('should clear input fields on page reload', async () => {
    const standardUser = getUserByType('standard');
    
    await page.fill('[data-test="username"]', standardUser.username);
    await page.fill('[data-test="password"]', standardUser.password);
    // Capture d'écran avant rechargement de la page
    await commonActions.takeScreenshot('before-page-reload');
    
    await page.reload();
    
    const usernameValue = await page.inputValue('[data-test="username"]');
    const passwordValue = await page.inputValue('[data-test="password"]');
    
    expect(usernameValue).toBe('');
    expect(passwordValue).toBe('');
    // Capture d'écran après rechargement (champs vidés)
    await commonActions.takeScreenshot('after-page-reload-cleared');
  });
});