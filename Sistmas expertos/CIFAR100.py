import numpy as np
from tensorflow.keras.datasets import cifar100

# --------- Funciones auxiliares ---------

def one_hot(y, num_classes):
    y = y.astype(int)
    oh = np.zeros((y.size, num_classes), dtype=np.float32)
    oh[np.arange(y.size), y.flatten()] = 1.0
    return oh

def im2col(img, ksize, pad):
    N, C, H, W = img.shape
    x_pad = np.pad(img, ((0,0),(0,0),(pad,pad),(pad,pad)), mode='constant')
    cols = np.zeros((N, C, ksize, ksize, H, W), dtype=img.dtype)
    for i in range(ksize):
        for j in range(ksize):
            cols[:, :, i, j, :, :] = x_pad[:, :, i:i+H, j:j+W]
    cols = cols.transpose(0,4,5,1,2,3).reshape(N*H*W, -1)
    return cols

# --------- Capas ---------

class Layer:
    def forward(self, x): raise NotImplementedError
    def backward(self, grad): raise NotImplementedError
    def params_and_grads(self): return []

class ReLU(Layer):
    def forward(self, x): self.mask = (x > 0); return x * self.mask
    def backward(self, grad): return grad * self.mask

class Flatten(Layer):
    def forward(self, x): self.orig_shape = x.shape; return x.reshape(x.shape[0], -1)
    def backward(self, grad): return grad.reshape(self.orig_shape)

class Dense(Layer):
    def __init__(self, in_dim, out_dim):
        limit = np.sqrt(6 / (in_dim + out_dim))
        self.W = np.random.uniform(-limit, limit, (in_dim, out_dim)).astype(np.float32)
        self.b = np.zeros(out_dim, dtype=np.float32)
    def forward(self, x): self.x = x; return x @ self.W + self.b
    def backward(self, grad):
        self.dW = self.x.T @ grad / self.x.shape[0]
        self.db = grad.mean(axis=0)
        return grad @ self.W.T
    def params_and_grads(self): return [(self.W, self.dW), (self.b, self.db)]

class Conv2D(Layer):
    def __init__(self, in_channels, out_channels, ksize=3, pad=1):
        limit = np.sqrt(6 / (in_channels * ksize * ksize + out_channels))
        self.W = np.random.uniform(-limit, limit, (out_channels, in_channels, ksize, ksize)).astype(np.float32)
        self.b = np.zeros(out_channels, dtype=np.float32)
        self.pad = pad
        self.k = ksize
    def forward(self, x):
        self.x = x
        N, C, H, W = x.shape
        self.cols = im2col(x, self.k, self.pad)
        W_col = self.W.reshape(self.W.shape[0], -1)
        out = self.cols @ W_col.T + self.b
        return out.reshape(N, H, W, -1).transpose(0,3,1,2)
    def backward(self, grad):
        N, out_ch, H, W = grad.shape
        grad_reshaped = grad.transpose(0,2,3,1).reshape(-1, out_ch)
        W_col = self.W.reshape(out_ch, -1)
        dcols = grad_reshaped @ W_col
        self.dW = (grad_reshaped.T @ self.cols).reshape(self.W.shape) / N
        self.db = grad_reshaped.mean(axis=0)
        dx = np.zeros_like(self.x)
        C, k = self.W.shape[1], self.k
        p = self.pad
        for i in range(k):
            for j in range(k):
                idx = i * k + j
                dx[:, :, i:i+H, j:j+W] += dcols[:, C*idx:C*(idx+1)].reshape(N, H, W, C).transpose(0,3,1,2)
        return dx[:, :, p:-p, p:-p] if p else dx
    def params_and_grads(self): return [(self.W, self.dW), (self.b, self.db)]

