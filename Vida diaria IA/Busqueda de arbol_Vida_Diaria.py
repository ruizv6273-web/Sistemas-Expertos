# Victor Alberto Ruiz Ruiz
from collections import deque

def bfs_minimum_spanning_tree(graph, start):
    tree_edges = []
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        for neighbor in sorted(graph[node]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                tree_edges.append((node, neighbor))
    return tree_edges

# Grafo: oficinas y salas conectadas por WiFi (sin pesos, solo conexiones posibles)
office_network = {
    'Router': ['Sala', 'Recepción'],
    'Sala': ['Router', 'Cocina', 'Oficina1'],
    'Recepción': ['Router', 'Oficina2'],
    'Cocina': ['Sala', 'Oficina3'],
    'Oficina1': ['Sala', 'Oficina4'],
    'Oficina2': ['Recepción', 'Oficina4'],
    'Oficina3': ['Cocina'],
    'Oficina4': ['Oficina1', 'Oficina2']
}

# Empezamos desde el Router principal
start_node = 'Router'
mst_edges = bfs_minimum_spanning_tree(office_network, start_node)

# Imprimir el "árbol de expansión" de la red WiFi
print("Red WiFi conectada sin redundancias (Árbol de expansión BFS):")
for edge in mst_edges:
    print(f"{edge[0]} → {edge[1]}")
