import argparse
from graph import UndirectedGraph
from algorithms import find_euler_cycle, find_hamilton_cycle


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Hamiltonian or Non-Hamiltonian graphs.")
    parser.add_argument("--hamilton", action="store_true", help="Generate a Hamiltonian graph")
    parser.add_argument("--non-hamilton", action="store_true", help="Generate a Non-Hamiltonian graph")
    parser.add_argument("nodes", type=int, help="Number of nodes (must be > 10)")
    parser.add_argument("saturation", type=int, help="Edge saturation percentage (e.g., 30, 50, 70)")

    args = parser.parse_args()

    if args.nodes <= 10:
        raise ValueError("Number of nodes must be greater than 10")

    graph = UndirectedGraph(args.nodes)

    if args.hamilton:
        graph.generate_hamiltonian_cycle()
        graph.fill_to_saturation(args.saturation)
        graph.add_short_cycles_for_even_degrees()
    elif args.non_hamilton:
        graph.generate_hamiltonian_cycle()
        graph.fill_to_saturation(args.saturation)
        graph.isolate_node()
    else:
        raise ValueError("Specify either --hamilton or --non-hamilton")

    graph.display_adjacency_list()
    print()
    find_euler_cycle(graph)
    print()
    find_hamilton_cycle(graph)
