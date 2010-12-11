'''
Created on Oct 31, 2010

@author: pekka
'''

from event import *
import constants
#------------------------------------------------------------------------------
class Charactor:
    """Class representing a player controlled charactor 
    (misspelled to avoid confusion with textual characters)  """
    
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)
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
        if isinstance(event, GameStartedEvent):
            gameMap = event.game.map
            self.place(gameMap.sectors[gameMap.startSectorIndex])
        
        elif isinstance(event, CharactorMoveRequest):
            if self.direction != event.direction and not event.force:
                # turn instead of move
                self.turn(event.direction)
            else:
                # the charactor already faces that direction, let's move there
                self.move(event.direction)
                
        elif isinstance(event, CharactorTurnAndMoveRequest):
            if self.direction != event.direction:
                self.turn(event.direction)
            self.move(event.direction)
                
        elif isinstance(event, CharactorMoveToRequest):
            ev = CalculatePathRequest(self.sector, event.pos)
            self.evManager.post(ev)
                
        elif isinstance(event, CharactorShootRequest):
                self.shoot()
