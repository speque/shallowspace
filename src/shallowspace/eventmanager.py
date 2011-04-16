from utils import debug
from event import TickEvent

class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        self.listener_groups = {"default":ListenerGroup()}

    def register_listener(self, listener, *args):
        if len(args) == 0:
            args = ["default"]
        for group_name in args:
            if group_name in self.listener_groups:     
                self.listener_groups[group_name].add_listener(listener)
            else:
                self.listener_groups[group_name] = ListenerGroup()
                self.listener_groups[group_name].add_listener(listener)

    def unregister_listener(self, listener):
        for group in self.listener_groups:
            if listener in self.listener_groups[group].listeners:
                del self.listener_groups[group].listeners[listener]
            
    def post(self, event, *args):
        if not isinstance(event, TickEvent):
            debug( "     Message: " + event.name )
            
        for group_name in args:
            listener_group = self.listener_groups[group_name].listeners
            for listener in listener_group:
                #NOTE: If the weakref has died, it will be automatically removed, so we don't have 
                #to worry about it.
                listener.notify(event)
        for listener in self.listener_groups["default"].listeners:
            listener.notify(event)

class ListenerGroup:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        
    def add_listener(self, listener):
        self.listeners[listener] = 1
        