class MaxPool2D(Layer):
    def __init__(self, ksize=2): self.k = ksize
    def forward(self, x):
        N, C, H, W = x.shape
        self.x = x
        x_reshaped = x.reshape(N, C, H//self.k, self.k, W//self.k, self.k)
        self.mask = (x_reshaped == x_reshaped.max(axis=(3,5), keepdims=True))
        return x_reshaped.max(axis=(3,5))
    def backward(self, grad):
        N, C, H, W = self.x.shape
        grad_repeat = grad[:, :, :, None, :, None] * self.mask
        return grad_repeat.reshape(N, C, H, W)

class SoftmaxCrossEntropy:
    def forward(self, logits, labels):
        exp = np.exp(logits - logits.max(axis=1, keepdims=True))
        self.probs = exp / exp.sum(axis=1, keepdims=True)
        self.labels = labels
        return -np.sum(labels * np.log(self.probs + 1e-7)) / logits.shape[0]
    def backward(self): return (self.probs - self.labels) / self.labels.shape[0]

class SGD:
    def __init__(self, lr=0.01, momentum=0.9): self.lr = lr; self.m = momentum; self.v = {}
    def step(self, params_grads):
        for i, (param, grad) in enumerate(params_grads):
            if i not in self.v: self.v[i] = np.zeros_like(grad)
            self.v[i] = self.m * self.v[i] - self.lr * grad
            param += self.v[i]

class CNN_CIFAR100:
    def __init__(self):
        self.layers = [
            Conv2D(3, 32, 3, 1), ReLU(), MaxPool2D(2),
            Conv2D(32, 64, 3, 1), ReLU(), MaxPool2D(2),
            Conv2D(64, 128, 3, 1), ReLU(), MaxPool2D(2),
            Flatten(),
            Dense(128*4*4, 512), ReLU(),
            Dense(512, 100)
        ]
        self.criterion = SoftmaxCrossEntropy()
        self.optimizer = SGD(lr=0.01, momentum=0.9)

    def forward(self, x):
        for layer in self.layers: x = layer.forward(x)
        return x

    def backward(self, grad):
        for layer in reversed(self.layers): grad = layer.backward(grad)

    def params_and_grads(self):
        for layer in self.layers:
            for p in layer.params_and_grads(): yield p

    def train_batch(self, x, y):
        logits = self.forward(x)
        loss = self.criterion.forward(logits, y)
        grad = self.criterion.backward()
        self.backward(grad)
        self.optimizer.step(self.params_and_grads())
        return loss, logits

    def predict(self, x): return self.forward(x).argmax(axis=1)

def batch_iter(X, y, batch_size=128, shuffle=True):
    idxs = np.arange(X.shape[0])
    if shuffle: np.random.shuffle(idxs)
    for start in range(0, len(idxs), batch_size):
        batch = idxs[start:start+batch_size]
        yield X[batch], y[batch]

def accuracy(model, X, y):
    preds = []
    for xb, _ in batch_iter(X, y, 256, shuffle=False):
        preds.append(model.predict(xb))
    preds = np.concatenate(preds)
    return (preds == y.argmax(axis=1)).mean()

def fit(model, X_train, y_train, X_val, y_val, epochs=50, batch_size=128):
    for epoch in range(1, epochs+1):
        losses = []
        for xb, yb in batch_iter(X_train, y_train, batch_size):
            loss, _ = model.train_batch(xb, yb)
            losses.append(loss)
        train_acc = accuracy(model, X_train, y_train)
        val_acc = accuracy(model, X_val, y_val)
        print(f"Época {epoch:3d} | Loss: {np.mean(losses):.4f} | Train acc: {train_acc:.3f} | Val acc: {val_acc:.3f}")

if __name__ == "__main__":
    # Descarga y carga datos con keras.datasets
    (X_train, y_train), (X_test, y_test) = cifar100.load_data(label_mode='fine')

    # Normaliza y adapta formato a (N, C, H, W)
    X_train = X_train.astype(np.float32) / 255.0
    X_test = X_test.astype(np.float32) / 255.0
    X_train = X_train.transpose(0,3,1,2)
    X_test = X_test.transpose(0,3,1,2)

    # One-hot encode labels
    y_train = one_hot(y_train, 100)
    y_test = one_hot(y_test, 100)

    # Split validación
    X_val, y_val = X_train[-5000:], y_train[-5000:]
    X_train, y_train = X_train[:-5000], y_train[:-5000]

    # Crear modelo y entrenar
    model = CNN_CIFAR100()
    fit(model, X_train, y_train, X_val, y_val, epochs=50)

    # Evaluar en test
    print("Test accuracy:", accuracy(model, X_test, y_test))
