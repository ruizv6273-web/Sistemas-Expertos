import json
import os
import math # Necesario para el cálculo de entropía

# Nombre del archivo para la base de conocimiento
DB_FILE = "campeones.json"

# MEJORA 1: Formato de preguntas para una mejor UX
# Mapea claves de atributos a preguntas más naturales.
FORMATO_PREGUNTAS = {
    "es_hombre": "¿Tu campeón es hombre?",
    "usa_magia": "¿Tu campeón usa magia?",
    "es_de_demacia": "¿Tu campeón es de Demacia?",
    "es_tanque": "¿Tu campeón es un tanque?",
    "usa_espada": "¿Tu campeón usa una espada?",
    "es_yordle": "¿Tu campeón es un Yordle?",
    "es_tirador": "¿Tu campeón es un tirador (ADC)?",
}

def formatear_pregunta(clave_pregunta):
    """Convierte una clave de atributo (ej: 'es_hombre') en una pregunta para el usuario."""
    pregunta = FORMATO_PREGUNTAS.get(clave_pregunta)
    if pregunta:
        return pregunta
    
    # Fallback para preguntas nuevas o no mapeadas
    pregunta_formateada = clave_pregunta.replace('_', ' ')
    # Asegura que comience con '¿' y termine con '?'
    if not pregunta_formateada.startswith("¿"):
        pregunta_formateada = f"¿Tu campeón {pregunta_formateada}?"
    if not pregunta_formateada.endswith("?"):
        pregunta_formateada += "?"
    return pregunta_formateada.capitalize()


def cargar_base_de_datos():
    """Carga la base de datos de campeones desde el archivo JSON."""
    if not os.path.exists(DB_FILE):
        print(f"Advertencia: No se encontró '{DB_FILE}'. Creando una base de conocimiento interna...")
        # MEJORA 2: Base de datos interna consistente
        # Se usa la data de tu JSON como fallback por defecto para que el script
        # sea funcional incluso sin el archivo.
        return {
            "campeones": [
                {"nombre": "Garen", "atributos": {"es_hombre": "si", "usa_magia": "no", "es_de_demacia": "si", "es_tanque": "si", "usa_espada": "si", "es_yordle": "no", "es_tirador": "no"}},
                {"nombre": "Lux", "atributos": {"es_hombre": "no", "usa_magia": "si", "es_de_demacia": "si", "es_tanque": "no", "usa_espada": "no", "es_yordle": "no", "es_tirador": "no"}},
                {"nombre": "Teemo", "atributos": {"es_hombre": "si", "usa_magia": "no", "es_de_demacia": "no", "es_tanque": "no", "usa_espada": "no", "es_yordle": "si", "es_tirador": "si"}},
                {"nombre": "Jinx", "atributos": {"es_hombre": "no", "usa_magia": "no", "es_de_demacia": "no", "es_tanque": "no", "usa_espada": "no", "es_yordle": "no", "es_tirador": "si"}},
                {"nombre": "Yasuo", "atributos": {"es_hombre": "si", "usa_magia": "si", "es_de_demacia": "no", "es_tanque": "no", "usa_espada": "si", "es_yordle": "no", "es_tirador": "no"}},
                {"nombre": "Ahri", "atributos": {"es_hombre": "no", "usa_magia": "si", "es_de_demacia": "no", "es_tanque": "no", "usa_espada": "no", "es_yordle": "no", "es_tirador": "no"}},
                {"nombre": "Darius", "atributos": {"es_hombre": "si", "usa_magia": "no", "es_de_demacia": "no", "es_tanque": "si", "usa_espada": "no", "es_yordle": "no", "es_tirador": "no"}}
            ]
        }
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al leer '{DB_FILE}': {e}. Usando base de datos de respaldo.")
        return cargar_base_de_datos() # Llama a sí misma con not os.path.exists=True

