import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# 1. Generar datos de entrenamiento
# ----------------------------
np.random.seed(0)
N = 1000
X = np.random.uniform(-5, 5, (N, 4))

# Función objetivo a aproximar
def funcion_objetivo(X):
    x1, x2, x3, x4 = X[:, 0], X[:, 1], X[:, 2], X[:, 3]
    return x1 * x2 + np.sin(x3) - np.log(np.abs(x4) + 2)

y = funcion_objetivo(X).reshape(-1, 1)

# Normalización de entradas y salidas
X_mean, X_std = X.mean(axis=0), X.std(axis=0)
X_norm = (X - X_mean) / X_std

y_mean, y_std = y.mean(), y.std()
y_norm = (y - y_mean) / y_std

# ----------------------------
# 2. Red neuronal desde cero
# ----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)

# Arquitectura
input_size = 4
hidden_size = 16
output_size = 1
lr = 0.01
epochs = 500

# Pesos y bias
W1 = np.random.randn(input_size, hidden_size) * 0.1
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size) * 0.1
b2 = np.zeros((1, output_size))

losses = []

# ----------------------------
# 3. Entrenamiento
# ----------------------------
for epoch in range(epochs):
    # Forward
    Z1 = X_norm @ W1 + b1
    A1 = sigmoid(Z1)
    Z2 = A1 @ W2 + b2
    y_pred = Z2

    # Error (MSE)
    error = y_pred - y_norm
    loss = np.mean(error ** 2)
    losses.append(loss)

    # Backprop
    dZ2 = 2 * error / N
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0, keepdims=True)

    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * sigmoid_deriv(Z1)
    dW1 = X_norm.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    # Actualizar pesos
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    if epoch % 50 == 0:
        print(f"Epoch {epoch}, MSE: {loss:.5f}")

# ----------------------------
# 4. Resultados y gráficas
# ----------------------------
# Salida denormalizada
y_pred_real = y_pred * y_std + y_mean

# Graficar error
plt.figure()
plt.plot(losses)
plt.title("Error cuadrático medio (MSE) vs Épocas")
plt.xlabel("Época")
plt.ylabel("MSE")
plt.grid(True)
plt.savefig("error_problema_1.png")
plt.show()

# Comparación real vs estimado
plt.figure()
plt.scatter(range(100), y[:100], label="Real")
plt.scatter(range(100), y_pred_real[:100], label="Estimado", marker='x')
plt.legend()
plt.title("Comparación salida real vs estimada")
plt.xlabel("Muestra")
plt.ylabel("Valor")
plt.grid(True)
plt.savefig("salida_vs_real_problema_1.png")
plt.show()
