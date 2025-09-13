# Victor Alberto Ruiz Ruiz
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances

# Grafo representando una ciudad
# Los pesos son "minutos de trayecto" en auto
city_map = {
    'Casa': {'Tienda': 5, 'Escuela': 10},
    'Tienda': {'Casa': 5, 'Escuela': 3, 'Hospital': 7},
    'Escuela': {'Casa': 10, 'Tienda': 3, 'Parque': 4},
    'Hospital': {'Tienda': 7, 'Parque': 2, 'Oficina': 6},
    'Parque': {'Escuela': 4, 'Hospital': 2, 'Oficina': 8},
    'Oficina': {'Hospital': 6, 'Parque': 8}
}

# Ejecutamos desde la Casa
start_place = 'Casa'
result = dijkstra(city_map, start_place)

print(f"Tiempo mínimo de trayecto desde '{start_place}':")
for place, time in result.items():
    print(f" - {place}: {time} minutos")
