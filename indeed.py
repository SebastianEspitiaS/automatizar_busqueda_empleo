from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import json

import random
import time

import pygetwindow as gw
import ast
import subprocess
import psutil
import sys
import os
import re

# Cerrar ventana del usuario actualmente abierta para poder optener las cookies 
def check_and_close_chrome():
    # Verificar si hay algún proceso de Chrome ejecutándose
    chrome_processes = [proc for proc in psutil.process_iter(['name']) if 'chrome' in proc.info['name'].lower()]
    abierto = False
    if chrome_processes:
        print(f"Se encontraron {len(chrome_processes)} procesos de Chrome abiertos.")
        respuesta = input("¿Deseas cerrarlos? (s/n): ").strip().lower()
        
        if respuesta == 's':
            abierto = True
            for proc in chrome_processes:
                try:
                    proc.terminate()  # Intentar terminar el proceso
                    proc.wait(timeout=3)  # Esperar a que termine
                except psutil.NoSuchProcess:
                    pass  # El proceso ya no existe
                except psutil.AccessDenied:
                    print(f"No se pudo terminar el proceso con PID {proc.pid}.")
            print("Todos los procesos de Chrome han sido cerrados (si fue posible).")
        else:
            print("No se cerraron los procesos de Chrome.")
            sys.exit(1)
    else:
        print("No hay procesos de Chrome abiertos.")
    return abierto

# Optener las cookies necesarias 
def open_chrome_with_default_profile():
    # Obtén el nombre del usuario actual
    user_name = os.getlogin()
    
    # Configura las opciones de Chrome
    chrome_options = Options()
    
    # Establece la ruta del perfil de usuario automáticamente
    user_data_dir = fr"C:\Users\{user_name}\AppData\Local\Google\Chrome\User Data"
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")  # Perfil por defecto
    # Agrega el modo headless
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Opcional, pero recomendado en algunos casos
    # Inicializa el navegador con las opciones configuradas
    driver = webdriver.Chrome(options=chrome_options)

    # Abre una página de ejemplo
    driver.get("https://co.indeed.com/")
    
    cookies = driver.get_cookies()
    # Guardar cookies en un archivo
    with open('cookies.txt', 'w') as file:
        for cookie in cookies:
            file.write(f"{cookie}\n")
    # Mantén la ventana abierta por un tiempo
    driver.quit()  # Cierra el navegador

# Abrir nuevamente la ventana de chrome del usuario
def abrir_chrome(abierto):
    if abierto:
        # Ruta al ejecutable de Google Chrome (modifica según tu instalación)
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        
        # Abre Google Chrome
        subprocess.Popen([chrome_path])
        
        # Espera un momento para asegurar que la ventana de Chrome esté abierta
        time.sleep(2)
        
        # Obtén la ventana de Chrome (la primera que encuentra)
        ventana_chrome = gw.getWindowsWithTitle("Google Chrome")[0]
        ventana_chrome.maximize()
        # Minimiza la ventana
        ventana_chrome.minimize()

def wait_for_page_load(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def escribir_texto(elemento, texto, driver):
    for _ in range(5):  # Intentar hasta 5 veces
        elemento.clear()
        elemento.send_keys(texto)
        time.sleep(1)  # Esperar un momento para que el texto se escriba
        if texto in elemento.get_attribute('value'):
            return True
    return False

def move_mouse_randomly(driver, element):
    action = ActionChains(driver)
    element_location = element.location
    element_size = element.size

    # Obtener las coordenadas del centro del elemento
    target_x = element_location['x'] + element_size['width'] / 2
    target_y = element_location['y'] + element_size['height'] / 2

    # Dividir el movimiento en varios pasos pequeños
    steps = 20
    current_x, current_y = target_x - 200, target_y - 200  # Comienza fuera del objetivo
    for i in range(steps):
        # Calcular la posición intermedia
        intermediate_x = current_x + random.uniform(-5, 5) + (target_x - current_x) * (i + 1) / steps
        intermediate_y = current_y + random.uniform(-5, 5) + (target_y - current_y) * (i + 1) / steps

        # Mover el mouse a la posición intermedia
        action.move_by_offset(intermediate_x - current_x, intermediate_y - current_y).perform()

        # Actualizar la posición actual del mouse
        current_x, current_y = intermediate_x, intermediate_y

        # Agregar una pausa aleatoria entre los movimientos
        time.sleep(random.uniform(0.05, 0.2))

    # Mover exactamente al centro del elemento
    action.move_by_offset(target_x - current_x, target_y - current_y).perform()

def volver_inicio(driver):
        driver.close()
        if driver.window_handles:
            try:
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
            except InvalidSessionIdException:
                print("La sesión del navegador no es válida. Cerrando el navegador.")
                driver.quit()
                sys.exit(1)
        else:
            print("No hay ventanas abiertas. Cerrando el navegador.")
            driver.quit()
            sys.exit(1)

def captcha_cloudflare(driver, retries=3):
    for _ in range(retries):
        try:
            # Cambiar de vuelta al contenido principal
            driver.switch_to.default_content()
            print('Buscando CAPTCHA...')
            # Esperar a que el iframe del CAPTCHA esté presente
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@title='Widget containing a Cloudflare security challenge']")))
            driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='Widget containing a Cloudflare security challenge']"))
            print("CAPTCHA iframe found.")
            
            # Esperar a que el checkbox del CAPTCHA sea clicable
            captcha_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
            print("CAPTCHA checkbox found.")

            # Asegurarse de que el checkbox del CAPTCHA esté visible
            driver.execute_script("arguments[0].scrollIntoView(true);", captcha_checkbox)
            print("CAPTCHA checkbox visible.")

            # Mover el mouse de manera errática al checkbox del CAPTCHA y hacer clic
            move_mouse_randomly(driver, captcha_checkbox)
            print("CAPTCHA checkbox clicked randomly.")

            captcha_checkbox.click()
            print("CAPTCHA checkbox clicked.")
        except TimeoutException:
            print("Timeout al esperar el checkbox del CAPTCHA Cloudflare.")
            continue
        except NoSuchElementException:
            print("No se encontró el iframe del CAPTCHA.")
            continue
        except WebDriverException as e:
            print(f"Error al hacer clic en el checkbox del CAPTCHA: {e}")
            continue
        finally:
            time.sleep(15)
            break

