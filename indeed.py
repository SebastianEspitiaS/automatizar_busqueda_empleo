from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException, WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import pyautogui
import math

import random
import time

import pygetwindow as gw
from PIL import Image
import pyscreeze
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

def move_browser_to_bottom_right(driver, window_width=1001, window_height=500):
    """
    Mueve la ventana del navegador a la esquina inferior derecha de la pantalla.

    :param driver: La instancia del navegador Selenium.
    :param window_width: Ancho de la ventana en píxeles.
    :param window_height: Alto de la ventana en píxeles.
    """
    
    driver.maximize_window()  # Maximizar la ventana
    
    # Obtener el tamaño de la pantalla
    screen_width = driver.execute_script("return window.screen.availWidth;")
    screen_height = driver.execute_script("return window.screen.availHeight;")
    
    # Calcular las coordenadas para la esquina inferior derecha
    x_position = screen_width - 100
    y_position = screen_height - 10
    # y_position = screen_height - window_height

    # Ajustar el tamaño de la ventana
    driver.set_window_size(window_width, window_height)
    
    # Mover la ventana a la posición calculada
    driver.set_window_position(x_position, y_position)

def move_mouse_smoothly(destination_x, destination_y, steps=3, max_deviation=200):
    """
    Mueve el ratón hacia la posición (destination_x, destination_y) con movimientos suaves y parabólicos.
    
    :param destination_x: Coordenada X del destino.
    :param destination_y: Coordenada Y del destino.
    :param steps: Número de pasos en el movimiento.
    :param max_deviation: Desviación máxima para generar una curva parabólica.
    """
    # Obtener la posición inicial del ratón
    start_x, start_y = pyautogui.position()

    # Generar un punto de control aleatorio para la curva (control point)
    control_x = (start_x + destination_x) / 2 + random.uniform(-max_deviation, max_deviation)
    control_y = (start_y + destination_y) / 2 - random.uniform(0, max_deviation)

    # Mover el ratón a través de los puntos intermedios en la curva
    intermediate_x_list = []
    intermediate_y_list = []
    for step in range(steps + 1):
        t = step / steps  # Fracción del progreso (de 0 a 1)
        
        # Fórmula de la curva cuadrática de Bézier: (1-t)^2 * start + 2 * (1-t) * t * control + t^2 * end
        intermediate_x = (1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * destination_x
        intermediate_y = (1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * destination_y
        
        intermediate_x_list.append(intermediate_x)
        intermediate_y_list.append(intermediate_y)
        # Mover el ratón a la posición intermedia sin interrupciones
    
    for intermediate_x, intermediate_y in zip(intermediate_x_list, intermediate_y_list):
        pyautogui.moveTo(intermediate_x, intermediate_y)  # Sin pausas entre los pasos
    
    # Finalmente, mover al destino exacto
    pyautogui.moveTo(destination_x, destination_y)

def move_directly_to_random_far_position(screen_width, screen_height, min_distance=200, max_distance=500, padding=50):
    """
    Mueve el ratón a una posición aleatoria en la pantalla que esté alejada de la posición actual.
    
    :param min_distance: Distancia mínima desde la posición actual.
    :param max_distance: Distancia máxima desde la posición actual.
    :param padding: Espacio para evitar mover el ratón demasiado cerca de los bordes.
    """
    # Tamaño de la pantalla
    # screen_width, screen_height = pyautogui.size()  # Asegurarse de definir estas variables dentro de la función
    
    # Posición actual del ratón
    current_x, current_y = pyautogui.position()

    # Generar una posición aleatoria que esté alejada de la posición actual
    while True:
        angle = random.uniform(0, 2 * math.pi)  # Ángulo aleatorio
        distance = random.uniform(min_distance, max_distance)  # Distancia aleatoria

        # Calcular nuevas coordenadas
        new_x = current_x + math.cos(angle) * distance
        new_y = current_y + math.sin(angle) * distance

        # Verificar que la nueva posición esté dentro de la pantalla con el padding
        if padding <= new_x <= screen_width - padding and padding <= new_y <= screen_height - padding:
            pyautogui.moveTo(new_x, new_y, duration=0.5)
            break  # Si está dentro, salimos del bucle

def captcha_cloudflare(driver, retries=3):
    captcha_image = "./Captcha.png"  # Cambia esto por la ruta a tu imagen de referencia
    captcha_resuelto = False
    for _ in range(retries):
        # Obtén el título de la ventana desde Selenium
        selenium_title = driver.title + " - Google Chrome"
        print(f"Título de la ventana en Selenium: {selenium_title}")

        # Encuentra todas las ventanas de Google Chrome
        chrome_windows = [w for w in gw.getWindowsWithTitle('Google Chrome')]

        # Busca la ventana que coincide con el título de Selenium
        for window in chrome_windows:
            print(f"Ventana detectada: {window.title}")
            if selenium_title in window.title:
                print("Ventana encontrada. Activando...")
                window.activate()
                break
        else:
            print("No se encontró la ventana correspondiente.")
        time.sleep(3)
        driver.maximize_window()
        print('Se expande la ventana')
        window_size = driver.get_window_size()
        screen_width = window_size['width']
        screen_height = window_size['height']
        time.sleep(2)
        # Ruta de la imagen que deseas encontrar
        location = ''
        try:
            # Buscar la imagen en la pantalla
            location = pyautogui.locateOnScreen(captcha_image, confidence=0.7)  # Ajusta "confidence" si es necesario
            if location:
                center = pyautogui.center(location)
    
                # Mueve el ratón con desvíos erráticos antes de hacer clic
                move_mouse_smoothly(center.x, center.y)

                # Realiza el clic
                pyautogui.click()
                print("Clic realizado en la imagen.")
                move_directly_to_random_far_position(screen_width, screen_height)
                time.sleep(10)
                driver.refresh()
                time.sleep(3)
                location = ''
                location = pyautogui.locateOnScreen(captcha_image, confidence=0.7)
                if location:
                    print("La imagen se encuentra nuevamente en la pantalla.")
            move_browser_to_bottom_right(driver)
            time.sleep(60*3)
            continue

        except Exception as e:
            if location == '':
                print("No se encontró la imagen en la pantalla.")
                captcha_resuelto = True
                break
            print(f"Error: {e}")
    return captcha_resuelto

def filtro_cargo_region(driver, intentos=3):
    cargo_encontrado = False
    for _ in range(intentos):
        try:
            buscar_cargo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'text-input-what')))
            # buscar_cargo.click()
            if not escribir_texto(buscar_cargo, 'Analista de datos', driver):
                print("No se pudo escribir en el cuadro de texto 'buscar_cargo'")
                # driver.quit()
                # exit()

            ubicacion_cargo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'text-input-where')))
            # ubicacion_cargo.click()
            ubicacion_cargo.send_keys(Keys.CONTROL + 'a' + Keys.BACKSPACE)
            if not escribir_texto(ubicacion_cargo, 'Antioquia', driver):
                print("No se pudo escribir en el cuadro de texto 'ubicacion_cargo'")
                # driver.quit()
                # exit()

            ubicacion_cargo.send_keys(Keys.ENTER)
            break
        except Exception as e:
            print(f"Error al buscar el cargo: {e}")
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

