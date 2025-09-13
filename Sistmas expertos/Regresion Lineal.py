import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
y = np.array([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])

# Valores de w a probar
w_values = np.linspace(0, 3, 100)
errors = []

# Calcular el error cuadrático medio para cada valor de w
for w in w_values:
    y_pred = w * x
    mse = np.mean((y - y_pred) ** 2)
    errors.append(mse)

# Graficar
plt.plot(w_values, errors)
plt.xlabel('w')
plt.ylabel('Error Cuadrático Medio (ECM)')
plt.title('w vs Error')
plt.grid(True)
plt.show()
