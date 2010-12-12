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
    
    def __init__(self, evManager, id=0):
        self.evManager = evManager
        self.evManager.register_listener(self)
        self.id = id
        self.sector = None
        self.direction = constants.DIRECTION_DOWN
        self.radius = 2

    #----------------------------------------------------------------------
    def move(self, direction):
        if self.sector.move_possible( direction ):
            self.sector = self.sector.neighbors[direction]
            ev = CharactorMoveEvent(self)
            self.evManager.post(ev)
            
    #----------------------------------------------------------------------
    def turn(self, direction):
        self.direction = direction
        ev = CharactorTurnEvent(self)
        self.evManager.post(ev)

    #----------------------------------------------------------------------
    def shoot(self):
        ev = CharactorShootEvent(self)
        self.evManager.post(ev)
        
    #----------------------------------------------------------------------
    def place(self, sector):
        self.sector = sector
        ev = CharactorPlaceEvent(self)
        self.evManager.post( ev )
        
    #----------------------------------------------------------------------
    def notify(self, event):        
        pass