import json
import os

# Archivo para guardar la base de conocimiento
ARCHIVO_KB = "knowledge.json"

# Función para cargar la base de conocimiento
def cargar_kb():
    if os.path.exists(ARCHIVO_KB):
        with open(ARCHIVO_KB, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Base inicial
        kb = {
            "hola": "¡Hola!",
            "como estas": "¡Estoy bien, gracias! ¿Y tú?",
            "de que te gustaria hablar": "Podemos hablar de tecnología, deportes, música, lo que quieras."
        }
        guardar_kb(kb)
        return kb

# Función para guardar la base de conocimiento
def guardar_kb(kb):
    with open(ARCHIVO_KB, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=4)

# Función para buscar respuesta
def obtener_respuesta(kb, pregunta):
    pregunta_lower = pregunta.lower()
    for key in kb:
        if key in pregunta_lower:
            return kb[key]
    return None

# Chat interactivo
def chat():
    kb = cargar_kb()
    print("💬 Chatbot: ¡Hola! Soy un chatbot que puede aprender de ti.")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("💬 Chatbot: ¡Hasta luego!")
            break

        respuesta = obtener_respuesta(kb, user_input)
        if respuesta:
            print(f"💬 Chatbot: {respuesta}")
        else:
            # Aprendizaje de nuevas respuestas
            nueva_respuesta = input("💬 No entiendo. ¿Qué debería responder a eso? ")
            kb[user_input.lower()] = nueva_respuesta
            guardar_kb(kb)
            print("💬 Chatbot: ¡Gracias! Aprendí algo nuevo.")

if __name__ == "__main__":
    chat()