


class Person:
    def __init__(self, name):
        self.name = name
        self.infection_status = 'healthy'
        self.days_infected = 0
        self.days_sick = 0
        self.quarantined = False
    

    def timestep(self):
        if self.infection_status == 'healthy':      # nothing happens if healthy
            pass
        elif self.infection_status == 'infected':   # after 6 days of being infected, become sick
            self.days_infected += 1
            if self.days_infected >= 6:
                self.infection_status = 'sick'
                self.days_infected = 0
        elif self.infection_status == 'sick':       # after 6 days of being sick, become healthy
            self.days_sick += 1
            if self.days_sick >= 6:
                self.infection_status = 'healthy'
                self.days_sick = 0


    def infect(self):       # Should this have a chance to get infected?
        if self.infection_status == 'healthy':
            self.infection_status = 'infected'
            self.days_infected = 0
