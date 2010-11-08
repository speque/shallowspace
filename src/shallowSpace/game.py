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
        self.evManager.RegisterListener( self )

        self.state = Game.STATE_PREPARING
        
        self.players = [ Player(evManager) ]
        
        wallsUp = [int(x) for x in constants.CONFIG.get('Map', 'wallsUp').split(',')]
        wallsRight = [int(x) for x in constants.CONFIG.get('Map', 'wallsRight').split(',')]
        wallsDown = [int(x) for x in constants.CONFIG.get('Map', 'wallsDown').split(',')]
        wallsLeft = [int(x) for x in constants.CONFIG.get('Map', 'wallsLeft').split(',')]

        self.map = Map(evManager, wallsUp, wallsRight, wallsLeft, wallsDown)
        self.bullets = Bullets(evManager)

    #----------------------------------------------------------------------
    def Start(self):
        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent( self )
        self.evManager.Post( ev )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            if self.state == Game.STATE_PREPARING:
                self.Start()
        
        if isinstance( event, CharactorShootEvent ):
            bullet = self.bullets.createBullet(event.charactor)
            ev = BulletPlaceEvent(event.charactor.sector, bullet)
            self.evManager.Post(ev)

#------------------------------------------------------------------------------
class Player:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        #self.evManager.RegisterListener( self )

        self.charactors = [ Charactor(evManager) ]