def optener_ofertas(driver, xpath_cerrar_pop_up, intentos=3):
    ofertas = None
    xpath_ofertas = "//div[@class='slider_container css-nqpl5t eu4oa1w0']"
    for _ in range(intentos):
        try:
            print("Buscando ofertas...")
            ofertas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_ofertas)))
            break
        except Exception:    
            driver.switch_to.default_content()
            time.sleep(2)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_pop_up))).click()
                ofertas = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, xpath_ofertas)))
                break
            except TimeoutException:
                if captcha_cloudflare(driver):
                    ofertas = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, xpath_ofertas)))
                    break
    return ofertas

def optener_titulo_oferta(driver, oferta, xpath_cerrar_pop_up, intentos=3):
    titulo_oferta = None
    xpath_titulo = ".//div[@class='css-rzhvbl e37uo190']"
    for _ in range(intentos):
        try:
            print("Accediendo a titulo de la oferta...")
            titulo_oferta = WebDriverWait(oferta, 3).until(EC.presence_of_element_located((By.XPATH, xpath_titulo))).text
            print("Accediendo a la oferta...")
            break
        except Exception:
            print("No se pudo acceder a la oferta")
            driver.switch_to.default_content()
            time.sleep(2)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_pop_up))).click()
                titulo_oferta = WebDriverWait(oferta, 3).until(EC.presence_of_element_located((By.XPATH, xpath_titulo))).text
                break
            except Exception:
                if captcha_cloudflare(driver):
                    print('****Captcha CloudFlare Resuelto****')
                    titulo_oferta = WebDriverWait(oferta, 10).until(EC.presence_of_element_located((By.XPATH, xpath_titulo))).text
                    break
    return titulo_oferta

