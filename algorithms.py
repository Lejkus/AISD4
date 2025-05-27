from typing import List
from graph import UndirectedGraph


def find_euler_cycle(graph: UndirectedGraph):
    if not graph.is_all_degrees_even():
        print("Euler cycle does not exist: not all degrees are even.")
        return

    graph_copy = {u: set(v) for u, v in graph.adjacency_list.items()}
    stack = [0]
    path = []

    while stack:
        current = stack[-1]
        if graph_copy[current]:
            neighbor = graph_copy[current].pop()
            graph_copy[neighbor].remove(current)
            stack.append(neighbor)
        else:
            path.append(stack.pop())

    print("Euler cycle:")
    print(" -> ".join(map(str, path[::-1])))

def find_hamilton_cycle(graph: UndirectedGraph):
    def backtrack(current: int, visited: List[bool], path: List[int]) -> bool:
        if len(path) == graph.num_nodes:
            if path[0] in graph.adjacency_list[path[-1]]:
                path.append(path[0])
                return True
            return False

        for neighbor in graph.adjacency_list[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                path.append(neighbor)
                if backtrack(neighbor, visited, path):
                    return True
                visited[neighbor] = False
                path.pop()

        return False

    for start_node in range(graph.num_nodes):
        visited = [False] * graph.num_nodes
        path = [start_node]
        visited[start_node] = True
        if backtrack(start_node, visited, path):
            print("Hamilton cycle:")
            print(" -> ".join(map(str, path)))
            return

    print("No Hamilton cycle found.")
