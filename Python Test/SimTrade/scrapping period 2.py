import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

# Configurer ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Chemin vers votre chromedriver
service = Service(r"C:\Program Files\Google\chromedriver-win64\chromedriver.exe")

# Démarrer Chrome avec Selenium
driver = webdriver.Chrome(service=service, options=chrome_options)

# Fonction de connexion à la simulation
def connecter():
    try:
        driver.get("https://www.simtrade.fr/CCMP/ESSEC_BBA/site/certifications/certifications_presentation.php?n=C&c=CERTIF2_US_FINANCE_ESSEC_BBA_2024_09&p=ESSEC2&lang=us#")
        
        # Connexion
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'LOG IN'))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'nom_v3')))
        driver.find_element(By.ID, 'nom_v3').send_keys('B00805678@essec.edu')  # Remplacez par votre identifiant
        driver.find_element(By.ID, 'motdepasse_v3').send_keys('@Stan1244')  # Remplacez par votre mot de passe
        driver.find_element(By.XPATH, "//input[@value='Log in']").click()
    except WebDriverException as e:
        print(f"Erreur de connexion : {e}")

# Accéder à la simulation
def acceder_simulation():
    try:
        time.sleep(1)
        driver.find_element(By.XPATH, "//a[contains(@href, 'challenges_presentation_certificat.php') and contains(., 'CONTESTS')]").click()
        driver.find_element(By.XPATH, "//a[contains(@href, 'challenges_presentation.php?n=C&c=CONC_BDF7_US_V7_ESSEC_BBA')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@value='Launch the simulation']").click()
        time.sleep(2)  # Attendre que la simulation soit prête
    except WebDriverException as e:
        print(f"Erreur lors de l'accès à la simulation : {e}")

# Fonction pour lire les nouvelles dans le bandeau défilant (Relocalisation systématique)
def lire_nouvelles():
    for attempt in range(3):  # Essayer jusqu'à 3 fois
        try:
            # Utiliser WebDriverWait pour attendre la présence de l'élément
            news_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#simulation_bandeau_Defilant .tickercontainer"))
            )
            news_text = news_element.text
            return news_text
        except (StaleElementReferenceException, WebDriverException) as e:
            print(f"Tentative {attempt + 1} de relire l'élément à cause de : {e}")
            time.sleep(1)  # Attendre 1 seconde avant de réessayer
    return ""

# Fonction pour placer des ordres limites d'achat et de vente
def placer_ordres_limites():
    start_time = time.time()
    while time.time() - start_time < 50:  # Répéter pendant 35 secondes
        try:
            # Placer un ordre limite d'achat à 99.50
            driver.find_element(By.ID, 'montant_ordre').clear()
            driver.find_element(By.ID, 'montant_ordre').send_keys('6000')  # Montant à acheter
            type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
            type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Limit order (LMT)"
            driver.find_element(By.ID, 'limite_ordre').clear()
            driver.find_element(By.ID, 'limite_ordre').send_keys('99.55')  # Limite d'achat à 99.50
            driver.find_element(By.XPATH, "//input[@value='Buy']").click()
            print("Ordre limite d'achat placé à 99.50.")

            # Attendre 2 secondes avant de placer l'ordre de vente
            time.sleep(0.5)

            # Placer un ordre limite de vente à 101.55
            driver.find_element(By.ID, 'qte_ordre').clear()
            driver.find_element(By.ID, 'qte_ordre').send_keys('100')  # Quantité à vendre
            type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
            type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Limit order (LMT)"
            driver.find_element(By.ID, 'limite_ordre').clear()
            driver.find_element(By.ID, 'limite_ordre').send_keys('101.50')  # Limite de vente à 101.55
            driver.find_element(By.XPATH, "//input[@value='Sell']").click()
            print("Ordre limite de vente placé à 101.50.")
        except WebDriverException as e:
            print(f"Erreur lors du placement des ordres limites : {e}")

