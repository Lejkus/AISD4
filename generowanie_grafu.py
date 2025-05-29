import random
import math
from typing import List
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

    def is_connected(self):
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
            a, b, c = random.sample(range(1, self.n + 1), 3)
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
        vertex = random.choice(self.hamiltonian_cycle)
        neighbors = list(self.adjacency[vertex])
        for neighbor in neighbors:
            self.adjacency[vertex].remove(neighbor)
            self.adjacency[neighbor].remove(vertex)
        assert len(self.adjacency[vertex]) == 0

    def get_adjacency_matrix(self):
        matrix = [[0] * (self.n + 1) for _ in range(self.n + 1)]
        for u in self.adjacency:
            for v in self.adjacency[u]:
                matrix[u][v] = 1
        return matrix

    def get_incidence_matrix(self):
        edges = [(u, v) for u in range(1, self.n + 1)
                 for v in self.adjacency[u] if u < v]
        matrix = [[0] * len(edges) for _ in range(self.n + 1)]
        for idx, (u, v) in enumerate(edges):
            matrix[u][idx] = 1
            matrix[v][idx] = 1
        return matrix

    def get_edge_list(self):
        return sorted({(min(u, v), max(u, v)) for u in self.adjacency for v in self.adjacency[u]})

    def get_adjacency_list(self):
        return {v: sorted(neighbors) for v, neighbors in self.adjacency.items()}

    def find_euler_cycle(self):
        if not self.is_eulerian():
            print("Graf nie ma cyklu Eulera!")
            return

        graph_copy = {u: set(v) for u, v in self.adjacency.items()}
        stack = [1]
        path = []
        while stack:
            current = stack[-1]
            if graph_copy[current]:
                neighbor = graph_copy[current].pop()
                graph_copy[neighbor].remove(current)
                stack.append(neighbor)
            else:
                path.append(stack.pop())
        print("Cykl Eulera:")
        print(" -> ".join(map(str, path[::-1])))

    def find_hamilton_cycle(self):
        def backtrack(current: int, visited: dict, path: List[int]) -> bool:
            if len(path) == self.n:
                return path[0] in self.adjacency[path[-1]]
            for neighbor in self.adjacency[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    path.append(neighbor)
                    if backtrack(neighbor, visited, path):
                        return True
                    visited[neighbor] = False
                    path.pop()
            return False

        for start in range(1, self.n + 1):
            visited = {v: False for v in range(1, self.n + 1)}
            path = [start]
            visited[start] = True
            if backtrack(start, visited, path):
                path.append(path[0])
                print("Cykl Hamiltona:")
                print(" -> ".join(map(str, path)))
                return
        print("Nie znaleziono cyklu Hamiltona.")

    def export_to_tikz(self, filename=None):
        tikz = """\\documentclass{standalone}
    \\usepackage{tikz}
    \\begin{document}
    \\begin{tikzpicture}[every node/.style={draw, circle, thick, minimum size=7mm}]
    """
        angle_step = 360 / self.n
        positions = {}

        for i, node in enumerate(range(1, self.n + 1)):
            angle = i * angle_step
            x = 5 * math.cos(math.radians(angle))
            y = 5 * math.sin(math.radians(angle))
            positions[node] = (x, y)

        # Draw nodes
        for node, (x, y) in positions.items():
            tikz += f"  \\node ({node}) at ({x:.2f},{y:.2f}) {{{node}}};\n"

        drawn = set()
        for u in self.adjacency:
            for v in self.adjacency[u]:
                if (u, v) not in drawn and (v, u) not in drawn:
                    tikz += f"  \\draw[thick] ({u}) -- ({v});\n"
                    drawn.add((u, v))

        # Draw Hamiltonian cycle in red (if present)
        if self.hamiltonian_cycle:
            for i in range(len(self.hamiltonian_cycle) - 1):
                u = self.hamiltonian_cycle[i]
                v = self.hamiltonian_cycle[i + 1]
                tikz += f"  \\draw[red, very thick] ({u}) -- ({v});\n"

        tikz += """\\end{tikzpicture}
    \\end{document}
    """

        # Save to file if filename is provided
        if filename:
            with open(filename, 'w') as f:
                f.write(tikz)

        # Also print to console
        print(tikz)


def generowanie(vertices, saturation, mode):
    graph = Graph(vertices)
    if mode == "hamil":
        graph.generate_hamiltonian_cycle()
        graph.add_edges_with_triangles(saturation)
        graph.ensure_even_degrees()
        graph.ensure_connectivity()
        print("\n[Cykl Hamiltona]:", " → ".join(map(str, graph.hamiltonian_cycle)))
    elif mode == "non-hamil":
        graph.generate_hamiltonian_cycle()
        graph.add_edges_with_triangles(saturation)
        graph.ensure_even_degrees()
        graph.ensure_connectivity()
        print("\n[Cykl Hamiltona]:", " → ".join(map(str, graph.hamiltonian_cycle)))
        graph.non_hamilton()
        print("Graf został wygenerowany!")
        print(graph.get_adjacency_list())
    return graph

if __name__ == "__main__":
    print("Generowanie grafu")
