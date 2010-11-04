'''
Created on Oct 31, 2010

@author: pekka
'''

from event import CharactorMoveEvent, CharactorPlaceEvent, GameStartedEvent, CharactorMoveRequest
#------------------------------------------------------------------------------
class Charactor:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )
        self.sector = None

    #----------------------------------------------------------------------
    def Move(self, direction):
        if self.sector.MovePossible( direction ):
            newSector = self.sector.neighbors[direction]
            self.sector = newSector
            ev = CharactorMoveEvent( self )
            self.evManager.Post( ev )

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

        elif isinstance( event, CharactorMoveRequest ):
            self.Move( event.direction )