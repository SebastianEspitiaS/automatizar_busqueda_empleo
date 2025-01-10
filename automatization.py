from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import locale
from datetime import datetime
import re
from huggingface_hub import InferenceClient

# Configuración inicial
locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
client = InferenceClient(api_key="")

descartar_palabras = [
    # Niveles de entrada o estudiantes
    "practicante", "practicantes", "bilingüe", "bilingües", "bilingue", "bilingues", 
    "ingles", "idioma", "idiomas", "traduccion", "traducciones", "traductor", 
    "traductores", "comunicacion", "comunicaciones", "internacional", "internacionales", 
    "expatriado", "expatriados", "asistente", "asistentes", "interno", "internos", 
    "becario", "becarios", "trainee", "trainees", "estudiante", "estudiantes", 
    "novato", "novatos", "aprendiz", "aprendices", "nuevo", "nuevos", "inicial", 
    "iniciales", "formacion", "formaciones", "entry", "nivel", "niveles", 
    "capacitación", "capacitaciones", "capacitacion", "capacitaciones", 
    "mentor", "mentores", "mentee", "mentees", "experiencia", "experiencias", 
    "basico", "basicos", "principiante", "principiantes", "practica", 
    "practicas", "auxiliar", "auxiliares"
]

incluir_palabras = [
    # Roles relacionados con analista de datos
    "datos", "data", "analisis", "análisis", "business", 
    "intelligence", "BI", "reportes", "visualización", "visualizacion", 
    "dashboard", "analytics", "analytics engineer", 
    "cientifico", "científica", "cientifico de datos", "científica de datos", 
    "scientist", "data scientist", "analytics specialist",

    # Roles relacionados con ingeniería de datos
    "ingeniero de datos", "ingeniera de datos", 
    "data engineer", "data pipeline", "ETL", "ingestión", "ingestion", 
    "transformación", "transformacion", "pipeline", "almacén de datos", 
    "almacen de datos", "data warehouse", "big data", "spark", 
    "hadoop", "cloud", "azure", "aws", "gcp", "bases de datos", 
    "SQL", "NoSQL", "mongodb", "postgresql", "mysql", "cassandra", 
    "oracle", "redshift", "data architecture", "arquitectura de datos",

    # Ciencia de datos y estadística
    "estadística", "estadistica", "modelos", "predicción", "prediccion", 
    "machine learning", "aprendizaje automático", "aprendizaje profundo", 
    "deep learning", "redes neuronales", "forecasting", "modelado", 
    "modelación", "optimización", "optimizacion", "regresión", 
    "clasificación", "análisis descriptivo", "descriptivo", "predictivo", 
    "prescriptivo", "clustering", "agrupamiento",

    # Inteligencia Artificial
    "inteligencia artificial", "AI", "IA", "artificial intelligence", 
    "NLP", "procesamiento de lenguaje natural", "chatbots", "recomendación", 
    "sistemas de recomendación", "computer vision", "visión por computadora", 
    "modelo generativo", "transformer", "LLM", "modelos de lenguaje", 
    "gan", "redes generativas", "visión artificial", "modelos preentrenados",

    # Roles en tecnología relacionados
    "ingeniero", "ingeniera", "desarrollador", 
    "developer", "programador", "developer advocate", "cloud engineer", 
    "software engineer", "data architect", "arquitecto de datos", 
    "arquitectura", "automatización", "automatizacion", "automatización de datos", 
    "devops", "ML engineer", "ingeniero de ML", "machine learning engineer", "machine learning"

    # Herramientas y tecnologías clave
    "python", "sql", "excel", "power bi", "tableau", "looker", 
    "data studio", "bigquery", "spark", "hive", "kafka", "pandas", 
    "numpy", "tensorflow", "keras", "scikit-learn", "pycaret", 
    "dbt", "airflow", "etl", "bash", "linux", "shell scripting", 
    "versionamiento", "git", "github", "gitlab",

    # Palabras específicas relacionadas con funciones clave
    "estrategia", "indicadores", "insights", "informes", 
    "automatizar", "automatización", "pipeline", 
    "infraestructuras", "almacenamiento", "cluster", "orquestación", 
    "cálculo", "calculo", "simulación", "simulacion", "proyección", 
    "proyeccion", "predicción", "optimización", "dashboards", "kpi", "metricas", 
    "indicadores clave", "reporting"
]