def guardar_base_de_datos(db):
    """Guarda la base de datos de campeones en el archivo JSON."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error al guardar la base de datos: {e}")

def obtener_respuesta_valida(pregunta):
    """Pide al usuario una respuesta 'si' o 'no' y la valida."""
    while True:
        respuesta = input(f"{pregunta} (si/no): ").lower().strip()
        if respuesta in ["si", "s", "yes", "y"]:
            return "si"
        if respuesta in ["no", "n"]:
            return "no"
        print("Respuesta no válida. Por favor, responde 'si' o 'no'.")

# --- MEJORA 3: Lógica de Decisión Basada en Entropía (Algoritmo ID3) ---

def calcular_entropia(grupo_campeones):
    """Calcula la entropía de un conjunto de campeones."""
    if not grupo_campeones:
        return 0
    
    total = len(grupo_campeones)
    conteo_nombres = {}
    for campeon in grupo_campeones:
        conteo_nombres[campeon['nombre']] = conteo_nombres.get(campeon['nombre'], 0) + 1
    
    entropia = 0.0
    for nombre, cantidad in conteo_nombres.items():
        probabilidad = cantidad / total
        if probabilidad > 0:
            entropia -= probabilidad * math.log2(probabilidad)
    return entropia

def encontrar_mejor_pregunta(posibles_campeones, preguntas_hechas):
    """
    Encuentra la mejor pregunta usando Ganancia de Información (basado en entropía).
    Esto es más eficiente que simplemente buscar un split 50/50.
    """
    if not posibles_campeones:
        return None

    mejor_ganancia_info = -1
    mejor_pregunta = None
    
    # Entropía actual (incertidumbre) del grupo
    entropia_actual = calcular_entropia(posibles_campeones)

    # Recopilar todas las preguntas únicas de los campeones restantes
    preguntas_posibles = set()
    for campeon in posibles_campeones:
        preguntas_posibles.update(campeon["atributos"].keys())

    preguntas_a_evaluar = list(preguntas_posibles - set(preguntas_hechas))

    if not preguntas_a_evaluar:
        return None

    for pregunta in preguntas_a_evaluar:
        grupo_si = []
        grupo_no = []
        
        for campeon in posibles_campeones:
            # Asumir 'no' si el atributo no está presente
            if campeon["atributos"].get(pregunta, "no") == "si":
                grupo_si.append(campeon)
            else:
                grupo_no.append(campeon)
        
        # Ignorar preguntas que no dividen (todos si o todos no)
        if not grupo_si or not grupo_no:
            continue

        # Calcular la entropía ponderada de los subgrupos
        total = len(posibles_campeones)
        entropia_ponderada = (len(grupo_si) / total) * calcular_entropia(grupo_si) + \
                             (len(grupo_no) / total) * calcular_entropia(grupo_no)
        
        # La ganancia de información es la reducción de la entropía
        ganancia_info = entropia_actual - entropia_ponderada

        if ganancia_info > mejor_ganancia_info:
            mejor_ganancia_info = ganancia_info
            mejor_pregunta = pregunta

    return mejor_pregunta

# --- MEJORA 4: Módulo de Aprendizaje Mejorado ---

def completar_atributos_nuevo_campeon(db, nuevo_campeon):
    """
    Después de agregar un nuevo campeón, pregunta al usuario sobre 
    otros atributos conocidos para hacer la base de datos más completa.
    """
    print(f"\nPara ayudarme a aprender más sobre {nuevo_campeon['nombre']},")
    print("contesta algunas preguntas más sobre él/ella.")
    
    # Obtener todos los atributos únicos de la base de datos
    todos_los_atributos = set()
    for campeon in db["campeones"]:
        todos_los_atributos.update(campeon["atributos"].keys())
        
    # Preguntar por los atributos que el nuevo campeón no tiene
    for atributo in sorted(list(todos_los_atributos)):
        if atributo not in nuevo_campeon["atributos"]:
            pregunta = formatear_pregunta(atributo)
            respuesta = obtener_respuesta_valida(pregunta)
            nuevo_campeon["atributos"][atributo] = respuesta
    
    print(f"¡Genial! He guardado toda la información sobre {nuevo_campeon['nombre']}.")

def modulo_aprendizaje(db, respuestas_usuario, campeon_incorrecto):
    """Inicia el proceso de aprendizaje cuando el sistema falla."""
    print("\n¡Vaya! Me he rendido. Ayúdame a aprender.")
    
    while True:
        nombre_correcto = input("¿En qué campeón estabas pensando? ").strip()
        if nombre_correcto:
            nombre_correcto = nombre_correcto.capitalize()
            break
        print("Por favor, introduce un nombre.")

    # Verificar si el campeón ya existe
    campeon_existente = next((c for c in db["campeones"] if c["nombre"].lower() == nombre_correcto.lower()), None)

    if campeon_existente and campeon_existente["nombre"] == campeon_incorrecto:
        print("¡Oh! Parece que hubo una contradicción en tus respuestas.")
        print(f"Basado en lo que sé, {campeon_incorrecto} debería haber sido la respuesta.")
        return

    # Obtener una pregunta diferenciadora
    pregunta_nueva = ""
    if campeon_incorrecto:
        prompt_pregunta = f"Dame una pregunta que se responda con 'sí' para {nombre_correcto}, pero con 'no' para {campeon_incorrecto}: "
    else:
        prompt_pregunta = f"Dame una pregunta que se responda con 'sí' para {nombre_correcto}: "
        
    while not pregunta_nueva:
        pregunta_nueva = input(prompt_pregunta).strip()

    # Normalizar la clave de la pregunta
    clave_pregunta = pregunta_nueva.lower().replace("¿", "").replace("?", "").replace(" ", "_")
    # Eliminar puntuación final si la hay
    clave_pregunta = clave_pregunta.rstrip('.,:;') 

    # Si el campeón es nuevo, se añade a la base de datos
    if not campeon_existente:
        nuevo_campeon = {
            "nombre": nombre_correcto,
            "atributos": respuestas_usuario.copy() # Copia las respuestas de esta partida
        }
        nuevo_campeon["atributos"][clave_pregunta] = "si"
        db["campeones"].append(nuevo_campeon)
        print(f"He aprendido sobre {nombre_correcto}.")
        
        # MEJORA 4 (continuación): Llamar al módulo de completar atributos
        completar_atributos_nuevo_campeon(db, nuevo_campeon)
        
    else:
        # Si el campeón ya existe, solo se actualiza su atributo
        campeon_existente["atributos"][clave_pregunta] = "si"
        # También actualizamos los atributos de la partida actual por si eran diferentes
        campeon_existente["atributos"].update(respuestas_usuario)
        print(f"He actualizado mi conocimiento sobre {nombre_correcto}.")

    # Actualizar al campeón incorrecto (si lo hubo)
    if campeon_incorrecto:
        campeon_a_actualizar = next((c for c in db["campeones"] if c["nombre"] == campeon_incorrecto), None)
        if campeon_a_actualizar:
            campeon_a_actualizar["atributos"][clave_pregunta] = "no"

    guardar_base_de_datos(db)
    print("¡Gracias! Mi conocimiento ha sido actualizado. ✨")

def jugar():
    """Función principal que ejecuta el bucle del juego."""
    db = cargar_base_de_datos()
    if not db["campeones"]:
        print("Error: La base de conocimiento de campeones está vacía.")
        return
        
    posibles_campeones = list(db["campeones"])
    preguntas_hechas = []
    respuestas_usuario = {}

    print("\n--- ¡Adivina el Campeón de League of Legends! ---")
    print("Piensa en un campeón y yo intentaré adivinarlo. Responde con 'si' o 'no'.")
    
    while len(posibles_campeones) > 1:
        pregunta = encontrar_mejor_pregunta(posibles_campeones, preguntas_hechas)

        if pregunta is None:
            # No hay más preguntas para diferenciar a los campeones restantes
            break
            
        pregunta_formateada = formatear_pregunta(pregunta)
        respuesta = obtener_respuesta_valida(pregunta_formateada)

        respuestas_usuario[pregunta] = respuesta
        preguntas_hechas.append(pregunta)

        # Filtrar la lista de campeones
        posibles_campeones = [
            c for c in posibles_campeones if c["atributos"].get(pregunta, "no") == respuesta
        ]

    # Fase de adivinanza
    if len(posibles_campeones) == 1:
        campeon_adivinado = posibles_campeones[0]
        respuesta_final = obtener_respuesta_valida(f"Tu campeón es... ¿{campeon_adivinado['nombre']}?")
        if respuesta_final == "si":
            print(f"\n¡Genial! ¡He adivinado! Era {campeon_adivinado['nombre']}. 🎉")
        else:
            modulo_aprendizaje(db, respuestas_usuario, campeon_adivinado['nombre'])

    elif len(posibles_campeones) == 0:
        print("\n🤔 No conozco ningún campeón con esas características.")
        modulo_aprendizaje(db, respuestas_usuario, None)
    
    else: # Múltiples campeones restantes pero sin preguntas para diferenciarlos
        print("\nNo tengo suficientes preguntas para diferenciar a los campeones restantes.")
        if posibles_campeones:
            nombres = ", ".join([c['nombre'] for c in posibles_campeones])
            print(f"Los campeones que coinciden son: {nombres}")
            # Se usa el primero como referencia para aprender
            modulo_aprendizaje(db, respuestas_usuario, posibles_campeones[0]['nombre'])
        else:
            # Este caso no debería ocurrir si la lógica es correcta, pero por si acaso
            modulo_aprendizaje(db, respuestas_usuario, None)


if __name__ == "__main__":
    while True:
        jugar()
        if obtener_respuesta_valida("\n¿Quieres jugar otra vez?") == "no":
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            break