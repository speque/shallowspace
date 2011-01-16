class EventTester():
    def __init__(self):
        self.lastEvent = None
    
    def notify(self, event):
        self.lastEvent = event
        
    def check_last_event(self):
        return self.lastEvent