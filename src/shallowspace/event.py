'''
Created on Oct 31, 2010

@author: pekka
'''

class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager"""
    def __init__(self):
        self.name = "Generic Event"

class TickEvent(Event):
    def __init__(self):
        self.name = "CPU Tick Event"

class QuitEvent(Event):
    def __init__(self):
        self.name = "Program Quit Event"

class MapBuiltEvent(Event):
    def __init__(self, gameMap):
        self.name = "Map Finished Building Event"
        self.map = gameMap

class GameStartedEvent(Event):
    def __init__(self, game):
        self.name = "Game Started Event"
        self.game = game

class CharactorMoveRequest(Event):
    def __init__(self, direction, force=False):
        self.name = "Charactor Move Request"
        self.direction = direction
        self.force = force

class CharactorTurnRequest(Event):
    def __init__(self, direction):
        self.name = "Charactor Turn Request"
        self.direction = direction
        
class CharactorTurnAndMoveRequest(Event):
    def __init__(self, direction):
        self.name = "Charactor Turn and Move Request"
        self.direction = direction        

class CharactorShootRequest(Event):
    def __init__(self):
        self.name = "Charactor Shoot Request"    
        
class CharactorPlaceEvent(Event):
    """this event occurs when a Charactor is *placed* in a sector,
    ie it doesn't move there from an adjacent sector."""
    def __init__(self, charactor):
        self.name = "Charactor Placement Event"
        self.charactor = charactor

class CharactorMoveEvent(Event):
    def __init__(self, charactor):
        self.name = "Charactor Move Event"
        self.charactor = charactor
        
class CharactorMoveToRequest(Event):
    def __init__(self, pos):
        self.name = "Charactor Move To Request"
        self.pos = pos        
        
class CharactorTurnEvent(Event):
    def __init__(self, charactor):
        self.name = "Charactor Turn Event"
        self.charactor = charactor        
        
class CharactorShootEvent(Event):
    def __init__(self, charactor):
        self.name = "Charactor Shoot Event"
        self.charactor = charactor
        
class BulletPlaceEvent(Event):
    def __init__(self, sector, bullet):
        self.name = "Bullet Place Event"
        self.sector = sector    
        self.bullet = bullet
        
class BulletsMoveEvent(Event):
    def __init__(self):
        self.name = "Bullets Move Event"    
        
class BulletChangedSectorEvent(Event):
    def __init__(self, bullet):
        self.name = "Bullet Changed Sector Event"
        self.bullet = bullet
        
class BulletDestroyedEvent(Event):
    def __init__(self, bullet):
        self.name = "Bullet Destroyed Event"
        self.bullet = bullet
        
class SectorsLitRequest(Event):
    def __init__(self, sectors):
        self.name = "Sectors Lit Request"
        self.sectors = sectors
        
class DimAllSectorsRequest(Event):
    def __init__(self):
        self.name = "Dim All Sectors Request"
        
class CalculatePathRequest(Event):
    def __init__(self, start_sector, pos):
        self.name = "Calculate Path Request"
        self.start_sector = start_sector
        self.pos = pos