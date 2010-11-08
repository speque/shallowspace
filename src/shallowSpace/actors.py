'''
Created on Oct 31, 2010

@author: pekka
'''

from event import *
import constants
#------------------------------------------------------------------------------
class Charactor:
    """Class representing a paleyer controlled charactor 
    (misspelled to avoid confusion with characters)  """
    
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
        self.sector = None
        self.direction = constants.DIRECTION_DOWN

    #----------------------------------------------------------------------
    def Move(self, direction):
        if self.sector.MovePossible( direction ):
            newSector = self.sector.neighbors[direction]
            self.sector = newSector
            ev = CharactorMoveEvent( self )
            self.evManager.Post( ev )

    #----------------------------------------------------------------------
    def Turn(self, direction):
        self.direction = direction
        ev = CharactorTurnEvent(self)
        self.evManager.Post(ev)

    #----------------------------------------------------------------------
    def Shoot(self):
        ev = CharactorShootEvent(self)
        self.evManager.Post(ev)
        
    #----------------------------------------------------------------------
    def Place(self, sector):
        self.sector = sector
        ev = CharactorPlaceEvent( self )
        self.evManager.Post( ev )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, GameStartedEvent ):
            gameMap = event.game.map
            self.Place( gameMap.sectors[gameMap.startSectorIndex] )
        
        elif isinstance(event, CharactorMoveRequest):
            if self.direction != event.direction:
                # turn instead of move
                self.Turn(event.direction)
            else:
                # the charactor already faces that direction, let's move there
                self.Move(event.direction)
                
        elif isinstance(event, CharactorShootRequest):
                self.Shoot()