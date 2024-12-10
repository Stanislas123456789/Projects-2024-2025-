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
    while time.time() - start_time < 50:  # Répéter pendant 50 secondes
        try:
            # Placer un ordre limite d'achat à 99.50
            driver.find_element(By.ID, 'montant_ordre').clear()
            driver.find_element(By.ID, 'montant_ordre').send_keys('3000')  # Montant à acheter
            type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
            type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Limit order (LMT)"
            driver.find_element(By.ID, 'limite_ordre').clear()
            driver.find_element(By.ID, 'limite_ordre').send_keys('99.55')  # Limite d'achat à 99.55
            driver.find_element(By.XPATH, "//input[@value='Buy']").click()
            print("Ordre limite d'achat placé à 99.55.")

            # Attendre 2 secondes avant de placer l'ordre de vente
            time.sleep(0.5)

            # Placer un ordre limite de vente à 101.55
            driver.find_element(By.ID, 'qte_ordre').clear()
            driver.find_element(By.ID, 'qte_ordre').send_keys('100')  # Quantité à vendre
            type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
            type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Limit order (LMT)"
            driver.find_element(By.ID, 'limite_ordre').clear()
            driver.find_element(By.ID, 'limite_ordre').send_keys('101.50')  # Limite de vente à 101.50
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
                print(f"Ordre d'achat exécuté pour {cash_disponible} €. ")
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

# Fonction pour optimiser les profits
def optimiser_profits():
    while True:
        try:
            # Récupérer le prix actuel
            prix_actuel = float(driver.find_element(By.ID, 'prix_actuel').get_attribute('value'))  # Assurez-vous que l'ID est correct
            titres_disponibles = float(driver.find_element(By.ID, 'nb_titres_disponibles').get_attribute('value'))

            # Vente de 25% si le prix atteint 116
            if prix_actuel >= 116 and titres_disponibles > 0:
                quantite_a_vendre = titres_disponibles * 0.25
                driver.find_element(By.ID, 'qte_ordre').clear()
                driver.find_element(By.ID, 'qte_ordre').send_keys(str(quantite_a_vendre))  # Quantité à vendre
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Market Order"
                driver.find_element(By.XPATH, "//input[@value='Sell']").click()
                print(f"Ordre de vente exécuté pour {quantite_a_vendre} titres à {prix_actuel} €.")
                time.sleep(2)  # Attendre un peu avant la prochaine vérification

            # Vente avec un ordre limite si le prix atteint 120
            elif prix_actuel >= 120 and titres_disponibles > 0:
                quantite_a_vendre = titres_disponibles
                driver.find_element(By.ID, 'qte_ordre').clear()
                driver.find_element(By.ID, 'qte_ordre').send_keys(str(quantite_a_vendre))  # Vendre tous les titres disponibles
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Limit Order"
                driver.find_element(By.ID, 'limite_ordre').clear()
                driver.find_element(By.ID, 'limite_ordre').send_keys(str(prix_actuel))  # Limite à prix actuel
                driver.find_element(By.XPATH, "//input[@value='Sell']").click()
                print(f"Ordre limite de vente exécuté pour {quantite_a_vendre} titres à {prix_actuel} €.")
                time.sleep(2)  # Attendre un peu avant la prochaine vérification

            # Achat de 25% si le prix atteint 89
            elif prix_actuel <= 89 and titres_disponibles < 100:  # Par exemple, supposons que vous n'avez pas d'actions
                cash_disponible = float(driver.find_element(By.ID, 'montant_cash_disponible').get_attribute('value'))
                quantite_a_acheter = cash_disponible * 0.25
                driver.find_element(By.ID, 'montant_ordre').clear()
                driver.find_element(By.ID, 'montant_ordre').send_keys(str(quantite_a_acheter))
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Market Order"
                driver.find_element(By.XPATH, "//input[@value='Buy']").click()
                print(f"Ordre d'achat exécuté pour {quantite_a_acheter} € à {prix_actuel} €.")
                time.sleep(2)  # Attendre un peu avant la prochaine vérification

            # Achat de 25% si le prix atteint 80
            elif prix_actuel <= 80 and titres_disponibles < 100:
                cash_disponible = float(driver.find_element(By.ID, 'montant_cash_disponible').get_attribute('value'))
                quantite_a_acheter = cash_disponible * 0.25
                driver.find_element(By.ID, 'montant_ordre').clear()
                driver.find_element(By.ID, 'montant_ordre').send_keys(str(quantite_a_acheter))
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Market Order"
                driver.find_element(By.XPATH, "//input[@value='Buy']").click()
                print(f"Ordre d'achat exécuté pour {quantite_a_acheter} € à {prix_actuel} €.")
                time.sleep(2)  # Attendre un peu avant la prochaine vérification

            # Achat de 50% si le prix atteint 78
            elif prix_actuel <= 78 and titres_disponibles < 100:
                cash_disponible = float(driver.find_element(By.ID, 'montant_cash_disponible').get_attribute('value'))
                quantite_a_acheter = cash_disponible * 0.50
                driver.find_element(By.ID, 'montant_ordre').clear()
                driver.find_element(By.ID, 'montant_ordre').send_keys(str(quantite_a_acheter))
                type_ordre_dropdown = Select(driver.find_element(By.ID, 'type_ordre'))
                type_ordre_dropdown.select_by_value('LIM')  # Sélectionner "Market Order"
                driver.find_element(By.XPATH, "//input[@value='Buy']").click()
                print(f"Ordre d'achat exécuté pour {quantite_a_acheter} € à {prix_actuel} €.")
                time.sleep(2)  # Attendre un peu avant la prochaine vérification

            time.sleep(1)  # Attendre un peu avant de vérifier à nouveau
        except Exception as e:
            print(f"Erreur lors de l'optimisation des profits : {e}")
            time.sleep(2)

# Code principal
if __name__ == "__main__":
    connecter()
    acceder_simulation()
    placer_ordres_limites()
    lire_nouvelles() 
    executer_ordre # Surveiller les nouvelles en permanence
    
    # Boucle principale pour surveiller les prix et optimiser les profits
    optimiser_profits()
