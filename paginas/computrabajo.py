import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from huggingface_hub import InferenceClient
from procesar import descartar_oferta, procesar_respuesta
import procesar
import re

def realizar_proceso_computrabajo(driver):
    """Proceso de navegación y aplicación a ofertas en Computrabajo."""
    try:
        palabras_a_descartar = input("Palabras a descartar (separadas por ','): ")
        palabras_a_incluir = input("Palabras a incluir (separadas por ','): ")
        api_key = input("\nIngresa la API key de Hugging Face: ")
        procesar.client = InferenceClient(api_key=api_key)

        print("\nEscribe el contexto para la respuesta (Presiona dos veces ENTER para finalizar):")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        contexto_ia = "\n".join(lines)

        driver.set_window_size(1050, 768)  # Ancho: 1024px, Alto: 768px
        # Intentar cerrar el pop-up inicial
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pop-up-webpush-sub']/div[2]/div/button[1]"))).click()
        except Exception as e:
            print(f"Error al cerrar el pop-up inicial: {e}")
        driver.minimize_window()
            
        for _ in range(5):
            try:
                articles = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//article[contains(@class, 'box_offer')]"))
                )
            except Exception as e:
                print(f"Error al cargar las ofertas: {e}")
                break

            regex = r"\d{1,3}(\.\d{3})*,\d{2}"
            
            for article in articles:
                try:
                    article_text = article.text
                    match = re.search(regex, article_text)
                    valor_oferta = float(match.group(0).replace('.', '').replace(',', '.')) if match else None
                    if descartar_oferta(article_text, palabras_a_descartar, palabras_a_incluir) or (not valor_oferta or valor_oferta < 2000000):
                        continue

                    print(f"Procesando oferta: {article_text}\n")
                    article.click()
                    time.sleep(1)
                    try:
                        # Intentar con la primera ruta XPath
                        apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[@class='b_primary big' and @data-apply-ac]"))
                        )
                    except TimeoutException:
                        try:
                            # Si no se encuentra, intentar con la segunda ruta XPath
                            apply_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'b_primary big') and text()='Aplicar']"))
                            )
                        except TimeoutException:
                            print("No se encontró el botón para aplicar a la oferta.")
                            continue

                    # Hacer clic en el botón de aplicar
                    try:
                        apply_button.click()
                    except WebDriverException as e:
                        print(f"Error al hacer clic en el botón de aplicar: {e}")
                        continue

                    # Verificar si ya se postuló a la oferta
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//p[@class='fs24' and text()='Ya te postulaste a esta oferta']"))
                        )
                        print("Ya te postulaste a esta oferta.\n")
                        continue
                    except TimeoutException:
                        print("Oferta no postulada.\n")

                    # Responder preguntas abiertas
                    try:
                        preguntas_entrevista = WebDriverWait(driver, 5).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//label[@class='mb10 dB']"))
                        )
                        cuadro_respuestas = WebDriverWait(driver, 2).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//textarea[@class='w100 rounded']"))
                        )

                        for pregunta, respuesta in zip(preguntas_entrevista, cuadro_respuestas):
                            print(f"Pregunta: {pregunta.text}")
                            respuesta_ia = procesar_respuesta(pregunta.text, contexto_ia)
                            respuesta.send_keys(respuesta_ia)
                            time.sleep(1)
                            print(f"Respuesta: {respuesta_ia}")
                    except TimeoutException:
                        print("No se encontraron preguntas de entrevista.")
                    except WebDriverException as e:
                        print(f"Error al responder preguntas abiertas: {e}")

                    # Seleccionar opciones de checkbox
                    try:
                        contenedor_checkbox = driver.find_elements(By.XPATH, "//div[@class='field_radio_box rounded']")
                        if not contenedor_checkbox:
                            print("No se encontraron contenedores de checkbox en la página.")
                        else:
                            for contenedor in contenedor_checkbox:
                                try:
                                    # Encontrar la pregunta del checkbox dentro del contenedor
                                    pregunta_checkbox = contenedor.find_element(By.XPATH, ".//label[@class='fs16 fw_n']")
                                    checkboxes = contenedor.find_elements(By.XPATH, ".//span[@class='label_box']")
                                    
                                    checkbox_texts = ", ".join([checkbox.text for checkbox in checkboxes])
                                    print(pregunta_checkbox.text, '\n\n')
                                except NoSuchElementException as e:
                                    print(f"Error al encontrar elementos de checkbox: {e}")
                                print(pregunta_checkbox.text, '\n\n')
                                print(checkbox_texts, '\n\n')
                                pregunta_y_opciones = f"Pregunta:{pregunta_checkbox.text}\n\nOpciones (Elije una de estas opciones y no digas nada mas, no expliques nada solo elige una opcion):\n{checkbox_texts}"
                                respuesta_ia = procesar_respuesta(pregunta_y_opciones, contexto_ia, checkboxes=True)
                                print(f"Respuesta: {respuesta_ia}")
                                respuesta_ia = respuesta_ia.lower().replace(',', '').replace('.', '').split(' ')
                                respuesta = []
                                for checkbox in checkboxes:
                                    checkbox_text = (checkbox.text).lower().replace(',', '').replace('.', '')
                                    respuesta = [checkbox_text for respuesta in respuesta_ia if respuesta == checkbox_text]
                                    if respuesta:
                                        print("Se selecciono la opcion: \n\n")
                                        print(checkbox.text, '\n\n')
                                        checkbox.click()
                                        break
                                if not respuesta:
                                    break
                    except WebDriverException as e:
                        print(f"Error al manejar los checkboxes: {e}")
                        continue

                    # Intentar enviar la postulación
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[@class='b_primary big ml10']"))
                        ).click()
                        time.sleep(2)
                    except Exception as e:
                        print(f"Error al enviar la postulación: {e}")
                except Exception as e:
                    print(f"Error general al procesar la oferta: {e}")

            # Ir a la siguiente página
            try:
                input("Presiona enter para cambiar de página...")
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='b_primary w48 buildLink cp']"))
                ).click()
                print("Cambiando a la siguiente página...\n")
                time.sleep(2)
            except Exception as e:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//p[@class='fs24 mb5']"))
                    )
                    print("Ya no se encontraron mas ofertas.")
                    return
                except TimeoutException as e:
                    print(f"Error al cambiar de página: {e}")
                    break
    except Exception as e:
        print(f"Error crítico en el proceso: {e}")
