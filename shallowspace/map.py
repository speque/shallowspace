'''
Created on Oct 31, 2010

@author: pekka

'''
from event import MapBuiltEvent, SectorsLitRequest, CharactorMoveEvent, CharactorTurnAndMoveRequest, \
DimAllSectorsRequest, CharactorPlaceEvent, CalculatePathRequest, OccupiedSectorAction, \
FreeSectorAction, ActiveCharactorChangeEvent, CharactorPlaceRequest
import constants
import math
from astar import a_star
#------------------------------------------------------------------------------
class Map:
    """..."""

    STATE_PREPARING = 0
    STATE_BUILT = 1

    #----------------------------------------------------------------------
    def __init__(self, event_manager, grid_size_x, grid_size_y, walls_up, walls_right, walls_left, walls_down):
        self.event_manager = event_manager
        self.event_manager.register_listener( self )

        self.state = Map.STATE_PREPARING

        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y

        self.sectors = None
        self.free_start_sector_indices = [0, 1, 2, 3]
        
        self.map_state = MapState(event_manager)
        
        self.walls_up = walls_up
        self.walls_right = walls_right
        self.walls_left = walls_left
        self.walls_down = walls_down

    #----------------------------------------------------------------------
    def build(self):
        self.sectors = [Sector(x) for x in xrange(self.grid_size_x*self.grid_size_y)]
        
        for i, sector in enumerate(self.sectors):
            if i > self.grid_size_x-1: #not first row
                sector.neighbors[constants.DIRECTION_UP] = self.sectors[i-self.grid_size_x]
                
                upleft = i-(self.grid_size_x+1)
                if upleft > -1 and not (upleft+1) % self.grid_size_x == 0:
                    sector.corners[constants.DIRECTION_UP_LEFT] = self.sectors[upleft]
                upright = i-(self.grid_size_x-1)
                if not (upright) % self.grid_size_x == 0:
                    sector.corners[constants.DIRECTION_UP_RIGHT] = self.sectors[upright]
            
            if i == 0 or not (i+1) % self.grid_size_x == 0: #not rightmost column
                sector.neighbors[constants.DIRECTION_RIGHT] = self.sectors[i+1]
            
            if i < self.grid_size_x*(self.grid_size_y-1): #not last row
                sector.neighbors[constants.DIRECTION_DOWN] = self.sectors[i+self.grid_size_x]
                
                downleft = i+(self.grid_size_x-1)
                if not (downleft+1) % self.grid_size_x == 0 :
                    sector.corners[constants.DIRECTION_DOWN_LEFT] = self.sectors[downleft]
                downright = i+self.grid_size_x+1
                if downright < self.grid_size_x*self.grid_size_y and not (downright) % self.grid_size_x == 0:
                    sector.corners[constants.DIRECTION_DOWN_RIGHT] = self.sectors[downright]
            
            if not i % self.grid_size_x == 0: #not leftmost column
                sector.neighbors[constants.DIRECTION_LEFT] = self.sectors[i-1]
        
        for i in self.walls_up:
            self.sectors[i].neighbors[constants.DIRECTION_UP] = None
            
        for i in self.walls_right:
            self.sectors[i].neighbors[constants.DIRECTION_RIGHT] = None
            
        for i in self.walls_down:
            self.sectors[i].neighbors[constants.DIRECTION_DOWN] = None
            
        for i in self.walls_left:
            self.sectors[i].neighbors[constants.DIRECTION_LEFT] = None
            
        for sector in self.sectors:
            for corner in sector.corners:
                if not self._is_open_corner_of(corner, sector):
                    sector.corners[sector.corners.index(corner)] = None

        self.state = Map.STATE_BUILT

        new_event = MapBuiltEvent(self)
        self.event_manager.post(new_event)
    
    def _is_open_corner_of(self, corner, sector):
        for neighbor in sector.neighbors:
            if not neighbor == None and corner in neighbor.neighbors:
                return True
        return False


    def fov(self, charactor):
        angle = 0
        lit_sectors = set()
        lit_sectors.add(charactor.sector)
        while angle < 360:
            delta_x = math.cos(angle*0.01745)
            delta_y = math.sin(angle*0.01745)
            lit_sectors = lit_sectors.union(self.determine_fov(charactor.sector, charactor.radius, delta_x, delta_y))
            angle += 6 #magic number here
        new_event = DimAllSectorsRequest()
        self.event_manager.post(new_event)
        new_event = SectorsLitRequest(lit_sectors)
        self.event_manager.post(new_event)

    #----------------------------------------------------------------------
    def determine_fov(self, sector, radius, delta_x, delta_y):
        i = 0
        original_x = self.sector_x(sector)+0.5
        original_y = self.sector_y(sector)+0.5
        lit_sectors = []
        while i < radius:
            old_sector = self.sector_by_coordinates((original_x), (original_y))
            original_x += delta_x
            original_y += delta_y
            new_sector = self.sector_by_coordinates((original_x), (original_y))
            if not new_sector == None:
                if not new_sector == old_sector and (new_sector in old_sector.neighbors or new_sector in old_sector.corners):  
                    lit_sectors.append(new_sector)
                else:
                    return lit_sectors
            i += 1
        return lit_sectors
    
    def sector_x(self, sector):
        return self.sectors.index(sector) % self.grid_size_x
    
    def sector_y(self, sector):
        return self.sectors.index(sector)/self.grid_size_x
    
    def sector_by_coordinates(self, x_coordinate, y_coordinate): 
        if x_coordinate >= 0 and x_coordinate < self.grid_size_x and y_coordinate >= 0 and y_coordinate < self.grid_size_y:
            index = int(math.floor(y_coordinate)*11.0+math.floor(x_coordinate)) #TODO magic number
            if index > -1:
                return self.sectors[index]
            
    def charactor_by_coordinates(self, x_coordinate, y_coordinate):
        sector = self.sector_by_coordinates(x_coordinate/constants.GRID_SIZE, y_coordinate/constants.GRID_SIZE)
        if sector == None or self.map_state.sector_is_free(sector):
            return None
        else:
            return self.map_state.actors_by_sector_id.get(sector.sector_id, -1)
        
    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance(event, CharactorMoveEvent) or isinstance(event, CharactorPlaceEvent) or isinstance(event, ActiveCharactorChangeEvent):
            self.fov(event.charactor)
            
        elif isinstance(event, CalculatePathRequest):
            goal = self.sector_by_coordinates(event.pos[0]/constants.GRID_SIZE, event.pos[1]/constants.GRID_SIZE)
            path = a_star(event.start_sector, goal, self)
            if not path == None:
                path.append(goal)
                for index, node in enumerate(path):
                    if index < len(path)-1:
                        new_event = CharactorTurnAndMoveRequest(node.neighbors.index(path[index+1]))
                        self.event_manager.post(new_event)
        
        elif isinstance(event, OccupiedSectorAction):
            event.function(self.charactor_by_coordinates(event.pos[0], event.pos[1]))
            
        elif isinstance(event, CharactorPlaceRequest):
            if not len(self.free_start_sector_indices) == 0:
                event.charactor.place(self.sectors[self.free_start_sector_indices.pop(0)])
          
            
