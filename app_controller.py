import random

class App_controller:
    def __init__(self, graph):
        self.contacts = {}  # Dictionary mapping each person with the app to their contact history
        self.graph = graph
    

    def set_app_users(self, app_users: dict):
        self.contacts = app_users


    def update_app(self, person1, contact, cur_timestep, history_length: int = 4) -> None:
        """
            Update the app history with a new contact for a person.
            params: person1: Person, the person whose app history is to be updated
                    contact: Person, the new contact to add to the app history
        """
        # this person does not have the app so do nothing
        if person1 not in self.contacts:
            return
        
        # the contact does not have the app so do nothing
        if contact not in self.contacts:
            return
        
        # add new contact with current timestep
        self.contacts[person1].append((contact, cur_timestep))

        # remove old contacts beyond the history length
        while self.contacts[person1] and (cur_timestep - self.contacts[person1][0][1]) > history_length:
            self.contacts[person1].pop(0)  # remove oldest contact if it's older than desired history_length


    def trigger_quarantine(self, person) -> None:
        """
            Trigger quarantine notification for a person's recent contacts using the app.
            params: person: Person, the person who is Removed and whose contacts need to be notified
        """
        if person not in self.contacts:
            return  # Person does not have the app, cannot trace contacts

        # Get recent contacts from the app history
        recent_contacts = [contact for contact, timestep in self.contacts[person]]

        # TODO Decide on quarantine probability and implement it here
        # maybe use a parameter for this
        for contact in recent_contacts:
            if random.random() < 0.5:   
                self.graph.quarantine_person(contact)