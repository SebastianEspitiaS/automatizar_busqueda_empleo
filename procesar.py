import re
from datetime import datetime

client = ''

def descartar_oferta(oferta, descartar, incluir):
    """Determina si una oferta debe ser descartada o no."""
    titulo_lower = oferta.lower()
    descartar = descartar.split(",") if descartar else []
    incluir = incluir.split(",") if incluir else []
    descartar_regex = re.compile(r'\b(' + '|'.join(re.escape(p.lower().strip()) for p in descartar) + r')\b')
    incluir_regex = re.compile(r'\b(' + '|'.join(re.escape(p.lower().strip()) for p in incluir) + r')\b')

    if descartar_regex.search(titulo_lower):
        return True
    if incluir_regex.search(titulo_lower):
        return False
    return True

def procesar_respuesta(pregunta_texto, contexto_ia, checkboxes=False):
    """Genera una respuesta automatizada usando Hugging Face."""
    if not checkboxes:
        prompt = f"""
            {contexto_ia}
            De este contexto, usa lo que sea necesario para responder la siguiente pregunta
            Para responder sigue las siguientes instrucciones:
            1. Solo responde lo que se te pregunta, no mensiones nada adicional
            2. solo se pueden usar 500 letras, se lo mas conciso posible 
            3. Siempre habla en primera persona
            4. Nunca menciones mi nombre
            5. No menciones nada que no este en el contexto
            6. No menciones nada que no se te haya preguntado
            7. No menciones que eres un robot o IA
            
            Ejemplo de respuesta:
                Pregunta Ejemplo:
                    Cual es su nivel de ingles
                Respuesta Ejemplo:
                    Mi nivel de ingles A2
                Pregunta de ejemplo:
                    nivel de estudios
                Respuesta de ejemplo:
                    Mi nivel de estudios es tecnico en sistemas
                Pregunta de ejemplo:
                    Experiencia cual es su experiencia en el area
                Respuesta de ejemplo:
                    'Menciona los años de experiencia las empresas y solo un trabajo que sea relevante para el cargo'
                Pregunta de ejemplo:
                    Tiene dominio avanzado de Snowflake ?
                Respuesta de ejemplo:
                    No, no tengo experiencia con Snowflake
            
            Toma los ejemplos como referencia para responder la pregunta y no olvides seguir las instrucciones al pie de la letra.

            Genera una respuesta muy pero muy corta y concisa a la siguiente pregunta:
            {pregunta_texto}
        """
    else:
        prompt = f"""
            {contexto_ia}
            De este contexto, usa lo que sea necesario para responder la siguiente pregunta
            Solo Vas a responder con las opciones que te voy a dar, no puedes agregar nada adicional
            Unicamente puedes responder con las opciones que te voy a dar, no puedes agregar nada adicional
            No agregues nada adicional, solo responde con las opciones que te voy a dar
            Escribe las opciones tal cual como te las doy, no puedes cambiarlas
            No corrijas las opciones, solo responde con las opciones que te voy a dar
            Usa la opcion que mas se ajuste a tu respuesta, no puedes agregar nada adicional
            Responde eligiendo una de as opciones, no le agregues nada escribela tal cual como te las doy da igual si una opcion tiene errores ortograficos solo elige UNA solo 1 opcion (Las opciones estan separadas por ',') No des explicaciones de nada solo elige una opcion:
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
