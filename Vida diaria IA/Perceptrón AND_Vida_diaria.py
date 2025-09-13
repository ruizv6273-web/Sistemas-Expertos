import numpy as np

# Función de activación: Escalón de Heaviside
def step_function(x):
    return 1 if x >= 0 else 0

# Datos de entrada para la compuerta AND
entradas = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# Salidas esperadas
salidas = np.array([0, 0, 0, 1])

# Inicializamos pesos y sesgo (bias)
pesos = np.random.rand(2)
bias = np.random.rand(1)
tasa_aprendizaje = 0.1
epocas = 20

# Entrenamiento
for epoca in range(epocas):
    print(f"Época {epoca+1}")
    for entrada, salida_esperada in zip(entradas, salidas):
        # Producto punto + bias
        suma = np.dot(entrada, pesos) + bias
        salida_obtenida = step_function(suma)

        # Error
        error = salida_esperada - salida_obtenida

        # Actualización de pesos y bias
        pesos += tasa_aprendizaje * error * entrada
        bias += tasa_aprendizaje * error
        print(f" Entrada: {entrada}, Esperada: {salida_esperada}, Obtenida: {salida_obtenida}, Pesos: {pesos}, Bias: {bias}")
    print()

# Prueba final
print("Pruebas finales del perceptrón:")
for entrada in entradas:
    salida = step_function(np.dot(entrada, pesos) + bias)
    print(f"{entrada} => {salida}")
