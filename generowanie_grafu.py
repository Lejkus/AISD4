import random
from collections import deque

class Graph:
    def __init__(self, vertices_count):
        self.n = vertices_count
        self.adjacency = {v: set() for v in range(1, vertices_count + 1)}
        self.hamiltonian_cycle = []

    def add_edge(self, u, v):
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)

    def remove_edge(self, u, v):
        self.adjacency[u].discard(v)
        self.adjacency[v].discard(u)

    def has_edge(self, u, v):
        return v in self.adjacency[u]

    def vertex_degree(self, v):
        return len(self.adjacency[v])

    def is_eulerian(self):
        return all(self.vertex_degree(v) % 2 == 0 for v in self.adjacency)

    def is_connected(self):#BFS - przeszukiwanie wszerz
        visited = set()
        queue = deque([1])
        while queue:
            u = queue.popleft()
            if u not in visited:
                visited.add(u)
                queue.extend(self.adjacency[u] - visited)
        return len(visited) == self.n

    def generate_hamiltonian_cycle(self):
        vertices = list(range(1, self.n + 1))
        random.shuffle(vertices)
        self.hamiltonian_cycle = vertices + [vertices[0]]
        for i in range(self.n):
            self.add_edge(vertices[i], vertices[(i + 1) % self.n])

    def add_edges_with_triangles(self, target_saturation):
        max_edges = self.n * (self.n - 1) // 2
        current_edges = sum(len(adj) for adj in self.adjacency.values()) // 2
        target_edges = int(target_saturation * max_edges)

        while current_edges < target_edges:
            nodes = random.sample(range(1, self.n + 1), 3)
            a, b, c = nodes

            added = 0
            if not self.has_edge(a, b):
                self.add_edge(a, b)
                added += 1
            if not self.has_edge(b, c):
                self.add_edge(b, c)
                added += 1
            if not self.has_edge(c, a):
                self.add_edge(c, a)
                added += 1

            current_edges += added // 2

            if current_edges >= max_edges:
                break

    def ensure_even_degrees(self):
        while True:
            odd_vertices = [v for v in self.adjacency if self.vertex_degree(v) % 2 != 0]

            if not odd_vertices:
                break

            if len(odd_vertices) % 2 != 0:
                raise RuntimeError("Nie można uzyskać parzystych stopni")

            u, v = random.sample(odd_vertices, 2)

            if self.has_edge(u, v):
                self.remove_edge(u, v)
            else:
                self.add_edge(u, v)

    def ensure_connectivity(self):
        if self.is_connected():
            return

        components = []
        visited = set()

        for v in range(1, self.n + 1):
            if v not in visited:
                component = set()
                queue = deque([v])

                while queue:
                    u = queue.popleft()
                    if u not in visited:
                        visited.add(u)
                        component.add(u)
                        queue.extend(self.adjacency[u] - visited)

                components.append(component)

        for i in range(len(components) - 1):
            u = random.choice(list(components[i]))
            v = random.choice(list(components[i + 1]))
            self.add_edge(u, v)

        self.ensure_even_degrees()
    def non_hamilton(self):
        vertex=random.choice(self.hamiltonian_cycle)
        neighbors = list(self.adjacency[vertex])

        for neighbor in neighbors:
            # Usuń krawędź w obie strony
            self.adjacency[vertex].remove(neighbor)
            self.adjacency[neighbor].remove(vertex)

        # Po izolacji wierzchołek powinien mieć pustą listę sąsiadów
        assert len(self.adjacency[vertex]) == 0
def generowanie(wierzcholki,nasycenie,hamil):
    vertices_count=wierzcholki
    graph = Graph(vertices_count)
    match hamil:
        case "hamil":
            graph.generate_hamiltonian_cycle()
            graph.add_edges_with_triangles(nasycenie)
            graph.ensure_even_degrees()
            graph.ensure_connectivity()
            print("\n[Cykl Hamiltona]:", " → ".join(map(str, graph.hamiltonian_cycle)))
        case "non-hamil":
            graph.generate_hamiltonian_cycle()
            graph.add_edges_with_triangles(nasycenie)
            graph.ensure_even_degrees()
            graph.ensure_connectivity()
            print("Fuck you")
if __name__ == "__main__":
    print("Generowanie grafu")