from collections import defaultdict
import random
from typing import List, Dict, Set

class UndirectedGraph:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.adjacency_list: Dict[int, Set[int]] = defaultdict(set)

    def add_edge(self, node_a: int, node_b: int):
        if node_a != node_b:
            self.adjacency_list[node_a].add(node_b)
            self.adjacency_list[node_b].add(node_a)

    def edge_count(self) -> int:
        return sum(len(neighbors) for neighbors in self.adjacency_list.values()) // 2

    def total_possible_edges(self) -> int:
        return self.num_nodes * (self.num_nodes - 1) // 2

    def is_all_degrees_even(self) -> bool:
        return all(len(neighbors) % 2 == 0 for neighbors in self.adjacency_list.values())

    def create_triangle(self, a: int, b: int, c: int):
        self.add_edge(a, b)
        self.add_edge(b, c)
        self.add_edge(c, a)

    def add_short_cycles_for_even_degrees(self, max_attempts: int = 1000):
        attempts = 0
        while not self.is_all_degrees_even() and attempts < max_attempts:
            a, b, c = random.sample(range(self.num_nodes), 3)
            self.create_triangle(a, b, c)
            attempts += 1

    def generate_hamiltonian_cycle(self):
        nodes = list(range(self.num_nodes))
        random.shuffle(nodes)
        for i in range(len(nodes)):
            self.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])

    def fill_to_saturation(self, saturation_percent: int):
        target_edges = int(self.total_possible_edges() * (saturation_percent / 100))
        while self.edge_count() < target_edges:
            u, v = random.sample(range(self.num_nodes), 2)
            self.add_edge(u, v)

    def isolate_node(self, node_index: int = 0):
        for neighbor in list(self.adjacency_list[node_index]):
            self.adjacency_list[neighbor].remove(node_index)
        self.adjacency_list[node_index] = set()

    def display_adjacency_list(self):
        print("Graph (adjacency list):")
        for node in range(self.num_nodes):
            print(f"{node}: {sorted(self.adjacency_list[node])}")