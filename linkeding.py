import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# Configurar el navegador y sus opciones
def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")  # Inicia el navegador maximizado
    # options.add_argument("--disable-notifications")  # Desactiva notificaciones
    options.add_argument("--log-level=3")  # Suprime mensajes de nivel INFO, WARNING y SEVERE
    # options.add_argument("--silent")  # Opcional: silencia aún más el navegador

    # Crear instancia del navegador
    return webdriver.Chrome(options=options)

# Función principal
def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)  # Configurar espera explícita de 10 segundos

    try:
        while True:
            try:
                # Navegar a Google
                driver.get("https://www.linkedin.com/jobs/")

                username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "session_key")))
                break
            except TimeoutException:
                print("Se produjo un error al navegar a Google. Intentando nuevamente...")
        
        username_input.send_keys("espitiasanchezsebastian64@gmail.com")       
        password_input = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
        password_input.send_keys("Boneflecher01")
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(2)
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='artdeco-button__text' and text()='Mostrar todo']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='SaIePOlfaiarZvgCmWDzKoYPsqHgnMjGroRHA t-black link-without-visited-state jobs-search-discovery-tabs__tab' and text()='Solicitud sencilla']"))).click()

        time.sleep(3)
        offers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'scaffold-layout__list-item')]")))
        for index, offer in enumerate(offers):
            offer.click()
            offer_text = offer.text
            print(offer_text, '\n\n')
            
            solicitado = True if driver.find_elements(By.XPATH, "//span[@class='artdeco-inline-feedback__message']") else False
            print('\n\n1\n\n')
            if solicitado:
                print('Solicitado\n\n')
                continue
            else:
                print('\n\n2\n\n')
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='jobs-search__job-details--wrapper']//button[contains(@class, 'jobs-apply-button')]"))).click()
                print('\n\n3\n\n')
                
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']"))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']"))).click()
            
        # ember-view
    except Exception as e:
        print(f"Se produjo un error: {e}")
    finally:
        # Cerrar el navegador
        input("Presiona enter para salir")
        driver.quit()

if __name__ == "__main__":
    main()
