import random
from neighbourhood import Neighourhood
from person import Person
import numpy as np
from colorama import init, Fore, Back, Style

init(autoreset=True)  # colors reset after each print


class Graph:
        
    def __init__(self, number_neighbourhoods=1, number_residents=10):
        self.A = None
        self.neigbourhoods = [Neighourhood(i, number_residents) for i in range(number_neighbourhoods)]
        self.nodes = [x for n in self.neigbourhoods for x in n.residents]
        self.number_neighbourhoods = number_neighbourhoods
        self.number_residents = number_residents


    def make_ring_lattice(self, k: int) -> None:
        """
            given list of nodes make ring lattice with k neighbors

            params: k: int, number of neighbors each node should have
            returns: adjacency matrix np.array of shape (n, n) where n is number of nodes
        
        """
     
        if k % 2 != 0:
            raise ValueError("k must be an even number for a symmetric ring lattice.")

        n = len(self.nodes)
        A = np.zeros((n, n), dtype=int) # Adjacency matrix initialized to 0
        for i in range(n):
            block_start = (i // self.number_residents) * self.number_residents
            for j in range(1, k//2 + 1):
                A[i][(i + j) % self.number_residents + block_start] = 1  # Connect to the next j nodes
                A[i][(i - j) % self.number_residents + block_start] = 1  # Connect to the previous j nodes
        self.A = A

    def rewire_edges(self, p) -> None:
        """
            Given an adjacency matrix, rewire edges with probability p.
            params: p: float, probability of rewiring each edge
            TODO: CHECK FUNCTION FOR ERRORS
        """
        
        A = self.A
        n = len(A)
        for i in range(n):
            block_start = (i // self.number_residents) * self.number_residents
            for j in range(i+1, n):  # Ensure each edge is considered only once
                if A[i][j] == 1 and random.random() < p:
                    
                    # Remove the edge
                    A[i][j] = 0
                    A[j][i] = 0
                    
                    # Find a new node to connect to
                    new_node = random.randint(block_start, block_start + self.number_residents - 1)
                    while new_node == i or A[i][new_node] == 1:
                        new_node = random.randint(block_start, block_start + self.number_residents - 1)
                    print(f'rewire edge between {i} and {j} to {new_node}')
                    # Add the new edge
                    A[i][new_node] = 1
                    A[new_node][i] = 1
        self.A = A 

        
    def print_edges(self) -> None:
        """
            Print the adjacency matrix with colored edges.
        """
        n = len(self.A)
        for i in range(n):
            for j in range(0, n):
                if self.A[i][j] == 1:
                    print(f"{Fore.GREEN}{self.A[i][j]} ", end='')
                else:
                    print(f"{self.A[i][j]} ", end='')
            print()  # New line after each row

    def timestep(self) -> None:
        """
            Each resident interacts with one of their contacts, if they have any.
            During the interaction the infection can possbily spread.
        """
        A = self.A  
        n = len(A)
        # loop through each person and have them interact with one of their contacts
        for i in range(n):

            # get indices of possible contacts for person i
            idx = np.flatnonzero(A[i])

            if idx.size == 0:
                # no contacts for this person, go to next person
                continue


            # get index of a random contact
            interaction = random.choice(idx)

            # =======================================================
            # TODO: Put interaction logic here ↓↓↓ ;
            
            person1 = self._get_person(i)
            person2 = self._get_person(interaction)

            print(f"Interaction between {person1.name} and {person2.name}")
            # =======================================================


    def make_neighbourhood_contacts(self, percentage: int) -> None:
        """
            Create contacts for each neighbourhood based on the adjacency matrix.
            Each person in a neighbourhood will have contacts with people in the same neighbourhood
            as well as people in connected neighbourhoods.
            params: percentage: int, percentage of residents in connected neighbourhoods to be added as contacts
        """

        n = len(self.nodes)

        # Get indices of residents to add contacts for
        indices = random.sample(range(n), int(n * (percentage / 100)))

        for i in indices:
            
            # Get the neighbourhood of the person
            neighbourhood_index = i // self.number_residents
            
            # Find possible contacts in other neighbourhoods
            possible_contacts = [x for x in range(n) if self.A[i][x] == 0 and (x // self.number_residents) != neighbourhood_index]
            new_contact = random.choice(possible_contacts)

            # Add new egdes to adjacency matrix
            self.A[i][new_contact] = 1
            self.A[new_contact][i] = 1

    def delete_neighbourhood_contacts(self) -> None:
        """
            Remove all contacts between different neighbourhoods.
        """
        n = len(self.nodes)
        for i in range(n):
            neighbourhood_index = i // self.number_residents
            for j in range(n):
                if (j // self.number_residents) != neighbourhood_index:
                    self.A[i][j] = 0
                    self.A[j][i] = 0

    def _get_person(self, n: int) -> Person:
        """
            Given a node index, return the corresponding Person object.
            params: n: int, index of the node
            returns: Person object
        """
        return self.nodes[n]

