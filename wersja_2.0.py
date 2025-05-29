import argparse
from generowanie_grafu import Graph
import generowanie_grafu
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hamilton', action='store_true')
    parser.add_argument('--non-hamilton', action='store_true')
    args = parser.parse_args()

    if args.hamilton:
        nodes = int(input("nodes > "))
        saturation = float(input("saturation (30 or 70) > "))
        while nodes<10 or (saturation!=30 and saturation !=70):
            print("Wieszchołków musi być większa od 10, a saturation musi być równa 30 lub 70:")
            nodes = int(input("nodes > "))
            saturation = float(input("saturation (30 or 70) > "))
        graph = Graph(nodes)
        generowanie_grafu.generowanie(nodes, saturation/100,"hamil")


    elif args.non_hamilton:
        nodes = int(input("nodes > "))
        while nodes<10:
            print("Wieszchołków muszi być większa od 10:")
            nodes = int(input("nodes > "))
        graph = Graph(nodes)
        generowanie_grafu.generowanie(nodes, 50, "non-hamil")

    else:
        print("Podaj --hamilton lub --non-hamilton")
        return

    print("\nOperacje na grafach:")
    print("  Print")
    print("  Euler - Znajdowania cyklu Eulera w grafie")
    print("  Hamilton - Algorytm z powracaniem znajdowania cyklu Hamiltona w grafie")
    print("  Exit")

    while True:
        try:
            action = input("action> ").strip().lower()
            match action:
                case "print":
                    rep = input("representation: matrix/list/table > ").strip().lower()
                    match rep:
                        case "matrix":
                            print("macież")
                        case "list":
                            print("lista następników")
                        case "table":
                            print("lista krawędzi")
                        case _:
                            print("Oj, takiego typu tutaj nie mamy")

                case "euler":
                    graph.find_euler_cycle()
                case "hamilton":
                    graph.find_hamilton_cycle()
                case "exit":
                    break
                case _:
                    print("Nie ma takiej opcji!")
        except ValueError:
            print("Nie takie dane")
        except Exception as e:
            print(f"Błąd: {e}")
if __name__ == '__main__':
    main()