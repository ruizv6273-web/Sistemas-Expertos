import numpy as np
import matplotlib.pyplot as plt

# Datos reales simulados
# x = horas de estudio
# y = calificación obtenida (aproximada)
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([50, 55, 60, 65, 72, 78, 82, 88, 93, 97])

# Valores de w a probar (efecto de cada hora de estudio en la calificación)
w_values = np.linspace(0, 15, 200)
errors = []

# Calcular el error cuadrático medio para cada valor de w
for w in w_values:
    y_pred = w * x
    mse = np.mean((y - y_pred) ** 2)
    errors.append(mse)

# Encontrar el valor óptimo de w
min_index = np.argmin(errors)
w_min = w_values[min_index]
error_min = errors[min_index]

# Graficar
plt.plot(w_values, errors, label='ECM')
plt.scatter(w_min, error_min, color='red', label=f'Mínimo: w={w_min:.2f}')
plt.xlabel('w (incremento en calificación por hora de estudio)')
plt.ylabel('Error Cuadrático Medio (ECM)')
plt.title('Optimización de w en un ejemplo real (estudio vs calificación)')
plt.legend()
plt.grid(True)
plt.show()

print(f"El mejor valor de w es aproximadamente {w_min:.2f},")
print("lo que significa que cada hora de estudio aumenta la calificación en ese valor.")
