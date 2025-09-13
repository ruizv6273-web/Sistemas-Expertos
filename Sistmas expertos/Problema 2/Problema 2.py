import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# 1. Datos XOR
# ----------------------------
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([
    [0],
    [1],
    [1],
    [0]
])

# ----------------------------
# 2. Funciones de activación
# ----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)

# ----------------------------
# 3. Inicialización
# ----------------------------
np.random.seed(42)
input_size = 2
hidden_size = 4
output_size = 1
lr = 0.1
epochs = 10000

W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

losses = []

# ----------------------------
# 4. Entrenamiento
# ----------------------------
for epoch in range(epochs):
    # Forward
    Z1 = X @ W1 + b1
    A1 = sigmoid(Z1)
    Z2 = A1 @ W2 + b2
    y_pred = sigmoid(Z2)

    # Error
    error = y_pred - y
    loss = np.mean(error**2)
    losses.append(loss)

    # Backprop
    dZ2 = error * sigmoid_deriv(Z2)
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0, keepdims=True)

    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * sigmoid_deriv(Z1)
    dW1 = X.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    # Update
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    if epoch % 1000 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.5f}")

# ----------------------------
# 5. Resultados
# ----------------------------
print("\nResultados finales:")
for i in range(4):
    print(f"Entrada: {X[i]} -> Salida esperada: {y[i][0]} | Salida estimada: {y_pred[i][0]:.4f}")

# ----------------------------
# 6. Gráfica de error
# ----------------------------
plt.plot(losses)
plt.title("Error cuadrático medio (MSE) vs Épocas")
plt.xlabel("Época")
plt.ylabel("MSE")
plt.grid(True)
plt.savefig("error_problema_2.png")
plt.show()
