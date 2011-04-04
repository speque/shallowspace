'''
Created on Oct 31, 2010

@author: pekka
'''
from event import CharactorMoveEvent, CharactorTurnEvent, CharactorShootEvent, CharactorPlaceEvent
import constants
#------------------------------------------------------------------------------
class Charactor:
    """Class representing a player controlled charactor 
    (misspelled to avoid confusion with textual characters)  """
    
    def __init__(self, event_manager, char_id=0):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.charactor_id = char_id
        self.sector = None
        self.direction = constants.DIRECTION_DOWN
        self.radius = 2

    #----------------------------------------------------------------------
    def move(self, direction):
        if self.sector.move_possible( direction ):
            self.sector = self.sector.neighbors[direction]
            new_event = CharactorMoveEvent(self)
            self.event_manager.post(new_event)
            
    #----------------------------------------------------------------------
    def turn(self, direction):
        self.direction = direction
        new_event = CharactorTurnEvent(self)
        self.event_manager.post(new_event)

    #----------------------------------------------------------------------
    def shoot(self):
        new_event = CharactorShootEvent(self)
        self.event_manager.post(new_event)
        
    #----------------------------------------------------------------------
    def place(self, sector):
        self.sector = sector
        new_event = CharactorPlaceEvent(self)
        self.event_manager.post( new_event )
        
    #----------------------------------------------------------------------
    def notify(self, event):        
        pass