class EventTester():
    def __init__(self):
        self.events = []
    
    def notify(self, event):
        self.events.append(event)
        
    def last_n_events(self, n):
        return self.events[:n]
    
    def last_event(self):
        return self.events[len(self.events)-1] #TODO better syntax??