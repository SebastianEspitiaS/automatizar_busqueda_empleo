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
    options.add_argument("--disable-notifications")  # Desactiva notificaciones
    options.add_argument("--log-level=3")  # Suprime mensajes de nivel INFO, WARNING y SEVERE
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Elimina el mensaje de automatización
    options.add_argument("--force-device-scale-factor=0.8")  # Establecer el zoom al 80%
    options.add_argument("--silent")  # Opcional: silencia aún más el navegador

    # Crear instancia del navegador
    return webdriver.Chrome(options=options)

# Función principal
def main():
    driver = setup_driver()
    wait_five_second = WebDriverWait(driver, 5)  # Configurar espera explícita de 3 segundos

    try:
        while True:
            try:
                # Navegar a Google
                driver.get("https://www.linkedin.com/jobs/")

                print("Esperando el campo de usuario...")
                username_input = wait_five_second.until(EC.presence_of_element_located((By.ID, "session_key")))
                print("Campo de usuario encontrado.")
                break
            except TimeoutException:
                print("Se produjo un error al navegar a Google. Intentando nuevamente...")

        print("Enviando nombre de usuario...")
        username_input.send_keys("espitiasanchezsebastian64@gmail.com")
        print("Esperando el campo de contraseña...")
        password_input = wait_five_second.until(EC.presence_of_element_located((By.ID, "session_password")))
        print("Campo de contraseña encontrado.")
        print("Enviando contraseña...")
        password_input.send_keys("Boneflecher01")
        password_input.send_keys(Keys.RETURN)

        print("Esperando 2 segundos...")
        time.sleep(2)
        print("Refrescando la página...")
        driver.refresh()
        print("Esperando botón 'Mostrar todo'...")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='artdeco-button__text' and text()='Mostrar todo']"))).click()
        print("Botón 'Mostrar todo' clickeado.")

        print("Esperando enlace 'Solicitud sencilla'...")
        wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 't-black link-without-visited-state jobs-search-discovery-tabs__tab') and text()='Solicitud sencilla']"))).click()
        print("Enlace 'Solicitud sencilla' clickeado.")

        time.sleep(3)
        print("Esperando ofertas de trabajo...")
        offers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'scaffold-layout__list-item')]")))
        print(f"Se encontraron {len(offers)} ofertas de trabajo.")
        for index, offer in enumerate(offers):
            try:
                print(f"Procesando oferta {index + 1}...")
                offer.click()
                offer_text = offer.text
                print(f"Texto de la oferta: {offer_text}\n\n")
                
                try:
                    solicitado = True if driver.find_elements(By.XPATH, "//span[@class='artdeco-inline-feedback__message']") else False
                    print("Verificando si ya se ha solicitado...")
                    print('\n\n1\n\n')
                    if solicitado:
                        print('Ya se ha solicitado esta oferta.\n\n')
                        continue
                except Exception as e:
                    print(f"Error al verificar si la oferta ya fue solicitada")
                    pass

                print('\n\n2\n\n')
                try:
                    print("Clickeando en el botón de 'Solicitar empleo'...")
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='jobs-apply-button--top-card']"))).click()
                    print('\n\n3\n\n')
                except TimeoutException as e:
                    print(f"Error al intentar hacer clic en 'Solicitar empleo': {e}")
                    pass

                try:
                    print("Clickeando en el botón de 'Siguiente'...")
                    time.sleep(1)
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']"))).click()
                    print("Botón 'Siguiente' clickeado.")
                except TimeoutException as e:
                    print(f"Error al intentar hacer clic en el botón de 'Siguiente'")
                    pass

                try:
                    print("Clickeando en el botón de 'Siguiente 2'...")
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']"))).click()
                    print("Botón 'Siguiente 2' clickeado.")
                except TimeoutException as e:
                    print(f"Error al intentar hacer clic en el botón de 'Siguiente 2'")
                    pass
                except Exception as e:
                    pass

                try:
                    wait_five_second.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='t-16 t-bold' and text()='Additional Questions']")))
                    print('Todavia no esta implementado responder preguntas adicionales.\n\n')
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Descartar']"))).click()
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']"))).click()
                    continue
                except TimeoutException:
                    try:
                        wait_five_second.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='t-16 t-bold' and text()='Preguntas adicionales']")))
                        print('Todavia no esta implementado responder preguntas adicionales.\n\n')
                        wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Descartar']"))).click()
                        wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']"))).click()
                        continue
                    except TimeoutException:
                        pass

                try:
                    print("Clickeando en el botón de 'Enviar'...")
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']"))).click()
                    print("Botón 'Enviar' clickeado.")
                except TimeoutException as e:
                    print(f"Error al intentar hacer clic en el botón de 'Enviar'")
                    pass

                try:
                    print("Clickeando en el botón de 'Descartar'...")
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Descartar']"))).click()
                    print("Botón 'Descartar' clickeado.")
                except TimeoutException as e:
                    print(f"Error al intentar hacer clic en el botón de 'Descartar'")
                    pass
                except Exception as e:
                    print('Intentando presionar nuevamente Descartar')
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Descartar']"))).click()
                try:
                    print("Clickeando en el botón de 'Descartar 2'...")
                    wait_five_second.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']"))).click()
                    print("Botón 'Descartar 2' clickeado.")
                except TimeoutException as e:
                    print(f"Error al intentar hacer clic en el botón de 'Descartar 2'")
                    pass
            except Exception as e:
                print(f"Error al procesar la oferta {index + 1}: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")
    finally:
        # Cerrar el navegador
        input("Presiona enter para salir")
        driver.quit()

if __name__ == "__main__":
    main()
