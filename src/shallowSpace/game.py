'''
Created on Oct 31, 2010

@author: pekka
'''

from actors import Charactor
from objects import *
from controllers import *
from map import Map
#------------------------------------------------------------------------------
class Game:
    """..."""

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener( self )

        self.state = Game.STATE_PREPARING
        
        self.players = [ Player(evManager) ]
        
        wallsUp = [int(x) for x in constants.CONFIG.get('Map', 'wallsUp').split(',')]
        wallsRight = [int(x) for x in constants.CONFIG.get('Map', 'wallsRight').split(',')]
        wallsDown = [int(x) for x in constants.CONFIG.get('Map', 'wallsDown').split(',')]
        wallsLeft = [int(x) for x in constants.CONFIG.get('Map', 'wallsLeft').split(',')]

        self.map = Map(evManager, wallsUp, wallsRight, wallsLeft, wallsDown)
        self.bullets = Bullets(evManager)

    #----------------------------------------------------------------------
    def start(self):
        self.map.build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent( self )
        self.evManager.post( ev )

    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance( event, TickEvent ):
            if self.state == Game.STATE_PREPARING:
                self.start()
        
        if isinstance( event, CharactorShootEvent ):
            bullet = self.bullets.create_bullet(event.charactor)
            ev = BulletPlaceEvent(event.charactor.sector, bullet)
            self.evManager.post(ev)

#------------------------------------------------------------------------------
class Player:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        #self.evManager.register_listener( self )

        self.charactors = [ Charactor(evManager) ]
