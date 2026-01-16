Saucedemo.com Tests Automated Project
# Modular Selenium Test Suite

This project provides a **modular, parameterized test framework** for automated web testing of the [Swag Labs](https://www.saucedemo.com/) demo application. It covers login workflows, product inventory verification, and navigation checks using **Python**, **pytest**, and **Selenium WebDriver**.

---

## Table of Contents

- [Features](#features)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Running Tests](#running-tests)  
- [Test Design](#test-design)  
- [Screenshots & Reporting](#screenshots--reporting)  
- [Extending Tests](#extending-tests)  

---

## Features

- **Modular Login Tests**
  - Valid credentials
  - Invalid credentials
  - Locked users
  - Error message verification
  - Automatic screenshot capture on failure

- **Modular Product Tests**
  - Inventory page product verification
  - UI element checks (image, add-to-cart, name link)
  - Product detail page navigation
  - Product details verification
  - Navigation back to inventory page

- **Centralized Configuration**
  - Timeouts, URLs, expected product count, and browser settings
  - Easy to modify for different environments

- **Parameterized Tests**
  - All login and product scenarios are combined into reusable, data-driven tests.

---

## Project Structure

            
# 🧪 Playwright Test Automation - SauceDemo
## Documentation Complète des Tests E2E

_______________________________________________________________________________

## 📌 Objectif des tests

Cette suite de tests Playwright automatise les tests end-to-end de l'application **SauceDemo** afin de valider les parcours utilisateurs principaux depuis le navigateur, avec un focus sur :
- ✅ La stabilité de l'interface utilisateur
- ✅ La navigation entre les pages
- ✅ Les flux métier critiques (login, filtrage, checkout)

Les tests permettent de **détecter rapidement les régressions UI** après chaque modification du code et garantissent que les fonctionnalités essentielles restent opérationnelles.

_______________________________________________________________________________

## 🏗️ Architecture du projet

### Diagramme d'architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Tests (specs/)                             │
│         Scénarios de test métier lisibles                     │
│  • login.spec.js                                              │
│  • product-filter.spec.js                                     │
│  • checkout-process.spec.js                                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ├──► Actions (actions/)
                     │    • AuthActions (login, logout)
                     │    • ProductActions (addToCart, verifyBadge)
                     │    • CartActions (goToCart, clearCart)
                     │    • CheckoutActions (fillForm, finishPurchase)
                     │    • CommonActions (screenshots, waitForLoad)
                     │
                     ├──► ActionMap (pages/)
                     │    • Sélecteurs CSS centralisés
                     │    • Locators de tous les éléments
                     │
                     └──► Loader (utils/)
                          • loadSteps() - Charge steps.json
                          • getUserByType() - Charge users.json
```

_______________________________________________________________________________

## 📂 Structure détaillée

```
tests/
├── pages/
│   └── actionMap.js              # 🎯 Sélecteurs CSS/XPath centralisés
│                                 # Tous les locators de l'application
│
├── actions/
│   └── actions.js                # 🔧 Classes d'actions réutilisables
│                                 # AuthActions, ProductActions, CartActions,
│                                 # CheckoutActions, CommonActions
│
├── utils/
│   └── loader.js                 # 📂 Utilitaires de chargement
│                                 # loadSteps(), getUserByType()
│
├── data/
│   ├── steps.json                # 📊 Données de test
│   │                             # Products, checkout info, messages
│   └── users.json                # 👤 Configuration des utilisateurs
│                                 # standard_user, problem_user, locked_out_user
│
└── specs/
    ├── login.spec.js             # ✅ Tests de connexion
    ├── product-filter.spec.js    # ✅ Tests de filtrage des produits
    └── checkout-process.spec.js  # ✅ Tests du processus d'achat complet
```

_______________________________________________________________________________

## ✅ Avantages de cette architecture

| Fichier              | Responsabilité                        | En cas de changement                                |
|----------------------|---------------------------------------|-----------------------------------------------------|
| **actionMap.js**     | Stocke tous les sélecteurs CSS        | Si l'UI change → Modifier **1 seul fichier**        |
| **actions.js**       | Définit les actions métier en classes | Si la logique change → Modifier les classes Actions |
| **loader.js**        | Charge les données JSON               | Si le format change → Modifier le loader            |
| **steps.json**       | Contient les données de test          | Modifier données **sans toucher au code**           |
| **users.json**       | Contient les utilisateurs             | Ajouter/modifier users facilement                   |
| **specs/\*.spec.js** | Décrit les scénarios de test          | Ajouter tests **sans modifier l'infrastructure**    |

_______________________________________________________________________________

## 🔐 Tests d'authentification (login.spec.js)

Les tests Playwright vérifient le processus de connexion à l'application :

### ✅ Scénarios couverts :
- ✔ **Connexion réussie** avec utilisateur standard
  - Accès à la page de login
  - Saisie des identifiants valides
  - Validation de la connexion
  - Vérification de la redirection vers `/inventory.html`
  - Présence des éléments de navigation (menu, panier)

- ✔ **Gestion des erreurs** de connexion
  - Utilisateur bloqué (`locked_out_user`)
  - Identifiants invalides
  - Champs vides
  - Affichage des messages d'erreur appropriés

- ✔ **Déconnexion**
  - Clic sur le menu burger
  - Clic sur "Logout"
  - Retour à la page de login

### 📋 Classes utilisées :
- `AuthActions` : login(), logout()
- `CommonActions` : waitForPageLoad(), takeScreenshot()

🎯 **Fonctionnalité couverte** : Authentification utilisateur

_______________________________________________________________________________

## 🔍 Tests de filtrage des produits (product-filter.spec.js)

Les tests valident le système de tri et filtrage de la page inventaire :

### ✅ Scénarios couverts :
- ✔ **Tri par nom (A → Z)**
  - Vérification de l'ordre alphabétique croissant
  - Validation que tous les produits sont affichés

- ✔ **Tri par nom (Z → A)**
  - Vérification de l'ordre alphabétique décroissant

- ✔ **Tri par prix (Low → High)**
  - Vérification que les produits sont triés du moins cher au plus cher
  - Validation des valeurs numériques des prix

- ✔ **Tri par prix (High → Low)**
  - Vérification que les produits sont triés du plus cher au moins cher

- ✔ **Persistance du filtre**
  - Le filtre reste actif après navigation

### 📋 Classes utilisées :
- `ProductActions` : selectFilter(), getProductNames(), getProductPrices()
- `AuthActions` : login()
- `CommonActions` : takeScreenshot()

### 🎯 **Fonctionnalité couverte** : Filtrage et tri des produits

_______________________________________________________________________________

## 🛒 Tests du processus d'achat (checkout-process.spec.js)

Les tests valident le flux complet de l'ajout au panier jusqu'à la confirmation de commande :

### ✅ Scénarios couverts :

#### 1️⃣ **Flux d'achat complet - Succès**
- Connexion utilisateur (beforeAll - session partagée)
- Ajout d'un produit au panier
- Vérification du badge panier (affiche "1")
- Navigation vers le panier
- Vérification du produit dans le panier
- Clic sur "Checkout"
- Remplissage du formulaire (First Name, Last Name, ZIP Code)
- Clic sur "Continue"
- Vérification de la page de récapitulatif
- Vérification du total et des produits
- Clic sur "Finish"
- Vérification du message de confirmation : "Thank you for your order!"
- Vérification que le badge panier disparaît

#### 2️⃣ **Validation du formulaire vide**
- Tentative de checkout sans remplir le formulaire
- Vérification du message d'erreur : "Error: First Name is required"

#### 3️⃣ **Annulation du checkout**
- Navigation vers le checkout
- Clic sur "Cancel"
- Retour au panier
- Vérification que le produit est toujours présent

#### 4️⃣ **Vérification du calcul des prix**
- Ajout de plusieurs produits
- Vérification du sous-total
- Vérification des taxes
- Vérification du total final

### 📋 Classes utilisées :
- `AuthActions` : login()
- `ProductActions` : addProductToCart(), verifyCartBadgeCount()
- `CartActions` : goToCart(), clearCart(), verifyProductInCart(), proceedToCheckout()
- `CheckoutActions` : fillCheckoutInfo(), continueToOverview(), finishPurchase(), verifyOrderConfirmation(), getTotalPrice()
- `CommonActions` : takeScreenshot(), waitForPageLoad()

### 🎯 **Fonctionnalité couverte** : Processus d'achat complet (E2E)

### ⚡ **Optimisation importante** :
- **Session partagée** : Les 4 tests utilisent la même connexion (définie dans `beforeAll`)
- **Nettoyage du panier** : `beforeEach` nettoie le panier entre chaque test
- **Isolation** : Chaque test part d'un état propre mais sans se reconnecter

_______________________________________________________________________________

## 📊 Structure des données

### 📄 steps.json
```json
{
  "config": {
    "baseURL": "https://www.saucedemo.com"
  },
  "products": {
    "backpack": "Sauce Labs Backpack",
    "bikeLight": "Sauce Labs Bike Light",
    "onesie": "Sauce Labs Onesie"
  },
  "checkout": {
    "testCustomer": {
      "firstName": "Test",
      "lastName": "User",
      "zipCode": "12345"
    },
    "confirmationMessage": "Thank you for your order!"
  },
  "filters": {
    "nameAsc": "Name (A to Z)",
    "nameDesc": "Name (Z to A)",
    "priceLowHigh": "Price (low to high)",
    "priceHighLow": "Price (high to low)"
  }
}
```

### 👤 users.json
```json
{
  "users": [
    {
      "type": "standard",
      "username": "standard_user",
      "password": "secret_sauce"
    },
    {
      "type": "locked",
      "username": "locked_out_user",
      "password": "secret_sauce"
    },
    {
      "type": "problem",
      "username": "problem_user",
      "password": "secret_sauce"
    }
  ]
}
```

_______________________________________________________________________________

## 🚀 Commandes d'exécution

### Installation
```bash
npm install
npm run install:browsers
```

### Exécution des tests
```bash
# Tous les tests (headless)
npm test

# Tests avec interface visible
npm test:headed

# Mode UI interactif
npm test:ui

# Mode debug
npm test:debug
```

### Exécution par fichier
```bash
# Tests de login uniquement
npm run test:login

# Tests de filtrage uniquement
npm run test:filter

# Tests de checkout uniquement
npm run test:checkout
```

### Rapports
```bash
# Afficher le rapport HTML
npm run show:report
```

_______________________________________________________________________________

## 📊 Rapport Playwright

Après chaque exécution, Playwright génère automatiquement un rapport HTML interactif dans `playwright-report/` contenant :

- ✔ Résultat de chaque test (✅ PASS / ❌ FAIL)
- 📸 Screenshots capturés pendant l'exécution
- 🎥 Vidéos des scénarios échoués
- 🧵 Traces Playwright pour le debug détaillé
- ⏱ Temps d'exécution par test
- 📊 Statistiques globales

**Emplacement des artefacts** :
- `screenshots/` : Captures d'écran des étapes clés
- `test-results/` : Résultats JSON et JUnit
- `playwright-report/` : Rapport HTML interactif

_______________________________________________________________________________

## 🧹 Bonnes pratiques appliquées

### ✅ Architecture
- **Page Object Model (POM)** : Séparation claire des responsabilités
- **Action Classes** : Logique métier réutilisable
- **Data-Driven Testing** : Données séparées du code
- **DRY Principle** : Pas de duplication de code

### ✅ Qualité
- **Assertions explicites** : expect() avec messages clairs
- **Gestion d'erreurs** : try/catch appropriés
- **Attentes intelligentes** : Auto-wait de Playwright
- **Screenshots automatiques** : Documentation visuelle

### ✅ Performance
- **Session partagée** : Connexion unique pour checkout-process.spec.js
- **Nettoyage sélectif** : beforeEach nettoie seulement si nécessaire
- **Exécution séquentielle** : workers: 1 (pour stabilité)

### ✅ Maintenabilité
- **Sélecteurs centralisés** : actionMap.js
- **Documentation** : Commentaires JSDoc
- **Logs structurés** : console.log avec émojis
- **Versionning** : Git + .gitignore approprié

_______________________________________________________________________________

## ⚙️ Configuration Playwright

### Paramètres clés (playwright.config.js)
```javascript
{
  testDir: './tests/specs',
  timeout: 90000,              // 90 secondes par test
  workers: 1,                  // Exécution séquentielle
  retries: 1,                  // 1 retry en cas d'échec
  headless: true,              // Mode headless par défaut
  screenshot: 'on',            // Screenshots sur tous les tests
  video: 'retain-on-failure'   // Vidéo uniquement en cas d'échec
}
```

### Projet ciblé
- **Navigateur** : Chrome uniquement
_______________________________________________________________________________

## 📈 Couverture de test

### ✅ Fonctionnalités testées (E2E)

| Module                | Couverture | Tests                                                                             |
|-----------------------|------------|-----------------------------------------------------------------------------------|
| **Authentification**  | 100%       | ✅ Login réussi<br>✅ Login échoué<br>✅ Logout                                  |
| **Filtrage produits** | 100%       | ✅ Tri A→Z<br>✅ Tri Z→A<br>✅ Prix Low→High<br>✅ Prix High→Low                |
| **Processus d'achat** | 100%       | ✅ Achat complet<br>✅ Validation formulaire<br>✅ Annulation<br>✅ Calcul prix |
_______________________________________________________________________________

## 🔄 CI/CD Integration

### Configuration recommandée

#### GitHub Actions
```yaml
- name: Install dependencies
  run: npm ci
  
- name: Install Playwright Browsers
  run: npx playwright install chrome

- name: Run Playwright tests
  run: npm test

- name: Upload test results
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

### Variables d'environnement CI
- `CI=true` : Active le mode CI (2 retries)
- `DEBUG=false` : Désactive le slow motion

_______________________________________________________________________________

## 📚 Ressources

### Documentation
- [Playwright Official Docs](https://playwright.dev/)
- [SauceDemo Test Site](https://www.saucedemo.com/)

### Support
- **Issues** : [GitHub Issues](https://github.com/hazmiabir/UTopiaFinalAbirHazmi/issues)

_______________________________________________________________________________

## ✅ Conclusion

Cette suite de tests Playwright permet de :
- ✅ **Sécuriser les fonctionnalités critiques** de l'application SauceDemo
- ✅ **Détecter rapidement les régressions UI** après chaque modification
- ✅ **Garantir la stabilité** des flux utilisateurs principaux
- ✅ **Améliorer la qualité globale** grâce aux rapports détaillés
- ✅ **Faciliter la maintenance** via une architecture modulaire et bien documentée

**Version** : 1.0.0  
**Dernière mise à jour** : Janvier 2025  
**Licence** : ISC

# SauceDemo Burger Menu Test Suite

Automated **Robot Framework** test suite for validating the **burger menu navigation** on [SauceDemo](https://www.saucedemo.com/).  
Tests are organized by **user type** and **menu functionality**, with robust logging and modular keywords.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [Running Tests](#running-tests)  
- [Test Design](#test-design)  
- [Extending Tests](#extending-tests)  

---

## Overview

This suite verifies the behavior of the **burger menu** for different users:

- **Standard User**: All menu options functional.
- **Problem User**: Known issues handled gracefully.
- **Locked User**: Login attempts fail with appropriate error (commented out in suite).  

It uses **modular keywords** to encapsulate browser actions, login steps, and menu interactions for reusability and maintainability.

---

## Features

- Open/close burger menu  
- Verify menu options presence (`All Items`, `About`, `Reset App State`, `Logout`)  
- Navigate to external links (`About`) with verification and return  
- Reset app state and validate cart and buttons  
- Logout and verify return to login page  
- Modular, reusable keywords for step-level logging and error handling  
- Known issue management for problem users  

---

## Project Structure

project/
│
├── Tests/
│ └── BurgerMenu.robot # Main Robot Framework test suite
│
├── Resources/
│ ├── Libraries/
│ │ ├── BrowserKeywords.py
│ │ ├── LoginKeywords.py
│ │ └── BurgerMenuKeywords.py
│ └── Variables/
│ └── Configuration.py # URLs, user credentials, selectors, timeouts
│
└── Reports/ # Test execution logs and reports