def face_busqueda(driver):
    try:
        buscar_cargo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'text-input-what')))
        buscar_cargo.click()
        if not escribir_texto(buscar_cargo, 'Analista de datos', driver):
            print("No se pudo escribir 'Analista de datos' en el cuadro de texto 'buscar_cargo'")
            driver.quit()
            exit()

        ubicacion_cargo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'text-input-where')))
        ubicacion_cargo.click()
        ubicacion_cargo.send_keys(Keys.CONTROL + 'a' + Keys.BACKSPACE)
        if not escribir_texto(ubicacion_cargo, 'Antioquia', driver):
            print("No se pudo escribir 'Antioquia' en el cuadro de texto 'ubicacion_cargo'")
            driver.quit()
            exit()

        ubicacion_cargo.send_keys(Keys.ENTER)
    except Exception as e:
        captcha_cloudflare(driver)

def agregar_cookies(driver, cookies):
    try:
        for cookie in cookies:
            cookie_dict = ast.literal_eval(cookie.strip())  # Convierte el string a un diccionario de cookies
            driver.add_cookie(cookie_dict)
        os.remove('cookies.txt')
    except Exception as e:
        print(f"Error al añadir cookies o eliminar el archivo: {e}")
        driver.quit()
        return
    try:
        driver.refresh()
    except WebDriverException as e:
        print(f"Error al refrescar la página: {e}")
        
