import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

# ----------------------------
# 1. Cargar dataset
# ----------------------------
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
data = pd.read_csv(url, sep=';')

# Variables
X = data.drop('quality', axis=1).values
y = data['quality'].values.reshape(-1, 1)

# Escalar
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------
# 2. Funciones de red
# ----------------------------
def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(float)

def mse(y_true, y_pred):
    return np.mean((y_pred - y_true) ** 2)

# ----------------------------
# 3. Inicialización
# ----------------------------
np.random.seed(0)
input_size = X.shape[1]
hidden_size = 16
output_size = 1
lr = 0.01
epochs = 1000

W1 = np.random.randn(input_size, hidden_size) * 0.1
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size) * 0.1
b2 = np.zeros((1, output_size))

losses = []

# ----------------------------
# 4. Entrenamiento
# ----------------------------
for epoch in range(epochs):
    # Forward
    Z1 = X_train @ W1 + b1
    A1 = relu(Z1)
    Z2 = A1 @ W2 + b2
    y_pred = Z2

    # Error
    loss = mse(y_train, y_pred)
    losses.append(loss)

    # Backprop
    dZ2 = 2 * (y_pred - y_train) / len(y_train)
    dW2 = A1.T @ dZ2
    db2 = np.sum(dZ2, axis=0, keepdims=True)

    dA1 = dZ2 @ W2.T
    dZ1 = dA1 * relu_deriv(Z1)
    dW1 = X_train.T @ dZ1
    db1 = np.sum(dZ1, axis=0, keepdims=True)

    # Update
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.4f}")

# ----------------------------
# 5. Evaluación
# ----------------------------
Z1_test = X_test @ W1 + b1
A1_test = relu(Z1_test)
Z2_test = A1_test @ W2 + b2
y_test_pred = Z2_test

test_loss = mse(y_test, y_test_pred)
mae = mean_absolute_error(y_test, y_test_pred)
r2 = r2_score(y_test, y_test_pred)

print(f"\nMSE en test: {test_loss:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# ----------------------------
# 6. Gráficas
# ----------------------------

# Curva de pérdida
plt.figure(figsize=(8, 5))
plt.plot(losses, label="MSE Loss")
plt.xlabel("Épocas")
plt.ylabel("Pérdida")
plt.title("Curva de pérdida durante el entrenamiento")
plt.grid(True)
plt.legend()
plt.savefig("loss_curve.png")
plt.close()

# Gráfica de predicciones vs reales
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_test_pred, alpha=0.5, color='royalblue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Calidad real")
plt.ylabel("Calidad estimada")
plt.title("Comparación entre valores reales y predichos")
plt.grid(True)
plt.savefig("prediction_vs_true.png")
plt.close()


