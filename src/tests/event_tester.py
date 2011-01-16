class EventTester():
    def __init__(self):
        self.lastEvent = None
    
    def notify(self, event):
        self.lastEvent = event
        
    def check_last_event(self):
        """The tester should return the last event posted"""
        result = self.lastEvent
        #self.lastEvent = None
        return result