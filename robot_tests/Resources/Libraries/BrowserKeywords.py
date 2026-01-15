from robot.api.deco import keyword
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import os

class BrowserKeywords:
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self.driver = None
        self.config = self._load_config()
    
    def _load_config(self):
        """Charge la configuration depuis le fichier JSON"""
        config_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'Variables', 'config.json'
        )
        with open(config_path, 'r') as f:
            return json.load(f)

    @keyword("Open Browser To URL")
    def open_browser_to_url(self, url=None):
        if url is None:
            url = self.config['urls']['base_url']

        if not self.driver:
            options = webdriver.ChromeOptions()

            # 🔥 REQUIRED FOR DOCKER
            options.binary_location = "/usr/bin/chromium"
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(self.config['timeouts']['default'])

        self.driver.get(url)

        WebDriverWait(self.driver, self.config['timeouts']['default']).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        print(f"✓ Navigateur ouvert à : {url}")

    @keyword("Close Browser")
    def close_browser(self):
        """Ferme le navigateur et nettoie les ressources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✓ Navigateur fermé")

    @keyword("Get Current URL")
    def get_current_url(self):
        """Retourne l'URL actuelle"""
        return self.driver.current_url

    @keyword("Switch To New Window")
    def switch_to_new_window(self):
        """Bascule vers la nouvelle fenêtre/onglet"""
        # Attendre qu'il y ait au moins 2 fenêtres
        WebDriverWait(self.driver, self.config['timeouts']['default']).until(
            lambda d: len(d.window_handles) > 1
        )
        # Basculer vers la dernière fenêtre ouverte
        self.driver.switch_to.window(self.driver.window_handles[-1])
        print(f"✓ Basculé vers la nouvelle fenêtre")

    @keyword("Switch To Main Window")
    def switch_to_main_window(self):
        """Bascule vers la fenêtre principale (première fenêtre)"""
        self.driver.switch_to.window(self.driver.window_handles[0])
        print("✓ Retour à la fenêtre principale")

    @keyword("Close Current Window")
    def close_current_window(self):
        """Ferme la fenêtre/onglet actuel"""
        self.driver.close()

    @keyword("Get Window Count")
    def get_window_count(self):
        """Retourne le nombre de fenêtres/onglets ouverts"""
        return len(self.driver.window_handles)

    @keyword("URL Should Contain")
    def url_should_contain(self, expected_text):
        """Vérifie que l'URL contient le texte attendu"""
        current_url = self.driver.current_url
        assert expected_text in current_url, \
            f"URL '{current_url}' ne contient pas '{expected_text}'"
        print(f"✓ URL contient '{expected_text}'")

    @keyword("Page Should Contain Element")
    def page_should_contain_element(self, locator_type, locator_value):
        """Vérifie que la page contient l'élément spécifié"""
        wait = WebDriverWait(self.driver, self.config['timeouts']['default'])
        by = getattr(By, locator_type.upper())
        element = wait.until(EC.presence_of_element_located((by, locator_value)))
        print(f"✓ Élément trouvé : {locator_type}={locator_value}")