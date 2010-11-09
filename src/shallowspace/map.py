'''
Created on Oct 31, 2010

@author: pekka

'''
from event import MapBuiltEvent
import constants
#------------------------------------------------------------------------------
class Map:
    """..."""

    STATE_PREPARING = 0
    STATE_BUILT = 1

    #----------------------------------------------------------------------
    def __init__(self, evManager, wallsUp, wallsRight, wallsLeft, wallsDown):
        self.evManager = evManager
        #self.evManager.RegisterListener( self )

        self.state = Map.STATE_PREPARING

        self.sectors = range(100)
        self.startSectorIndex = 0
        
        self.wallsUp = wallsUp
        self.wallsRight = wallsRight
        self.wallsLeft = wallsLeft
        self.wallsDown = wallsDown

    #----------------------------------------------------------------------
    def build(self):
        for i in range(100):
            self.sectors[i] = Sector( self.evManager )

        for i in range(100):
            if i > 9:
                self.sectors[i].neighbors[constants.DIRECTION_UP] = self.sectors[i-10]
            if i == 0 or not (i+1) % 10 == 0:
                self.sectors[i].neighbors[constants.DIRECTION_RIGHT] = self.sectors[i+1]
            if i < 90:
                self.sectors[i].neighbors[constants.DIRECTION_DOWN] = self.sectors[i+10]
            if not i % 10 == 0:
                self.sectors[i].neighbors[constants.DIRECTION_LEFT] = self.sectors[i-1]
        
        for i in self.wallsUp:
            self.sectors[i].neighbors[constants.DIRECTION_UP] = None
            
        for i in self.wallsRight:
            self.sectors[i].neighbors[constants.DIRECTION_RIGHT] = None
            
        for i in self.wallsDown:
            self.sectors[i].neighbors[constants.DIRECTION_DOWN] = None
            
        for i in self.wallsLeft:
            self.sectors[i].neighbors[constants.DIRECTION_LEFT] = None

        self.state = Map.STATE_BUILT

        ev = MapBuiltEvent( self )
        self.evManager.post( ev )

#------------------------------------------------------------------------------
class Sector:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        #self.evManager.RegisterListener( self )

        self.neighbors = range(4)

        self.neighbors[constants.DIRECTION_UP] = None
        self.neighbors[constants.DIRECTION_DOWN] = None
        self.neighbors[constants.DIRECTION_LEFT] = None
        self.neighbors[constants.DIRECTION_RIGHT] = None

    #----------------------------------------------------------------------
    def MovePossible(self, direction):
        if self.neighbors[direction]:
            return 1
        else:
            return 0
