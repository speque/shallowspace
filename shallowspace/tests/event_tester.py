class EventTester():
    def __init__(self):
        self.events = []
    
    def notify(self, event):
        self.events.append(event)
        
    def last_n_events(self, n):
        return self.events[:n]
    
    def last_event(self):
        if not len(self.events) == 0:
            return self.events[-1]
        else:
            return None
    
    def clear(self):
        self.events = []