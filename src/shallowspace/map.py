'''
Created on Oct 31, 2010

@author: pekka

'''
from event import MapBuiltEvent, SectorsLitRequest, CharactorMoveEvent, DimAllSectorsRequest, CharactorPlaceEvent
import constants
import math
from utils import *
#------------------------------------------------------------------------------
class Map:
    """..."""

    STATE_PREPARING = 0
    STATE_BUILT = 1

    #----------------------------------------------------------------------
    def __init__(self, evManager, wallsUp, wallsRight, wallsLeft, wallsDown):
        self.evManager = evManager
        self.evManager.register_listener( self )

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
            self.sectors[i] = Sector()

        for i in range(100):
            if i > 9: #not first row
                self.sectors[i].neighbors[constants.DIRECTION_UP] = self.sectors[i-10]
                
                upleft = i-11 
                if upleft > -1 and not (upleft+1) % 10 == 0:
                    self.sectors[i].corners[constants.DIRECTION_UP_LEFT] = self.sectors[upleft]
                upright = i-9
                if not (upright) % 10 == 0:
                    self.sectors[i].corners[constants.DIRECTION_UP_RIGHT] = self.sectors[upright]
            
            if i == 0 or not (i+1) % 10 == 0: #not rightmost column
                self.sectors[i].neighbors[constants.DIRECTION_RIGHT] = self.sectors[i+1]
            
            if i < 90: #not last row
                self.sectors[i].neighbors[constants.DIRECTION_DOWN] = self.sectors[i+10]
                
                downleft = i+9 
                if not (downleft+1) % 10 == 0 :
                    self.sectors[i].corners[constants.DIRECTION_DOWN_LEFT] = self.sectors[downleft]
                downright = i+11
                if downright < 100 and not (downright) % 10 == 0:
                    self.sectors[i].corners[constants.DIRECTION_DOWN_RIGHT] = self.sectors[downright]
            
            if not i % 10 == 0: #not leftmost column
                self.sectors[i].neighbors[constants.DIRECTION_LEFT] = self.sectors[i-1]
        
        for i in self.wallsUp:
            self.sectors[i].neighbors[constants.DIRECTION_UP] = None
            
        for i in self.wallsRight:
            self.sectors[i].neighbors[constants.DIRECTION_RIGHT] = None
            
        for i in self.wallsDown:
            self.sectors[i].neighbors[constants.DIRECTION_DOWN] = None
            
        for i in self.wallsLeft:
            self.sectors[i].neighbors[constants.DIRECTION_LEFT] = None
            
        for s in self.sectors:
            for c in s.corners:
                if not self._is_open_corner_of(c, s):
                    s.corners[s.corners.index(c)] = None

        self.state = Map.STATE_BUILT

        ev = MapBuiltEvent( self )
        self.evManager.post( ev )
    
    def _is_open_corner_of(self, corner, sector):
        for n in sector.neighbors:
            if not n == None and corner in n.neighbors:
                return True
        return False


    def fov(self, charactor):
        i = 0
        litSectors = set()
        litSectors.add(charactor.sector)
        while i < 360:            
            dx = math.cos(i*0.01745)
            dy = math.sin(i*0.01745)
            litSectors = litSectors.union(self.determine_fov(charactor.sector, charactor.radius, dx, dy))
            i += 3
        ev = DimAllSectorsRequest()
        self.evManager.post(ev)
        ev = SectorsLitRequest(litSectors)
        self.evManager.post(ev)

    #----------------------------------------------------------------------
    def determine_fov(self, sector, radius, dx, dy):
        i = 0
        ox = self.sector_x(sector)+0.5
        oy = self.sector_y(sector)+0.5
        litSectors = []
        while i < radius:
            oldSector = self.sector_by_coordinates((ox), (oy))
            ox += dx;
            oy += dy;
            newSector = self.sector_by_coordinates((ox), (oy))
            if not newSector == None:
                if not newSector == oldSector and (newSector in oldSector.neighbors or newSector in oldSector.corners):  
                    litSectors.append(newSector)
                else:
                    return litSectors
            i += 1
        return litSectors
    
    def sector_x(self, sector):
        return self.sectors.index(sector) % 10
    
    def sector_y(self, sector):
        return self.sectors.index(sector)/10
    
    def sector_by_coordinates(self, x, y):
        if x >= 0 and x < 10 and y >= 0 and y < 10:
            index = int(math.floor(y)*10.0+math.floor(x))
            if index > -1:
                return self.sectors[index]
    
    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, CharactorMoveEvent) or isinstance(event, CharactorPlaceEvent):
            self.fov(event.charactor)
            
#------------------------------------------------------------------------------
class Sector:
    """..."""
    def __init__(self):
        self.neighbors = range(4)
        self.corners = range(4)

        self.neighbors[constants.DIRECTION_UP] = None
        self.neighbors[constants.DIRECTION_DOWN] = None
        self.neighbors[constants.DIRECTION_LEFT] = None
        self.neighbors[constants.DIRECTION_RIGHT] = None
        
        self.corners[constants.DIRECTION_UP_RIGHT] = None
        self.corners[constants.DIRECTION_DOWN_RIGHT] = None
        self.corners[constants.DIRECTION_DOWN_LEFT] = None
        self.corners[constants.DIRECTION_UP_LEFT] = None

    #----------------------------------------------------------------------
    def move_possible(self, direction):
        if self.neighbors[direction]:
            return 1
        else:
            return 0
