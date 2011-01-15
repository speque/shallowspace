from utils import debug
from event import TickEvent

class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        self.listenerGroups = {"default":ListenerGroup()}

    def register_listener(self, listener, groups=[]):
        if len(groups) == 0:
            groups = ["default"]
        for groupName in groups:
            if groupName in self.listenerGroups:     
                self.listenerGroups[groupName].add_listener(listener)
            else:
                self.listenerGroups[groupName] = ListenerGroup()
                self.listenerGroups[groupName].add_listener(listener)

    def unregister_listener(self, listener):
        for group in self.listenerGroups:
            if listener in self.listenerGroups[group].listeners:
                del self.listenerGroups[group].listeners[listener]
            
    def post(self, event, groups=[]):
        if not isinstance(event, TickEvent):
            debug( "     Message: " + event.name )
            
        for groupName in groups:
            listenerGroup = self.listenerGroups[groupName].listeners
            for listener in listenerGroup:
                #NOTE: If the weakref has died, it will be automatically removed, so we don't have 
                #to worry about it.
                listener.notify(event)
        for listener in self.listenerGroups["default"].listeners:
            listener.notify(event)

class ListenerGroup:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        
    def add_listener(self, listener):
        self.listeners[listener] = 1
        