# Funciones reutilizables
def configurar_navegador():
    """Configura el navegador con las opciones necesarias."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1100, 720)
    driver.minimize_window()
    return driver

def login(driver):
    """Realiza el login en la página."""
    driver.get("https://co.computrabajo.com/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='publish_offers_link']/span"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@alt='Ingresar' and contains(@class, 'js_login')]"))).click()
    
    # Ingreso de credenciales
    entrada_correo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='LoginModel_Email' and @type='email']")))
    entrada_correo.send_keys("espitiasanchezsebastian64@gmail.com")
    entrada_correo.send_keys(Keys.ENTER)
    
    time.sleep(2)
    entrada_contraseña = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='LoginModel_Password' and @type='password']")))
    entrada_contraseña.send_keys("Boneflecher01")
    entrada_contraseña.send_keys(Keys.ENTER)
    
    time.sleep(2)

def buscar_ofertas(driver):
    """Realiza la búsqueda de ofertas de trabajo en el portal."""
    entrada_cargo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='prof-cat-search-input' and @type='search']")))
    entrada_cargo.send_keys("Analista de datos en Antioquia")
    entrada_cargo.send_keys(Keys.ENTER)

def descartar_oferta(oferta, descartar, incluir):
    """Determina si una oferta debe ser descartada o no."""
    titulo_lower = oferta.lower()
    descartar_regex = re.compile(r'\b(' + '|'.join(re.escape(p.lower()) for p in descartar) + r')\b')
    incluir_regex = re.compile(r'\b(' + '|'.join(re.escape(p.lower()) for p in incluir) + r')\b')

    if descartar_regex.search(titulo_lower):
        return True
    if incluir_regex.search(titulo_lower):
        return False
    return True

def procesar_respuesta(pregunta_texto):
    """Genera una respuesta automatizada usando Hugging Face."""
    prompt = f"""
        Soy analista de datos con más de 2 años de experiencia en herramientas como Python, SQL, Excel, Power BI y tecnologías de Azure (Azure Synapse Analytics, Data Lake, SQL Server, Databricks, Spark y PySpark). He trabajado en proyectos de inteligencia artificial utilizando Azure OpenAI (AzureGPT) y Gemini AI, aplicando análisis de datos en sectores como finanzas, subsidios y otros entornos empresariales.

        En mis roles anteriores:

        En Comfama, optimicé procesos con Azure, Python y SQL Server, mejorando la eficiencia operativa.
        En Strast SAS, automatizé reportes y análisis utilizando Python, Excel y SQL, impulsando la toma de decisiones.
        Tengo experiencia creando visualizaciones interactivas en Power BI y Looker Studio, así como automatizando procesos y extracciones de datos mediante APIs con Python. He trabajado en equipos bajo metodologías ágiles como Scrum, aportando soluciones efectivas y colaborativas.

        Busco oportunidades donde pueda aplicar mis conocimientos técnicos y habilidades blandas para resolver problemas y aportar valor estratégico. Estoy interesado en unirme a un equipo innovador y colaborativo, donde pueda seguir creciendo profesionalmente y aportar mi experiencia en análisis de datos y proyectos de inteligencia artificial.
        
        En Comfama trabaje desde Octubre de 2022 hasta Abril de 2024 (1 año y 6 meses)
        En Strast SAS trabaje desde Junio de 2024 hasta {(datetime.today().date()).strftime('%B de %Y').capitalize()} (mas de 6 meses)
        
        Excel: avanzado
        Power BI: intermedio
        Looker Studio: intermedio
        SQL: avanzado
        Python: avanzado
        Herramientas De Azure: intermedio
        Spark y PySpark: intermedio
                            
        Mi direccion de recidencia es Medellin - Prado Centro
        Mi telefono es: 3155363185
        Mi correo es: espitiasanchezsebastian64@gmail.com
        Mi nivel de ingles es: A2
        Nivel de estudio o ultimo estudio es: tecnico como desarrollador de software (con enfacis en analisis de datos)
        Horarios para una entrevista puede ser a cualquier hora de 8am a 4pm
                            
        De esta informacion, usa lo que sea necesario para responder la siguiente pregunta (Da una respuesta resumida y directa, no expliques mucho y siempre habla en primera persona, nunca menciones mi nombre y siempre responde en español), la pregunta es:      
        {pregunta_texto}
    """
    prompt = prompt.replace('\n', ' ').replace('  ', ' ')
    messages = [{"role": "user", "content": prompt}]
    
    stream = client.chat.completions.create(
        model="codeLlama/CodeLlama-34b-Instruct-hf", 
        messages=messages, 
        temperature=0.5,
        max_tokens=2048,
        top_p=0.7,
        stream=True
    )
    
    respuesta_ia = ''
    for chunk in stream:
        respuesta_ia += chunk.choices[0].delta.content
    return respuesta_ia.strip()

# Flujo principal
try:
    driver = configurar_navegador()
    login(driver)
    buscar_ofertas(driver)
    
    for _ in range(5):
        articles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//article[contains(@class, 'box_offer')]")))
        regex = r"\d{1,3}(\.\d{3})*,\d{2}"
        
        for article in articles:
            article_text = article.text
            match = re.search(regex, article_text)
            valor_oferta = float((match.group(0)).replace('.', '').replace(',', '.')) if match else None
            
            if descartar_oferta(article_text, descartar_palabras, incluir_palabras) or (not valor_oferta or valor_oferta < 2000000):
                continue
            
            print(article_text, '\n\n')
            article.click()
            time.sleep(1)
            
            # Asegurarse de que el botón de aplicar sea visible
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='b_primary big' and @data-apply-ac]"))).click()
            
            try:
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//p[@class='fs24' and text()='Ya te postulaste a esta oferta']")))
                continue
            except Exception:
                pass
            
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//span[@class = 'label_box']"))
                )
                print("Hay un CheckBox. \n\n")
                continue
            except Exception:
                pass
            
            # Completar las preguntas de entrevista
            preguntas_entrevista = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//label[contains(@class, 'mb10') and contains(@class, 'dB')]")))
            cuadro_respuestas = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//textarea[contains(@class, 'w100') and contains(@class, 'rounded')]")))
            
            for pregunta, respuesta in zip(preguntas_entrevista, cuadro_respuestas):
                print(pregunta.text, '\n\n')
                respuesta_ia = procesar_respuesta(pregunta.text)
                respuesta.send_keys(respuesta_ia)
                time.sleep(1)
                print(respuesta_ia, '\n\n')
            
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'b_primary') and contains(@class, 'big') and contains(@class, 'ml10')]"))).click()
            time.sleep(2)
        
        # Ir a la siguiente página de resultados
        print("Se completo esta página\n\n")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='offersGridOfferContainer']/div[6]/span[2]"))).click()
        print("Siguiente página\n\n")

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    driver.quit()
