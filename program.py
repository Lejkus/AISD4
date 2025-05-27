import argparse
import random
from collections import defaultdict, deque

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = defaultdict(set)

    def add_edge(self, u, v):
        if u != v:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def degree_even(self):
        return all(len(self.adj[v]) % 2 == 0 for v in self.adj)

    def print_graph(self):
        print("Graph (adjacency list):")
        for u in range(self.n):
            print(f"{u}: {sorted(self.adj[u])}")

    def edge_count(self):
        return sum(len(neigh) for neigh in self.adj.values()) // 2

    def total_possible_edges(self):
        return self.n * (self.n - 1) // 2

    def add_short_cycles_for_even_degrees(self):
        attempts = 0
        while not self.degree_even() and attempts < 1000:
            a, b, c = random.sample(range(self.n), 3)
            self.add_edge(a, b)
            self.add_edge(b, c)
            self.add_edge(c, a)
            attempts += 1

    def generate_hamiltonian_cycle(self):
        nodes = list(range(self.n))
        random.shuffle(nodes)
        for i in range(len(nodes)):
            self.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])

    def fill_to_saturation(self, target_saturation):
        target_edges = int(self.total_possible_edges() * (target_saturation / 100))
        while self.edge_count() < target_edges:
            u, v = random.sample(range(self.n), 2)
            self.add_edge(u, v)

    def isolate_node(self):
        # Isolate node 0 by removing all its edges
        for neighbor in list(self.adj[0]):
            self.adj[neighbor].remove(0)
        self.adj[0] = set()

    def find_euler_cycle(self):
        if not self.degree_even():
            print("Euler cycle does not exist: not all degrees are even.")
            return

        graph_copy = {u: set(v) for u, v in self.adj.items()}
        stack = [0]
        path = []

        while stack:
            u = stack[-1]
            if graph_copy[u]:
                v = graph_copy[u].pop()
                graph_copy[v].remove(u)
                stack.append(v)
            else:
                path.append(stack.pop())

        print("Euler cycle:")
        print(" -> ".join(map(str, path[::-1])))

    def find_hamilton_cycle(self):
        path = []

        def backtrack(v, visited):
            if len(path) == self.n:
                if path[0] in self.adj[path[-1]]:
                    path.append(path[0])
                    return True
                return False

            for neighbor in self.adj[v]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    path.append(neighbor)
                    if backtrack(neighbor, visited):
                        return True
                    visited[neighbor] = False
                    path.pop()

            return False

        for start in range(self.n):
            visited = [False] * self.n
            path = [start]
            visited[start] = True
            if backtrack(start, visited):
                print("Hamilton cycle:")
                print(" -> ".join(map(str, path)))
                return
        print("No Hamilton cycle found.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hamilton', action='store_true')
    parser.add_argument('--non-hamilton', action='store_true')
    parser.add_argument('--nodes', type=int, required=True)
    parser.add_argument('--saturation', type=int, required=False)
    args = parser.parse_args()

    g = Graph(args.nodes)

    if args.hamilton:
        if args.nodes <= 10:
            print("Number of nodes must be greater than 10.")
            return
        sat = args.saturation or 30
        print(f"(a) Generowanie grafu hamiltonowskiego z nasyceniem {sat}%")
        g.generate_hamiltonian_cycle()
        g.fill_to_saturation(sat)
        g.add_short_cycles_for_even_degrees()

    elif args.non_hamilton:
        print(f"(b) Generowanie grafu nie-hamiltonowskiego z nasyceniem 50%")
        g.generate_hamiltonian_cycle()
        g.fill_to_saturation(50)
        g.isolate_node()

    g.print_graph()

    print("\nOperacje na grafie:")
    g.find_euler_cycle()
    g.find_hamilton_cycle()

if __name__ == "__main__":
    main()
