import random
import math

class Person:
    def __init__(self, name):
        self.name = name
        self.infection_status = 'Susceptible'
        self.days_exposed = 0
        self.days_infected = 0
        self.quarantined = False
        self.careless = False
    

    def timestep(self):
        if self.infection_status == 'Susceptible':  # nothing happens if healthy
            pass
        elif self.infection_status == 'Exposed':    # after 6 days of being infected, become sick
            self.days_exposed += 1
            p = math.exp(2 * (self.days_exposed - 3.2))   # exponential growth, ~100% by day 4 as per paper
            if random.random() < p:
                self.infection_status = 'Infected'
                self.days_exposed = 0
        elif self.infection_status == 'Infected':   # after 6 days of being sick, become healthy
            self.days_infected += 1
            p = math.exp(2 * (self.days_infected - 3.2))       # same exponential form
            if random.random() < p:
                self.infection_status = 'Removed'
                self.days_infected = 0


    def infect(self):
        """
            Determines whether a susceptible individual becomes exposed (infected but not yet infectious)
            after contact with an infected individual. The infection does not occur deterministically; 
            instead, it happens with a fixed probability (e.g., 3% for normal individuals or 15% for 
            careless individuals). This reflects the chance-based nature of transmission in the model.
        """
        if self.infection_status == 'Susceptible':
            infection_chance = 0.15 if self.careless else 0.03
            if random.random() < infection_chance:
                self.infection_status = 'Exposed'
                self.days_exposed = 0
                print(f"{self.name} has been exposed!")