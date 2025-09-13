import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ----------------------------
# 1. Cargar datos del repositorio UCI
# ----------------------------
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
columnas = ['id', 'diagnosis'] + [f'feat_{i}' for i in range(1, 31)]
data = pd.read_csv(url, header=None, names=columnas)

# Convertir etiquetas a binario: M=1, B=0
data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

# Datos y etiquetas
X = data.drop(columns=['id', 'diagnosis']).values
y = data['diagnosis'].values.reshape(-1, 1)

# Normalización
scaler = StandardScaler()
X = scaler.fit_transform(X)

# División en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------
# 2. Funciones de red neuronal
# ----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)

# ----------------------------
# 3. Inicialización
# ----------------------------
np.random.seed(1)
input_size = X_train.shape[1]
hidden_size = 10
output_size = 1
lr = 0.1
epochs = 1000

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
    Z1 = X_train @ W1 + b1
    A1 = sigmoid(Z1)
    Z2 = A1 @ W2 + b2
    y_pred = sigmoid(Z2)

    # Error (binary cross-entropy)
    loss = np.mean((y_pred - y_train) ** 2)
    losses.append(loss)

    # Backprop
    dZ2 = 2 * (y_pred - y_train) * sigmoid_deriv(Z2)
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0, keepdims=True)

    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * sigmoid_deriv(Z1)
    dW1 = X_train.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    # Update
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.5f}")

# ----------------------------
# 5. Evaluación
# ----------------------------
# Prueba
Z1 = X_test @ W1 + b1
A1 = sigmoid(Z1)
Z2 = A1 @ W2 + b2
y_test_pred = sigmoid(Z2)
y_test_class = (y_test_pred > 0.5).astype(int)

accuracy = np.mean(y_test_class == y_test)
print(f"\nPrecisión en test: {accuracy * 100:.2f}%")

# ----------------------------
# 6. Gráficas
# ----------------------------
# Error
plt.figure()
plt.plot(losses)
plt.title("Error MSE vs Épocas")
plt.xlabel("Época")
plt.ylabel("MSE")
plt.grid(True)
plt.savefig("error_problema_3.png")
plt.show()

# Comparación de etiquetas
plt.figure()
plt.plot(y_test[:50], label='Real')
plt.plot(y_test_pred[:50], 'x', label='Estimado')
plt.title("Comparación salida real vs estimada")
plt.xlabel("Muestra")
plt.ylabel("Etiqueta")
plt.legend()
plt.grid(True)
plt.savefig("salida_vs_real_problema_3.png")
plt.show()
