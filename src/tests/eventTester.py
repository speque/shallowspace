class EventTester:
    def __init__(self):
        self.lastEvent = None
    
    def Notify(self, ev):
        self.lastEvent = ev
        
    def checkLastEvent(self):
        result = self.lastEvent
        self.lastEvent = None
        return result 
