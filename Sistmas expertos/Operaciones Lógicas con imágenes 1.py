import cv2
import numpy as np

# Crear dos imágenes negras de 400x600
img1 = np.zeros((400,600), dtype=np.uint8)
img2 = np.zeros((400,600), dtype=np.uint8)

# Dibujar un rectángulo blanco en img1
img1[100:300, 200:400] = 255

# Dibujar un círculo blanco en img2
img2 = cv2.circle(img2, (300,200), 125, (255), -1)

# Operaciones lógicas
AND = cv2.bitwise_and(img1, img2)
OR  = cv2.bitwise_or(img1, img2)
XOR = cv2.bitwise_xor(img1, img2)
NOT = cv2.bitwise_not(img1)

# Mostrar imágenes originales
cv2.imshow('Imagen 1 (Rectángulo)', img1)
cv2.imshow('Imagen 2 (Círculo)', img2)

# Mostrar resultados de operaciones
cv2.imshow('AND', AND)
cv2.imshow('OR', OR)
cv2.imshow('XOR', XOR)
cv2.imshow('NOT (de img1)', NOT)

# Esperar a que se presione una tecla y cerrar todo
cv2.waitKey(0)
cv2.destroyAllWindows()
