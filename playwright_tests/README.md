🧪 Playwright Test Coverage – Documentation
_______________________________________________________________________________
📌 Objectif des tests
        Cette suite de tests Playwright automatise les tests end-to-end de l’application SauceDemo afin de valider les parcours utilisateurs principaux depuis le navigateur, avec un focus sur la stabilité de l’interface et la navigation.
        Les tests permettent de détecter rapidement les régressions UI après chaque modification du code.

🏗️ Architecture du projet
Diagramme d'architecture
┌─────────────────────────────────────────────────────────┐
│                    Tests (specs/)                        │
│         Scénarios de test métier lisibles                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├──► Actions (actions/)
                     │    Logique métier réutilisable
                     │
                     ├──► ActionMap (pages/)
                     │    Sélecteurs CSS centralisés
                     │
                     └──► Loader (utils/)
                          Chargement données JSON
📂 Structure détaillée
tests/
├── pages/
│   └── actionMap.js          # 🎯 Sélecteurs CSS/XPath centralisés
│                             # Tous les locators de l'application
│
├── actions/
│   └── actions.js            # 🔧 Actions réutilisables
│                             # login(), selectFilter(), verifyOrder()
│
├── utils/
│   └── loader.js             # 📂 Chargement des données JSON
│                             # loadSteps(), loadUsers()
│
├── data/
│   ├── steps.json            # 📊 Données de test
│   │                         # Credentials, messages d'erreur, filtres
│   └── users.json            # 👤 Configuration des utilisateurs
│                             # standard, problem, locked
│
└── specs/
    └── saucedemo-filter.spec.js  # ✅ Scénarios de test
                                   # Tests de filtrage et connexion

✅ Avantages de cette architecture
____________________________________________________________________________________________
Fichier         | Responsabilité              | En cas de changement
____________________________________________________________________________________________
actionMap.js    | Stocke tous les sélecteurs  | Si l'UI change → Modifier 1 seul fichier
____________________________________________________________________________________________
actions.js      | Définit les actions métier  | Si la logique change → Modifier actions
_____________________________________________________________________________________________
loader.js       | Charge les données          | Si le format change → Modifier loader
_____________________________________________________________________________________________
steps.json      | Contient les données        | Modifier données sans toucher au code
_____________________________________________________________________________________________
specs/*.spec.js | Décrit les tests            | Ajouter tests sans modifier l'infra
_____________________________________________________________________________________________


🔐 Tests d’authentification
        Les tests Playwright vérifient le processus de connexion à l’application :
                * Accès à la page de login
                * Saisie des identifiants utilisateur
                * Validation de la connexion réussie
                * Vérification de la redirection vers la page d’inventaire
                * Gestion des erreurs en cas de credentials invalides
        🎯 Fonctionnalité couverte : Login utilisateur

🛒 Tests de la page Inventaire (Produits)
        Les tests valident l’affichage correct de la liste des produits :
                * Présence de tous les produits attendus
                * Affichage des noms et des prix
                * Présence des images produits
                * Présence des boutons Add to cart
                * Vérification de la cohérence visuelle de la page
        🎯 Fonctionnalité couverte : Consultation des produits

🔍 Tests de navigation et filtres
        Les scénarios Playwright couvrent également :
                * Navigation entre les pages
                * Interaction avec les filtres de produits
                * Vérification de l’ordre ou du contenu affiché après filtrage
                * Validation du comportement dynamique de l’UI
        🎯 Fonctionnalité couverte : Navigation & filtrage

📄 Tests basés sur les données (Data-Driven)
        Les tests utilisent des données externes (JSON) pour :
                * Réutiliser les mêmes scénarios avec différents jeux de données
                * Rendre les tests plus maintenables
                * Séparer la logique de test des données fonctionnelles
        🎯 Améliore la lisibilité et la maintenabilité des tests

📊 Rapport Playwright
        Après chaque exécution, Playwright génère automatiquement un rapport HTML interactif contenant :
                ✔ Résultat de chaque test (PASS / FAIL)
                📸 Screenshots en cas d’échec
                🎥 Vidéos des scénarios échoués
                🧵 Traces Playwright pour le debug
                ⏱ Temps d’exécution par test

🧹 Bonnes pratiques appliquées
            * Page Object Model (POM)
            * Séparation claire (pages / actions / data / specs)
            * Tests lisibles et réutilisables
            * Assertions explicites
            * Rapports automatiques
            * Compatible CI/CD

⚠️ Limitations
            * Tests dépendants de l’interface utilisateur
            * Sensibles aux changements visuels
            * Ne couvrent pas :
               - les performances
               - la sécurité
               - les tests de charge

✅ Conclusion
            Cette suite de tests Playwright permet de :
                * sécuriser les fonctionnalités clés de l’application,
                * détecter rapidement les régressions UI,
                * améliorer la qualité globale du produit.               