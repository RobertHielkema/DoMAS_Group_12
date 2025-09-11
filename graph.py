import random
from neighbourhood import Neighourhood
from person import Person
# import numpy as np


class Graph:
        
    def __init__(self, number_neighbourhoods=1, number_residents=10):
        self.edges = None
        self.neigbourhoods = [Neighourhood(i+1, number_residents) for i in range(number_neighbourhoods)]
        self.nodes = [x for n in self.neigbourhoods for x in n.residents]


    def make_ring_lattice(self, k):
        """
            given list of nodes make ring lattice with k neighbors

            params: k: int, number of neighbors each node should have
            returns: adjacency dictionary {node: set(neighbors)}
        
        """
     
        if k % 2 != 0:
            raise ValueError("k must be an even number for a symmetric ring lattice.")

        nodes = self.nodes
        n = len(nodes)
        adjacency = {node: set() for node in nodes}

        for i, node in enumerate(nodes):
            for j in range(1, k // 2 + 1):
                # Connect to neighbors in the "forward" direction
                neighbor_forward = nodes[(i + j) % n]
                adjacency[node].add(neighbor_forward)
                # Connect to neighbors in the "backward" direction
                neighbor_backward = nodes[(i - j) % n]
                adjacency[node].add(neighbor_backward)
        self.edges = adjacency
        return adjacency
    
    def rewire_edges(self, p):
        """
            Given an adjacency dictionary, rewire edges with probability p.
            params: adjacency: dict, adjacency dictionary {node: set(neighbors)}
                    p: float, probability of rewiring each edge
            returns: new adjacency dictionary {node: set(neighbors)}
        """
        
        adjacency = self.edges
        nodes = list(adjacency.keys())

        for node in nodes:
            neighbors = list(adjacency[node])
            for neighbor in neighbors:
                if random.random() < p:
                    # Remove the edge
                    adjacency[node].remove(neighbor)

                    # Add a new edge to a random node that is not the current node or its current neighbors
                    potential_new_neighbors = set(nodes) - {node} - adjacency[node]
                    if potential_new_neighbors:
                        new_neighbor = random.choice(list(potential_new_neighbors))
                        adjacency[node].add(new_neighbor)

        self.edges = adjacency
        return adjacency
        
    def print_edges(self):
        for node, neighbors in self.edges.items():
            print(f"{node.name}: {', '.join(str(neighbor.name) for neighbor in neighbors)}")