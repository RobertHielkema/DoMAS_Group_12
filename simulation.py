from neighbourhood import Neighourhood
import random

class Simulation:
    def __init__(self, Nneighbourhoods=0, PperN=20):
        self.Nneighbourhoods = Nneighbourhoods
        self.PperN = PperN
        self.neighbourhoods = [Neighourhood]


    def setup(self):
        self.neighbourhoods = [Neighourhood(f"Neighbourhood {i+1}") for i in range(self.Nneighbourhoods)]
        for n in self.neighbourhoods:
            n.add_residents(self.PperN)

    
    def create_random_contacts(self):
        """ Create random contacts between residents in different neighbourhoods.
        1% of the population will have a contact with someone from another neighbourhood each day.
        """
        total_population = self.Nneighbourhoods * self.PperN
        n_cross_contacts = total_population // 100
        for _ in range(n_cross_contacts):
            n1, n2 = random.sample(self.neighbourhoods, 2)
            p1 = random.choice(n1.residents)
            p2 = random.choice(n2.residents)
            # p1 and p2 have contact, should they also have a contact in their own neighbourhoods?