# Fonction pour analyser les recommandations et l'indice de confiance
def analyser_recommandation(news_text):
    if "The FAO predicts less severe droughts in China" in news_text:
        return "vendre"
    elif "The FAO predicts more severe droughts in China" in news_text:
        return "acheter"
    
    if "BDF announces a profit for last year of €620 m (consensus: €700 m)" in news_text:
        return "vendre"
    elif "BDF announces a profit for last year of €805 m (consensus: €700 m)" in news_text:
        return "acheter"
    
    if "8" in news_text:
        return "acheter"
    elif "6" in news_text:
        return "vendre"
    
    if "wins the tender offer" in news_text:
        return "acheter"
    elif "loses the tender offer" in news_text:
        return "vendre"
    
    if "lab discovers a remedy for the stem rust" in news_text:
        return "acheter"
    elif "Fire in wheat fields owned by BDF" in news_text:
        return "vendre"
    
    return None

# Fonction pour exécuter l'ordre d'achat ou de vente après la nouvelle
def executer_ordre(action):
    try:
        if action == "acheter":
            # Vérifier le montant de cash disponible
            cash_disponible = float(driver.find_element(By.ID, 'montant_cash_disponible').get_attribute('value'))
            if cash_disponible > 0:
                driver.find_element(By.ID, 'montant_ordre').clear()
                driver.find_element(By.ID, 'montant_ordre').send_keys(str(cash_disponible))  # Utiliser tout le cash disponible
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('MAR')  # Sélectionner "Market Order"
                driver.find_element(By.XPATH, "//input[@value='Buy']").click()
                print(f"Ordre d'achat exécuté pour {cash_disponible} €.")
            else:
                print("Pas de cash disponible pour l'achat.")

        elif action == "vendre":
            # Vérifier le nombre d'actifs disponibles
            titres_disponibles = float(driver.find_element(By.ID, 'nb_titres_disponibles').get_attribute('value'))
            if titres_disponibles > 0:
                driver.find_element(By.ID, 'qte_ordre').clear()
                driver.find_element(By.ID, 'qte_ordre').send_keys(str(titres_disponibles))  # Vendre tous les titres disponibles
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('MAR')  # Sélectionner "Market Order"
                driver.find_element(By.XPATH, "//input[@value='Sell']").click()
                print(f"Ordre de vente exécuté pour {titres_disponibles} titres.")
            else:
                print("Pas de titres disponibles pour la vente.")
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'ordre : {e}")

# Fonction principale pour surveiller en permanence les nouvelles
def surveiller_nouvelles():
    checked_news = set()  # Utiliser un ensemble pour stocker les nouvelles déjà vérifiées
    while True:
        try:
            news_text = lire_nouvelles()
            if news_text and news_text not in checked_news:  # Vérifier si la nouvelle a déjà été traitée
                checked_news.add(news_text)
                action = analyser_recommandation(news_text)

                if action:
                    print(f"Nouvelles détectées: {news_text}")
                    executer_ordre(action)
                else:
                    print("Nouvelle détectée, mais aucune action requise.")
            
            time.sleep(0.6)  # Attendre 1 seconde avant de vérifier les nouvelles à nouveau
        except WebDriverException as e:
            print(f"Erreur dans la boucle de décision : {e}")

# Lancer la fonction principale
if __name__ == "__main__":
    try:
        connecter()  # Connexion au site
        acceder_simulation()  # Accéder à la simulation
        print("Placement des ordres limites pendant 60 secondes.")
        placer_ordres_limites()  # Placer les ordres limites pendant 60 secondes

        print("Passage à la stratégie basée sur les nouvelles.")
        surveiller_nouvelles()  # Surveiller les nouvelles en permanence
    except KeyboardInterrupt:
        print("Arrêt du bot.")
    except WebDriverException as e:
        print(f"Erreur WebDriver : {e}")
    finally:
        # Assurez-vous de fermer correctement le navigateur
        driver.quit()

