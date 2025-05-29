import argparse
import generowanie_grafu
def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Proszę wprowadzić liczbę całkowitą!")
def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--hamilton', action='store_true', help='Generuj graf Hamiltonowski')
    group.add_argument('--non-hamilton', action='store_true', help='Generuj graf nie-Hamiltonowski')
    args = parser.parse_args()

    if args.hamilton:
        nodes = get_integer_input("Liczba wierzchołków > ")
        saturation = get_integer_input("Nasycenie (30 lub 70)> ")
        while nodes < 10 or saturation not in (30, 70):
            print("Liczba wierzchołków musi być większa niż 10, a nasycenie musi wynosić 30 lub 70.")
            nodes = get_integer_input("Liczba wierzchołków > ")
            saturation = get_integer_input("Nasycenie (30 lub 70)> ")

        graph = generowanie_grafu.generowanie(nodes, saturation/100, "hamil")

    elif args.non_hamilton:
        nodes = get_integer_input("Liczba wierzchołków > ")
        while nodes < 10:
            print("Wierzchołków musi być większa od 10:")
            nodes = get_integer_input("Liczba wierzchołków > ")
        graph = generowanie_grafu.generowanie(nodes, 0.5, "non-hamil")

    print("\nDostępne operacje na grafie:")
    print("  print      - Wypisz reprezentację grafu")
    print("  euler      - Znajdź cykl Eulera")
    print("  hamilton   - Znajdź cykl Hamiltona")
    print("  export     - Eksportuj do TikZ")
    print("  exit       - Zakończ program")

    while True:
        try:
            action = input("action> ").strip().lower()
            match action:
                case "print":
                    rep = input("Reprezentacja (macierz_sasiedz / macierz_incy / list_krawe / lista_sasiedz) > ").strip().lower()
                    match rep:
                        case "macierz_sasiedz":
                            print(graph.get_adjacency_matrix())
                        case "macierz_incy":
                            print(graph.get_incidence_matrix())
                        case "list_krawe":
                            print(graph.get_edge_list())
                        case "lista_sasiedz":
                            print(graph.get_adjacency_list())
                        case _:
                            print("Nieznany typ reprezentacji.")

                case "euler":
                    graph.find_euler_cycle()

                case "hamilton":
                    graph.find_hamilton_cycle()

                case "export":
                    graph.export_to_tikz()

                case "exit":
                    break

                case _:
                    print("Nieznana akcja!")

        except ValueError:
            print("Nieprawidłowe dane.")
        except Exception as e:
            print(f"Błąd: {e}")

if __name__ == '__main__':
    main()