def proceso_indeed():
    # Ruta al archivo JSON que contiene las cookies
    cookies_file = 'cookies.txt'
    options = uc.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--silent")
    driver = uc.Chrome(options=options)
    # driver.maximize_window()
    driver.set_window_size(1001, 500)
    try:
        driver.get('https://co.indeed.com')
    except WebDriverException as e:
        print(f"Error al cargar la página inicial: {e}")
        driver.quit()
        return

    # Lee las cookies desde el archivo
    try:
        with open(cookies_file, 'r') as file:
            cookies = file.readlines()
    except FileNotFoundError:
        print(f"El archivo de cookies '{cookies_file}' no existe.")
        driver.quit()
        return
    except Exception as e:
        print(f"Error al leer las cookies: {e}")
        driver.quit()
        return

    # Añade las cookies al navegador
    agregar_cookies(driver, cookies)
    
    face_busqueda(driver)
    time.sleep(2)

    wait_for_page_load(driver)
    for _ in range(4):
        try:
            ofertas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='slider_container css-nqpl5t eu4oa1w0']")))
        except Exception:    
            try:
                driver.switch_to.default_content()
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-yi9ndv e8ju0x51']"))).click()
                ofertas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='slider_container css-nqpl5t eu4oa1w0']")))
            except TimeoutException:
                captcha_cloudflare(driver)
        for oferta in ofertas:
            try:
                titulo_oferta = WebDriverWait(oferta, 3).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='css-rzhvbl e37uo190']")))
                oferta.click()
            except Exception:
                try:
                    print("No se pudo acceder a la oferta")
                    input("Presiona Enter para continuar")
                    driver.switch_to.default_content()
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-yi9ndv e8ju0x51']"))).click()
                    time.sleep(2)
                    titulo_oferta = WebDriverWait(oferta, 3).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='css-rzhvbl e37uo190']")))
                    oferta.click()
                except TimeoutException:
                    captcha_cloudflare(driver)
                    print("No hay captcha en la oferta")

            titulo_oferta_texto = titulo_oferta.text
            print(titulo_oferta_texto, "\n")
            
            try:
                descripcion_oferta = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='jobsearch-JobComponent-description css-10ybyod eu4oa1w0']")))
            except TimeoutException:
                continue
            descripcion_oferta_texto = descripcion_oferta.text
            print(descripcion_oferta_texto, "\n\n")
            
            extraer_valor_oferta = r'\b\d{1,3}(?:\.\d{3}){2,}(?:,\d+)?\b'
            valor_oferta = re.findall(extraer_valor_oferta, descripcion_oferta_texto)
            print(valor_oferta, "\n\n")
            if not valor_oferta:
                continue
            else:
                valor_oferta = valor_oferta[-1].replace('.', '')  # Eliminar los puntos
                valor_oferta = float(valor_oferta)
                if valor_oferta < 2000000:
                    continue

            try:
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='indeedApplyButton']"))).click()
            except TimeoutException:
                continue
            driver.switch_to.window(driver.window_handles[-1])
            wait_for_page_load(driver=driver)
            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ia-container']/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div"))).click()
            except TimeoutException:
                pass
            print('***ENTRO A LA PARA REGISTRARSE A LA OFERTA***\n\n')

            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Este empleo está ubicado en Colombia']")))
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='yes']"))).click()
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ia-container']/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/button"))).click()
            except TimeoutException:
                pass

            elementos_expandidos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-expanded]")))
            len(elementos_expandidos)
            if len(elementos_expandidos) > 1:
                segundo_elemento = elementos_expandidos[1]
                segundo_elemento.click()
            else:
                primer_elemento = elementos_expandidos[0]
                primer_elemento.click()
            print('***ELIGIO LA HOJA DE VIDA A ENVIAR***\n\n')

            try:
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='ia-container']/div/div[1]/div/div/div[2]/div[2]/div/div/main/div[3]/div"))
                ).click()
                print("Se completo esta página\n\n")
            except TimeoutException:
                print("Timeout al esperar el primer botón clicable.")
            except WebDriverException as e:
                print(f"Error al hacer clic en el primer botón: {e}")

            try:
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='extra-scope']/div/div/div/div/div[2]/button"))
                ).click()
                print("Siguiente página\n\n")
            except TimeoutException:
                print("Timeout al esperar el segundo botón clicable.")
            except WebDriverException as e:
                print(f"Error al hacer clic en el segundo botón: {e}")

            try:
                print("Cargo La Pagina\n\n")
                wait_for_page_load(driver=driver)
            except TimeoutException:
                print("Timeout al esperar que la página cargue completamente.")

            preguntas = []
            try:
                preguntas = WebDriverWait(driver, 3).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//span[@class='css-ft2u8r e1wnkr790']"))
                )
                if len(preguntas) > 1:
                    print('Todavia no esta implementado responder preguntas.')
                    volver_inicio(driver)
                    continue
            except TimeoutException:
                pass

            try:
                if preguntas:
                    print("No se encontraron preguntas\n\n")
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='ia-container']/div/div/div/div/div[2]/div[2]/div/div/main/div[3]/div/button"))
                    ).click()
                    print("Se completo esta página\n\n")
            except TimeoutException:
                print("Timeout al esperar el tercer botón clicable.")
            except WebDriverException as e:
                print(f"Error al hacer clic en el tercer botón: {e}")

            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//iframe[@title='reCAPTCHA']"))
                )
                # Cambiar al iframe del CAPTCHA
                driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']"))
                
                captcha_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='recaptcha-checkbox-border']"))
                )
                # Mover el mouse de manera errática al checkbox del CAPTCHA y hacer clic
                move_mouse_randomly(driver, captcha_checkbox)
                captcha_checkbox.click()
                print("CAPTCHA checkbox clicked.")
            except TimeoutException:
                print("Timeout al esperar el checkbox del CAPTCHA.")
            except WebDriverException as e:
                print(f"Error al hacer clic en el checkbox del CAPTCHA: {e} \n\n")
            finally:
                # Cambiar de vuelta al contenido principal
                driver.switch_to.default_content()
                time.sleep(3)

            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'css-14m9ps3 e8ju0x50')]"))).click()
                time.sleep(3)
                print("Se completo esta página\n\n")
            except TimeoutException:
                print("Timeout al esperar el cuarto botón clicable.")
            except WebDriverException as e:
                print(f"Error al hacer clic en el cuarto botón: {e}")
            volver_inicio(driver)

        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='pagination-page-next']"))
            ).click()
        except TimeoutException:
            print("Timeout al esperar el botón de paginación.")
        except WebDriverException as e:
            print(f"Error al hacer clic en el botón de paginación: {e}")
        time.sleep(3)

    try:
        print(driver.title)
    except WebDriverException as e:
        print(f"Error al obtener el título de la página: {e}")

    try:
        input("Presiona Enter para cerrar el navegador: ")
        driver.quit()
    except WebDriverException as e:
        print(f"Error al cerrar el navegador: {e}")

if __name__ == "__main__":
    chrome_abierto = check_and_close_chrome()
    open_chrome_with_default_profile()
    # abrir_chrome(chrome_abierto)
    proceso_indeed()