#------------------------------------------------------------------------------
class Sector:
    """..."""
    def __init__(self, sector_id=0):
        self.sector_id = sector_id
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
            return True
        else:
            return False
        
    def __repr__(self):
        result = "[Sector] "
        result += "id: %s, " % (self.sector_id, )
        result += "neighbors: %s, " % ([neighbor.sector_id for neighbor in self.neighbors if not neighbor == None], )
        result += "open corners: %s" % ([open_corner.sector_id for open_corner in self.corners if not open_corner == None])
        return result

class MapState:
    """Keeps record of occupied sectors and actors occupying them"""
    def __init__(self, event_manager):
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.occupied_sectors_by_actor_id = {}
        self.actors_by_sector_id = {}
    
    def sector_is_free(self, sector):
        if sector not in self.occupied_sectors_by_actor_id.values():
            return True
        return False
    
    def notify(self, event):
        if isinstance(event, CharactorPlaceEvent) or isinstance(event, CharactorMoveEvent):
            self.occupied_sectors_by_actor_id[event.charactor.charactor_id] = event.charactor.sector
            self.actors_by_sector_id[event.charactor.sector.sector_id] = event.charactor
            #print [(c,d) for c,d in enumerate(self.actors_by_sector_id)]
            #print [(c, d) for c,d in enumerate(self.occupied_sectors_by_actor_id)]

        elif isinstance(event, FreeSectorAction):
            event.function(self.sector_is_free(event.sector))
            