def optener_descripcion_oferta(driver, xpath_cerrar_pop_up, intentos=3):
    descripcion_oferta = None
    xpath_descripcion = ".//div[contains(@class, 'jobsearch-JobComponent-description')]"
    for _ in range(intentos):
        try:
            print("Accediendo a la descripcion de la oferta...")
            descripcion_oferta = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_descripcion))).text
            break
        except Exception:
            print("No se pudo acceder a la descripcion de la oferta")
            driver.switch_to.default_content()
            time.sleep(2)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_pop_up))).click()
                descripcion_oferta = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath_descripcion))).text
                break
            except Exception:
                if captcha_cloudflare(driver):
                    driver.back()
                    time.sleep(2)
                    descripcion_oferta = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_descripcion))).text
                    break
    return descripcion_oferta

def proceso_indeed():
    # Ruta al archivo JSON que contiene las cookies
    cookies_file = 'cookies.txt'
    options = uc.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--silent")
    driver = uc.Chrome(options=options)
    move_browser_to_bottom_right(driver, window_width=1001, window_height=700)
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
    filtro_cargo_region(driver)
    time.sleep(2)
    wait_for_page_load(driver)
    
    xpath_cerrar_pop_up = "//button[@aria-label='cerrar' and @type='button']"
    for _ in range(4):
        ofertas = optener_ofertas(driver, xpath_cerrar_pop_up)
        for oferta in ofertas:
            titulo_oferta = optener_titulo_oferta(driver, oferta, xpath_cerrar_pop_up)
            try:
                oferta.click()
            except Exception:
                try:
                    print("No se pudo acceder al titulo de la oferta")
                    print("Intentando cerrar el pop-up inicial...")
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_cerrar_pop_up))).click()
                    oferta.click()
                except Exception:
                    continue
            print(titulo_oferta, "\n")
            
            descripcion_oferta = optener_descripcion_oferta(driver, xpath_cerrar_pop_up)
            # try:
            #     descripcion_oferta = descripcion_oferta.text
            # except Exception:
            #     print("No se pudo acceder a la descripcion de la oferta")
            #     continue
            print(descripcion_oferta, "\n\n")
            
            extraer_valor_oferta = r'\b\d{1,3}(?:\.\d{3}){2,}(?:,\d+)?\b'
            valor_oferta = re.findall(extraer_valor_oferta, descripcion_oferta)
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
            
            try:
                elementos_expandidos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-expanded]")))
                len(elementos_expandidos)
                if len(elementos_expandidos) > 1:
                    segundo_elemento = elementos_expandidos[1]
                    segundo_elemento.click()
                else:
                    primer_elemento = elementos_expandidos[0]
                    primer_elemento.click()
                print('***ELIGIO LA HOJA DE VIDA A ENVIAR***\n\n')
            except TimeoutException:
                pass

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
            print("Clic en el botón de paginación")
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