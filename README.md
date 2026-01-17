# 🧪 Projet CORP QA - Automatisation de Tests Saucedemo

## 📋 Description du Projet

Ce projet d'automatisation de tests a pour objectif de valider les fonctionnalités principales de l'application **Saucedemo.com** à travers une suite de tests automatisés utilisant différentes technologies et frameworks.

### Objectifs
- ✅ Automatiser les scénarios de test critiques de l'application Saucedemo
- ✅ Mettre en place une intégration continue avec Jenkins
- ✅ Gérer les cas de test et résultats avec JIRA XRAY
- ✅ Démontrer la maîtrise de plusieurs frameworks de test (Playwright, Selenium, Robot Framework)

### Technologies Utilisées
- **JavaScript + Playwright** : Tests E2E modernes
- **Python + Selenium** : Automatisation de navigateur
- **Robot Framework** : Framework basé sur mots-clés
- **JIRA XRAY** : Gestion des cas de test
- **Jenkins** : Intégration continue
- **Git** : Versionnement du code

### Application Testée
- **URL** : https://www.saucedemo.com
- **Identifiants de test** :
  - Utilisateur standard : `standard_user` / `secret_sauce`
  - Utilisateur avec problème : `problem_user` / `secret_sauce`
  - Utilisateur verrouillé : `locked_out_user` / `secret_sauce`

---

## 🔧 Prérequis d'Installation

### Logiciels Requis

