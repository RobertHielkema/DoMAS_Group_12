from person import Person
from neighbourhood import Neighourhood
from graph import Graph
import random

if __name__ == "__main__":

    graph = Graph(number_neighbourhoods=3, number_residents=10)

    graph.make_ring_lattice(4)
    graph.print_edges()
    
    # make small world model
    graph.rewire_edges(0.5)
    print("\nAfter rewiring:\n")
    graph.print_edges()

    for i in range(1):
        print(f"\nTimestep {i+1}\n")
        graph.timestep()




    