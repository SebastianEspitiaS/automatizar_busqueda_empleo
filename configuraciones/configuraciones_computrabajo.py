from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def login(driver):
    """Realiza el login en la página."""
    driver.get("https://co.computrabajo.com/")
    
    print("Ingresando credenciales de Computrabajo...")
    while True:
        correo = input("Ingresa tu correo: ")
        contraseña = input("Ingresa tu contraseña: ")
        print("Son correctos los datos? (s/n)\n")
        print(f"Correo: {correo}")
        print(f"Contraseña: {contraseña}")
        respuesta = input()
        if respuesta.lower() == 's' or respuesta.lower() == 'si' or respuesta.lower() == '':
            break
        elif respuesta.lower() == 'n' or respuesta.lower() == 'no':
            continue
        else:
            print("Respuesta no valida, intente de nuevo.")
            continue
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='publish_offers_link']/span"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@alt='Ingresar' and contains(@class, 'js_login')]"))).click()
    
    # Ingreso de credenciales
    entrada_correo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='LoginModel_Email' and @type='email']")))
    entrada_correo.send_keys(correo)
    entrada_correo.send_keys(Keys.ENTER)
    
    entrada_contraseña = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='LoginModel_Password' and @type='password']")))
    entrada_contraseña.click()
    entrada_contraseña.send_keys(contraseña)
    entrada_contraseña.send_keys(Keys.ENTER)
    driver.minimize_window()
    time.sleep(2)

def buscar_ofertas(driver):
    """Realiza la búsqueda de ofertas de trabajo en el portal."""
    empleo_a_buscar = input("Ingresa el empleo que deseas buscar: ")
    entrada_cargo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='prof-cat-search-input' and @type='search']")))
    entrada_cargo.send_keys(empleo_a_buscar)
    entrada_cargo.send_keys(Keys.ENTER)