#### 1. Node.js et npm
- **Version** : Node.js 18.x ou supérieur
- **Installation** : Télécharger depuis [nodejs.org](https://nodejs.org/)
- **Vérification** :
  ```bash
  node --version
  npm --version
  ```

#### 2. Python
- **Version** : Python 3.8 ou supérieur
- **Installation** : Télécharger depuis [python.org](https://www.python.org/)
- **Vérification** :
  ```bash
  python --version
  pip --version
  ```

#### 3. Git
- **Installation** : Télécharger depuis [git-scm.com](https://git-scm.com/)
- **Vérification** :
  ```bash
  git --version
  ```

#### 4. Jenkins (optionnel pour exécution locale)
- **Installation** : Télécharger depuis [jenkins.io](https://www.jenkins.io/)
- **Plugins requis** :
  - Pipeline
  - HTML Publisher
  - JUnit
  - NodeJS

### Installation des Dépendances du Projet

#### 1. Cloner le dépôt
```bash
git clone https://github.com/votre-username/automation-project-saucedemo.git
cd automation-project-saucedemo
```

#### 2. Installation des dépendances JavaScript (Playwright)
```bash
cd playwright_tests
npm install
npx playwright install --with-deps
cd ..
```

#### 3. Installation des dépendances Python (Selenium + Robot Framework)
```bash
pip install -r requirements.txt
```

**Contenu du fichier `requirements.txt`** :
```
selenium==4.15.0
robotframework==6.1.1
robotframework-seleniumlibrary==6.1.3
webdriver-manager==4.0.1
```

---

## 🚀 Instructions d'Exécution des Tests

### Exécution des Tests Playwright (JavaScript)

#### Tous les tests Playwright
```bash
cd playwright_tests
npx playwright test
```

#### Test spécifique
```bash
npx playwright test tests/product-filtering.spec.js
npx playwright test tests/checkout-process.spec.js
```

#### Mode headed (avec interface graphique)
```bash
npx playwright test --headed
```

#### Choix du navigateur
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

#### Visualiser le rapport HTML
```bash
npx playwright show-report
```

---

### Exécution des Tests Selenium (Python)

#### Tous les tests Selenium
```bash
cd selenium_tests
python -m pytest tests/ -v
```

#### Test spécifique
```bash
python -m pytest tests/test_login_errors.py -v
python -m pytest tests/test_product_verification.py -v
```

#### Avec rapport HTML
```bash
python -m pytest tests/ -v --html=reports/selenium_report.html
```

---

### Exécution des Tests Robot Framework

#### Tous les tests Robot Framework
```bash
cd robot_tests
robot tests/
```

#### Test spécifique
```bash
robot tests/burger_menu_navigation.robot
```

#### Avec rapport personnalisé
```bash
robot --outputdir reports tests/
```

#### Visualiser les rapports
- Ouvrir `robot_tests/reports/report.html` dans un navigateur

---

### Exécution via Jenkins

#### Pipeline complet
1. Accéder à Jenkins : `http://localhost:8080`
2. Sélectionner le job **"Saucedemo-All-Tests"**
3. Cliquer sur **"Build with Parameters"**
4. Choisir les paramètres :
   - **BROWSER** : chromium / firefox / webkit / all
   - **HEADED_MODE** : true / false
5. Cliquer sur **"Build"**

#### Consulter les rapports
- **Rapport Playwright** : Disponible dans les artifacts Jenkins
- **Rapport JUnit** : Onglet "Test Result" du build
- **Rapport HTML** : Lien "Rapport HTML Playwright" dans le build

---

## 📁 Explication de la Structure du Projet

```
automation-project-saucedemo/
│
├── playwright_tests/               # Tests Playwright (JavaScript)
│   ├── tests/
│   │   ├── product-filtering.spec.js      # Test 1: Filtrage produits
│   │   └── checkout-process.spec.js       # Test 2: Processus paiement
│   ├── playwright.config.js        # Configuration Playwright
│   ├── package.json               # Dépendances Node.js
│   └── package-lock.json
│
├── selenium_tests/                # Tests Selenium (Python)
│   ├── tests/
│   │   ├── test_login_errors.py          # Test 3: Erreurs connexion
│   │   └── test_product_verification.py  # Test 4: Vérification produits
│   ├── pages/                     # Page Object Model
│   │   ├── login_page.py
│   │   └── products_page.py
│   └── conftest.py                # Configuration pytest
│
├── robot_tests/                   # Tests Robot Framework
│   ├── tests/
│   │   └── burger_menu_navigation.robot  # Test 5: Menu burger
│   ├── resources/
│   │   ├── keywords.robot         # Mots-clés personnalisés
│   │   └── variables.robot        # Variables globales
│   └── reports/                   # Rapports générés
│       ├── log.html
│       ├── report.html
│       └── output.xml
│
├── jenkins/                       # Configuration Jenkins
│   ├── Jenkinsfile               # Pipeline principal
│   └── jobs/                     # Jobs individuels
│       ├── playwright-job.groovy
│       ├── selenium-job.groovy
│       └── robot-job.groovy
│
├── reports/                       # Rapports consolidés
│   ├── html-report/              # Rapports HTML
│   ├── junit-results/            # Résultats JUnit
│   └── screenshots/              # Captures d'écran
│
├── .gitignore                    # Fichiers à ignorer par Git
├── requirements.txt              # Dépendances Python
└── README.md                     # Ce fichier
```

### Description des Répertoires Principaux

#### `playwright_tests/`
Contient tous les tests E2E écrits avec Playwright et JavaScript. Chaque test est structuré avec des hooks `beforeAll` pour la configuration et des assertions robustes.

**Tests inclus** :
- **Test 1** : Filtrage des produits et vérification de l'ordre
- **Test 2** : Processus de paiement complet

#### `selenium_tests/`
Tests d'automatisation utilisant Selenium WebDriver avec Python. Utilise le pattern Page Object Model pour une meilleure maintenabilité.

**Tests inclus** :
- **Test 3** : Gestion des erreurs de connexion
- **Test 4** : Navigation et vérification des produits

#### `robot_tests/`
Tests écrits avec Robot Framework utilisant une approche par mots-clés. Les ressources sont séparées pour faciliter la réutilisation.

**Tests inclus** :
- **Test 5** : Navigation dans le menu burger

#### `jenkins/`
Fichiers de configuration pour l'intégration continue avec Jenkins. Le Jenkinsfile définit le pipeline complet d'exécution des tests.

#### `reports/`
Répertoire de sortie pour tous les rapports de tests générés (HTML, XML, JSON, screenshots).

---

## 📊 Intégration JIRA XRAY

### Projet JIRA
- **Nom** : CORP-CSF-SAUCEDEMO-TEST
- **Template** : SCRUM

### Cas de Test Créés
1. **CCS-1** : Filtrage produits (Playwright)
2. **CCS-2** : Processus paiement (Playwright)
3. **CCS-3** : Erreurs connexion (Selenium Python)
4. **CCS-4** : Vérification produits (Selenium Python)
5. **CCS-5** : Navigation menu burger (Robot Framework)

### Dashboard XRAY
Le dashboard inclut :
- Résumé des tests (PASS/FAIL)
- Progression des tests
- Historique d'exécution
- Répartition par technologie

---

## 🐛 Dépannage

### Erreur : "Playwright not found"
```bash
cd playwright_tests
npm install
npx playwright install
```

### Erreur : "Selenium module not found"
```bash
pip install -r requirements.txt
```

### Erreur : "ChromeDriver version mismatch"
```bash
pip install --upgrade webdriver-manager
```

### Tests instables
- Augmenter les timeouts dans les configurations
- Vérifier la connexion internet
- S'assurer que Saucedemo.com est accessible

---

## 👥 Contributeurs

- **Nom du Candidat 1** - Tests Playwright
- **Nom du Candidat 2** - Tests Selenium
- **Nom du Candidat 3** - Tests Robot Framework
- **Formateur** - Supervision et revue

---

## 📝 Licence

Ce projet est réalisé dans le cadre d'une formation en automatisation de tests.

---

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Contacter le formateur
- Consulter la documentation des frameworks :
  - [Playwright Docs](https://playwright.dev/)
  - [Selenium Docs](https://www.selenium.dev/)
  - [Robot Framework Docs](https://robotframework.org/)

---

**Dernière mise à jour** : Janvier 2026  
**Version** : 1.0.0
