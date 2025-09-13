import pandas as pd
from sklearn.linear_model import LinearRegression

# Datos históricos de ejemplo: duración en minutos y prioridad real asignada por el usuario
historial = pd.DataFrame({
    "duracion": [10, 30, 45, 60, 120],
    "prioridad": [2, 3, 3, 4, 5]
})

# Entrenar modelo de IA
X = historial[["duracion"]]
y = historial["prioridad"]
modelo = LinearRegression()
modelo.fit(X, y)

# Lista de tareas nuevas
tareas = []
print("📋 Gestor de Tareas con IA")
print("Ingresa tus tareas. Escribe 'fin' cuando termines.\n")

while True:
    nombre = input("👉 Nombre de la tarea (o 'fin' para terminar): ")
    if nombre.lower() == "fin":
        break
    try:
        duracion = int(input("   Duración aproximada (minutos): "))
    except ValueError:
        print("⚠️ Duración debe ser un número. Intenta de nuevo.")
        continue
    
    # Predecir prioridad usando la IA
    prioridad_predicha = modelo.predict([[duracion]])[0]
    prioridad_predicha = round(max(1, min(prioridad_predicha, 5)), 1)  # Limitar entre 1 y 5
    
    tareas.append({
        "nombre": nombre,
        "duracion": duracion,
        "prioridad": prioridad_predicha
    })

# Ordenar tareas por prioridad predicha (mayor a menor)
tareas_ordenadas = sorted(tareas, key=lambda x: x["prioridad"], reverse=True)

# Mostrar resultado
print("\n✅ Orden de tareas sugerido por la IA:\n")
for t in tareas_ordenadas:
    print(f"- {t['nombre']} (Prioridad {t['prioridad']}, {t['duracion']} min)")