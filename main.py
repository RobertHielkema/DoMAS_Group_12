from person import Person
from neighbourhood import Neighourhood
from graph import Graph
import random

if __name__ == "__main__":

    # neigbourhood1 = Neighourhood(1)
    # neigbourhood1.add_residents(10)

    graph = Graph(number_neighbourhoods=2, number_residents=10)
    print(len(graph.nodes))

    graph.make_ring_lattice(4)
    graph.print_edges()
    print("\nAfter rewiring:\n")
    
    # make small world model
    # graph.rewire_edges(0.5)
    # graph.print_edges()


    # for i in range(100):
    #     print(f"\nTimestep {i+1}\n")
    #     for connection in graph.edges.items():
    #         print(f"{connection[0].name}: {', '.join(str(neighbor.name) for neighbor in connection[1])}")
    #         interaction = random.choice(list(connection[1]))
    #         print(f"Interaction between {connection[0].name} and {interaction.name}")




    