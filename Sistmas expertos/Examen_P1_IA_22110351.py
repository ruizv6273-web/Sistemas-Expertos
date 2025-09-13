#Victor Alberto Ruiz Ruiz

import numpy as np
import matplotlib.pyplot as plt
import heapq

# Definición de la clase Nodo para representar los estados del algoritmo A*
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # La posición (coordenadas) del nodo en el mapa
        self.parent = parent  # Nodo padre para reconstruir el camino una vez encontrado
        self.g = 0  # Costo desde el nodo inicial hasta este nodo
        self.h = 0  # Heurística (estimación de la distancia al objetivo)
        self.f = 0  # Costo total (g + h), utilizado para decidir el próximo nodo a explorar

    # Método para comparar nodos en la cola de prioridad (heap), basado en el costo total f
    def __lt__(self, other):
        return self.f < other.f

# Función heurística: Calcula la distancia Manhattan entre dos puntos (útil para la estimación en A*)
def heuristic(a, b):
    # La distancia Manhattan es la suma de las diferencias absolutas en las coordenadas
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementación del algoritmo A*
def a_star(grid, start, goal):
    open_list = []  # Lista de nodos por explorar (se usa una cola de prioridad)
    closed_set = set()  # Conjunto de nodos ya explorados
    start_node = Node(start)  # Nodo de inicio
    goal_node = Node(goal)  # Nodo objetivo
    heapq.heappush(open_list, start_node)  # Agregar nodo inicial a la lista abierta
    
    while open_list:
        # Extraer el nodo con menor costo total (f)
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)  # Marcar el nodo como explorado
        
        # Si hemos llegado al objetivo, reconstruimos el camino
        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)  # Añadimos la posición del nodo al camino
                current_node = current_node.parent  # Seguimos al nodo padre
            return path[::-1]  # Devolvemos el camino invertido (de inicio a fin)
        
        # Movimientos posibles: arriba, abajo, izquierda, derecha
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in neighbors:
            # Calculamos la posición del vecino
            neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)
            
            # Validamos que el vecino esté dentro de los límites del mapa y no sea un obstáculo
            if (neighbor_pos[0] < 0 or neighbor_pos[0] >= grid.shape[0] or
                neighbor_pos[1] < 0 or neighbor_pos[1] >= grid.shape[1] or
                grid[neighbor_pos] == 1 or neighbor_pos in closed_set):
                continue  # Si es inválido, lo saltamos
            
            # Creación del nodo vecino
            neighbor = Node(neighbor_pos, current_node)
            neighbor.g = current_node.g + 1  # El costo al vecino es 1 más que el costo al nodo actual
            neighbor.h = heuristic(neighbor_pos, goal_node.position)  # Heurística (distancia al objetivo)
            neighbor.f = neighbor.g + neighbor.h  # Costo total (g + h)
            
            # Verificamos si ya existe un nodo con la misma posición y un menor costo total
            if any(open_node.position == neighbor.position and open_node.f <= neighbor.f for open_node in open_list):
                continue  # Si es así, no agregamos el nodo a la lista abierta
            
            # Agregamos el nodo vecino a la lista abierta
            heapq.heappush(open_list, neighbor)
    
    return None  # Si no se encuentra un camino, devolvemos None

# Funciones para crear diferentes mapas con obstáculos
def create_map_1():
    grid = np.zeros((20, 20))  # Crear un mapa vacío de 20x20
    grid[5:7, 3:15] = 1  # Obstáculo horizontal
    grid[7:15, 10:12] = 1  # Obstáculo vertical
    return grid

def create_map_2():
    grid = np.zeros((20, 20))
    grid[8:12, 4:16] = 1  # Obstáculo horizontal
    grid[2:14, 8:10] = 1  # Obstáculo vertical
    return grid

def create_map_3():
    grid = np.zeros((20, 20))
    grid[3:10, 6:8] = 1  # Obstáculo vertical
    grid[10:15, 12:14] = 1  # Otro obstáculo vertical
    grid[6:8, 10:18] = 1  # Obstáculo horizontal
    return grid

# Función para graficar el mapa y el camino encontrado
def plot_path_with_grid(grid, start, goal, title):
    path = a_star(grid, start, goal)  # Llamamos a A* para encontrar el camino

    plt.figure(figsize=(6,6))  # Establecer el tamaño de la figura
    plt.imshow(grid, cmap="gray_r")  # Mostrar el mapa en escala de grises (1 = obstáculo, 0 = espacio libre)

    # Graficamos el camino encontrado (si existe)
    if path:
        path_x, path_y = zip(*path)  # Desempaquetamos las coordenadas del camino
        plt.plot(path_y, path_x, color='blue', linewidth=2, label='Path')  # Dibujamos el camino en azul

    # Marcamos el inicio y el objetivo en el mapa
    plt.scatter(start[1], start[0], c='green', s=100, label='Start')  # Marcamos el punto de inicio (verde)
    plt.scatter(goal[1], goal[0], c='red', s=100, label='Goal')  # Marcamos el objetivo (rojo)

    plt.legend()  # Mostrar leyenda
    plt.title(title)  # Título de la gráfica
    plt.xticks(ticks=range(grid.shape[1]))  # Etiquetas del eje X
    plt.yticks(ticks=range(grid.shape[0]))  # Etiquetas del eje Y
    plt.grid(visible=True, color='black', linewidth=0.5)  # Mostrar la cuadrícula del mapa
    
    # Guardar la imagen en formato PNG
    plt.savefig(f"{title}.png")
    plt.show()  # Mostrar la gráfica

# Definir mapas con obstáculos y puntos de inicio y objetivo
maps = [create_map_1(), create_map_2(), create_map_3()]
start_positions = [(2, 2), (1, 1), (3, 3)]  # Coordenadas de los puntos de inicio
goal_positions = [(18, 18), (18, 18), (17, 17)]  # Coordenadas de los puntos de objetivo

# Generar imágenes con los caminos encontrados en los tres mapas
for i in range(3):
    plot_path_with_grid(maps[i], start_positions[i], goal_positions[i], f"Mapa_{i+1}_AStar")
