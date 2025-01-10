from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

def configurar_navegador():
    """Configura el navegador con las opciones necesarias."""
    # Configurar el nivel de logging de Selenium
    logging.getLogger("selenium").setLevel(logging.ERROR)
    options = Options()
    options.add_argument("--log-level=3")  # Mostrar solo errores: 0=ALL, 1=DEBUG, 2=INFO, 3=WARNING, 4=ERROR, 5=FATAL
    options.add_argument("--disable-logging")  # Desactivar logs adicionales
    options.add_argument("--disable-extensions")  # Desactivar extensiones para evitar mensajes extra
    options.add_argument("--disable-gpu")  # Reducir mensajes relacionados con GPU
    options.add_argument("--no-sandbox")  # Evitar mensajes sandbox innecesarios
    options.add_argument("--silent")  # Configuración adicional para reducir mensajes
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1050, 768) 
    return driver