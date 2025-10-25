import random
from neighbourhood import Neighourhood
from person import Person
import numpy as np
from colorama import init, Fore, Back, Style
import copy
from app_controller import App_controller
from plot import plot_data, plot_quarantained_bar
import networkx as nx
import configparser

init(autoreset=True)  # colors reset after each print


class Graph:
        
    def __init__(self, number_neighbourhoods: int, 
                 number_residents: int, num_connections: int, 
                 careless_prob: float, rewire_prob: float,
                 include_quarantining: bool,
                 app_usage_rate: float = 1.0,
                 quarantine_probability: float = 0.5,
                 include_self_test: bool = True):
        """
            Initialize the graph with a given number of neighbourhoods and residents per neighbourhood.
            Each neighbourhood is represented as a Neighourhood object containing Person objects.
            params: number_neighbourhoods: int, number of neighbourhoods in the graph
                    number_residents: int, number of residents per neighbourhood
                    num_connections: int, number of connections each node should have in the ring lattice
                    careless_prob: float, probability of a person being careless
                    rewire_prob: float, probability of rewiring each edge in the small-world model
                    include_quarantining: bool, whether to include quarantining in the simulation
                    app_usage_rate: float, percentage of non-careless population to use the app
                    quarantine_probability: float, probability that a contact will quarantine when notified
        """
        self.app = App_controller(self, quarantine_probability)
        self.neigbourhoods = [Neighourhood(i, number_residents, self.app) for i in range(number_neighbourhoods)]
        self.nodes = [x for n in self.neigbourhoods for x in n.residents]
        self.number_neighbourhoods = number_neighbourhoods
        self.number_residents = number_residents
        self.include_quarantining = include_quarantining
        self.include_self_test = include_self_test


        self._make_careless(p=careless_prob)

        if self.include_quarantining:
            self.app_users = self._get_app_users(rate=app_usage_rate)
            self.app.set_app_users(self.app_users)
        else:
            self.app.set_app_users({})  # No one has the app if quarantining is not included

        self.history_E = []
        self.history_I = []
        self.history_S = []
        self.history_R = []

        self.history_quarantined = []

        # Infect 1% of the population at the start of the simulation
        self.first_infected_index = self._infect_first_people(p=0.01)  

        self.A = self._make_ring_lattice(k=num_connections)

        self._rewire_edges(rewire_prob)
        self.copyA = copy.deepcopy(self.A)

        print(f"Graph initialized with {len(self.nodes)} nodes in {self.number_neighbourhoods} neighbourhoods.")

    def _infect_first_people(self, p=0.0148):  #Prob as described in the paper we copy
        """
            Infect a percentage p of the population at the start of the simulation.
            params: p: float, percentage of population to infect
        """
        total_population = len(self.nodes)
        n_infected = max(1, int(total_population * p))  # Ensure at least one person is infected
        infected_people = random.sample(self.nodes, n_infected)
        infected_index = [self.nodes.index(person) for person in infected_people]
        for person in infected_people:
            person.infection_status = 'Infected'
            #print(f"{person.name} has been initially infected!")
        return infected_index
    
    def _make_careless(self, p=0.05):
        """
            Make a percentage p of the population careless.
            params: p: float, percentage of population to make careless
        """
        total_population = len(self.nodes)
        n_careless = int(total_population * p)
        careless_people = random.sample(self.nodes, n_careless)
        #print(f"Making {n_careless} people careless.")
        for person in careless_people:
            person.careless = True


    def _get_app_users(self, rate: float):
        """
            Set app users based on the given rate.
            params: rate: float, percentage of non-careless population to use the app
        """
        self.potential_app_users = {person: [] for person in self.nodes if not person.careless}
        n_app_users = int(len(self.potential_app_users) * rate)
        app_users = random.sample(list(self.potential_app_users.keys()), n_app_users)
        return {person: [] for person in app_users}


    def _make_ring_lattice(self, k: int) -> np.array:
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
        return A

    def _rewire_edges(self, p) -> None:
        """
            Given an adjacency matrix, rewire edges with probability p.
            params: p: float, probability of rewiring each edge
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
                    #print(f'rewire edge between {i} and {j} to {new_node}')
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


    def timestep(self, i: int) -> None:
        """
            Each resident interacts with one of their contacts, if they have any.
            During the interaction the infection can possbily spread.
            params: i: int, current timestep
        """
        A = self.A  
        n = len(A)
        # loop through each person and have them interact with one of their contacts
        for i in range(n):

            # run timestep for person
            person1 = self._get_person(i)
            person1.timestep()

            # get indices of possible contacts for person i
            idx = np.flatnonzero(A[i])

            if idx.size == 0:
                # no contacts for this person, go to next person
                continue


            # get index of a random contact
            interaction = random.choice(idx)

            # interaction logic
            
            person2 = self._get_person(interaction)

            # update history of both persons
            self.app.update_app(person1, person2, i)
            self.app.update_app(person2, person1, i)

            # print(f"Interaction between {person1.name} and {person2.name}")

            if (person1.infection_status == 'Infected'):
                person2.infect()
            elif (person2.infection_status == 'Infected'):
                person1.infect()

        n_infected, n_exposed, n_removed, n_susceptible = self.count_n_infections()
        self.history_I.append(n_infected)
        self.history_E.append(n_exposed)
        self.history_R.append(n_removed)
        self.history_S.append(n_susceptible)

        #self.print_n_infections(n_infected, n_exposed, n_removed, n_susceptible)


    def quarantine_person(self, person: Person) -> None:
        """
            Quarantine a person by setting their quarantined status to True.
            params: person: Person, the person to quarantine
        """

        def self_test(person: Person) -> bool:
            """
                Returns result of self test with probavility of false positive of false negative.
                returns: bool, True if test is positive, False otherwise
            """

            # 8,16% false negative rate
            if person.infection_status == 'Infected':
                return random.random() > 0.0816
            
            # 0.05% false positive rate
            return random.random() < 0.0005

        if self.include_self_test:
            if self_test(person):
                person.quarantined = True

                # check whether a person is correctly quarantined in history
                if person.infection_status == 'Infected' or person.infection_status == 'Exposed':
                    self.history_quarantined.append(1)
                else:
                    self.history_quarantined.append(0)
        
        else:
            person.quarantined = True
            # check whether a person is correctly quarantined in history
            if person.infection_status == 'Infected' or person.infection_status == 'Exposed':
                self.history_quarantined.append(1)
            else:
                self.history_quarantined.append(0)


    def remove_quarantined(self) -> None:
        """
            Remove all quarantined individuals from the adjancy matrix such that no interaction will be made with those persons.
        """
        # Find indices of quarantined individuals
        quarantined_indices = [i for i, person in enumerate(self.nodes) if person.quarantined]

        if not quarantined_indices:
            return  # No one is quarantined, nothing to do

        # Zero out their rows and columns in the adjacency matrix
        for idx in quarantined_indices:
            self.A[idx, :] = 0  # Zero out the entire row
            self.A[:, idx] = 0  # Zero out the entire column
                
                
    def count_n_infections(self):
        n_infected = sum(1 for person in self.nodes if person.infection_status == 'Infected')
        n_exposed = sum(1 for person in self.nodes if person.infection_status == 'Exposed')
        n_removed = sum(1 for person in self.nodes if person.infection_status == 'Removed')
        n_susceptible = sum(1 for person in self.nodes if person.infection_status == 'Susceptible')
        return n_infected, n_exposed, n_removed, n_susceptible
    

    def print_n_infections(self, n_infected, n_exposed, n_removed, n_susceptible):
        """
            Print the total number of infections.
        """
        n_quarantined = sum(1 for person in self.nodes if person.quarantined)
        print(f"Total Infected: {n_infected}, Exposed: {n_exposed}, Removed: {n_removed}, Susceptible: {n_susceptible}, Quarantined: {n_quarantined}")


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
            possible_contacts = [j for j in range(n) if self.A[i][j] == 0 and not self._is_in_neighbourhood(neighbourhood_index, j)]
            new_contact = random.choice(possible_contacts)

            # Add new egdes to adjacency matrix
            self.A[i][new_contact] = 1
            self.A[new_contact][i] = 1

   
    def delete_neighbourhood_contacts(self) -> None:
        """
            Remove all contacts between different neighbourhoods by resetting the adjacency matrix to its original state.
            This ensures that only intra-neighbourhood contacts remain.
        """
        self.A = copy.deepcopy(self.copyA)
        if self.include_quarantining:
            self.remove_quarantined()


    def _is_in_neighbourhood(self, neighbourhood_index: int, person_index: int) -> bool:
        """
            Check if a person belongs to a given neighbourhood.
            params: neighbourhood_index: int, index of the neighbourhood
                    person_index: int, index of the person
            returns: bool, True if person belongs to neighbourhood, False otherwise
        """
        return (person_index // self.number_residents) == neighbourhood_index

    def _get_person(self, n: int) -> Person:
        """
            Given a node index, return the corresponding Person object.
            params: n: int, index of the node
            returns: Person object
        """
        return self.nodes[n]
    

    def _get_infected_ids(self) -> list[int]:
        return [i for i in range(len(self.nodes)) if self.nodes[i].infection_status == "Infected"]
    

    def _fix_node_positions(self) -> dict:
        pos = {}
        cols = 6 
        space_between_nodes = 30 

        for i in range(self.number_neighbourhoods):
            start = i * self.number_residents
            end = start + self.number_residents
            nodes = list(range(start, end))
            G_neighbourhood = nx.Graph()
            for u in nodes:
                for v in nodes:
                    if self.A[u][v] == 1:
                        G_neighbourhood.add_edge(u, v)
            neighbourhood_pos = nx.spring_layout(G_neighbourhood, seed=i)

            between_x = (i % cols) * space_between_nodes
            between_y = (i // cols) * space_between_nodes
            x_max = 0
            y_max = 0

            for node, (x, y) in neighbourhood_pos.items():
                new_x = x * 10 + between_x
                new_y = y * 10 + between_y
                if new_x > x_max:
                    x_max = new_x
                if new_y > y_max:
                    y_max = new_y
                pos[node] = (new_x, new_y)

        

        return pos, x_max, y_max


    def plot_history(self, history_E, history_I, history_S, history_R):
        days = list(range(1, len(self.history_I) + 1))
        plot_data(days, history_E, history_I, history_S, history_R, len(self.nodes))


    def plot_quarantained(self, quarantined_history):
        plot_quarantained_bar(quarantined_history)