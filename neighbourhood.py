from person import Person
from typing import List, Dict
import random

class Neighourhood:
    def __init__(self, name):
        self.name = name
        self.residents = [Person]
        self.contacts = {Person: List[Person]}  # Dictionary mapping each person to a list of their contacts


    def add_residents(self, n):
        for i in range(n):
            self.residents.append(Person(f"Person {i+1} in {self.name}"))
        self.create_contacts()
    

    def create_contacts(self):
        # implementation to be added
        pass


    def timestep(self):
        """ Each resident has contact with at least one other resident, if
        they are not quarantined. And each resident updates their infection status.
        """
        for person in self.residents:
            if not person.quarantined:
                # Each person has contact with at least one other resident
                contacts = self.contacts.get(person, [])
                if contacts:
                    contact = contacts[random.randint(0, len(contacts)-1)]
                    # If one is infected and the other is healthy, the healthy one has a chance to get infected
                    if (person.infection_status == 'infected'):
                        contact.infect()
                    elif (contact.infection_status == 'infected'):
                        person.infect()
            person.timestep()