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

    #----------------------------------------------------------------------
    def move(self, direction):
        if self.sector.move_possible( direction ):
            newSector = self.sector.neighbors[direction]
            self.sector = newSector
            ev = CharactorMoveEvent(self)
            self.evManager.post( ev )

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
        if isinstance( event, GameStartedEvent ):
            gameMap = event.game.map
            self.place( gameMap.sectors[gameMap.startSectorIndex] )
        
        elif isinstance(event, CharactorMoveRequest):
            if self.direction != event.direction:
                # turn instead of move
                self.turn(event.direction)
            else:
                # the charactor already faces that direction, let's move there
                self.move(event.direction)
                
        elif isinstance(event, CharactorShootRequest):
                self.shoot()
