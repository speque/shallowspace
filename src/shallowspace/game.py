'''
Created on Oct 31, 2010

@author: pekka
'''

from objects import Bullets
from player import Player
import constants
from event import GameStartedEvent, TickEvent, CharactorShootEvent, BulletPlaceEvent, CharactorPlaceEvent
from map import Map
import ConfigParser
import os

class Game:
    """..."""

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener(self)

        self.state = Game.STATE_PREPARING
        
        self.idGenerator = ObjectIdGenerator()
        #self.state = GameState()
        
        self.players = [Player(evManager, self.idGenerator)]
        
        programPath = os.path.dirname(__file__)
        confFilePath = os.path.abspath(os.path.join(programPath, "../../config/config.cfg"))
        config = ConfigParser.ConfigParser()
        config.read(confFilePath)
        config.set("Images", "rootdir", os.path.abspath(os.path.join(programPath, "../../")))
        constants.CONFIG = config
        
        wallsUp = [int(x) for x in constants.CONFIG.get('Map', 'wallsUp').split(',')]
        wallsRight = [int(x) for x in constants.CONFIG.get('Map', 'wallsRight').split(',')]
        wallsDown = [int(x) for x in constants.CONFIG.get('Map', 'wallsDown').split(',')]
        wallsLeft = [int(x) for x in constants.CONFIG.get('Map', 'wallsLeft').split(',')]

        self.map = Map(evManager, wallsUp, wallsRight, wallsLeft, wallsDown)
        self.bullets = Bullets(evManager)

    def start(self):
        self.map.build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent( self )
        self.evManager.post( ev )

    def notify(self, event):
        if isinstance( event, TickEvent ):
            if self.state == Game.STATE_PREPARING:
                self.start()
        
        if isinstance( event, CharactorShootEvent ):
            bullet = self.bullets.create_bullet(event.charactor)
            ev = BulletPlaceEvent(event.charactor.sector, bullet)
            self.evManager.post(ev)


class ObjectIdGenerator:
    """..."""
    def __init__(self):
        self.nextId = 0
    
    def getId(self):
        id = self.nextId
        self.nextId = self.nextId + 1
        return id
    
    
class GameState:
    """..."""
    def __init__(self, evManager):
        evManager.register_listener(self)
        #map from actors to sectors
        self.actors = []
    
    def sectorIsFree(self, sector):
        blockedSectors = [c.sector for c in self.actors]
        if sector in blockedSectors:
            return False
        return True
        
    def notify(self, event):
        if isinstance(event, CharactorPlaceEvent):
            self.actors.append(event.charactor)
