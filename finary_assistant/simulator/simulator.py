class Simulator:
    def __init__(self, events=None):
        self.events = [] if events is None else events
    
    def simulate(self, portfolio):
        return 'Simulation'