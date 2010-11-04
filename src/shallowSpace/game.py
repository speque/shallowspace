'''
Created on Oct 31, 2010

@author: pekka
'''


import ConfigParser
from actors import Charactor
from controllers import *
#------------------------------------------------------------------------------
class Game:
    """..."""

    CONF_FILE = "/home/pekka/workspace/ShallowSpace/config/config.cfg"

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.state = Game.STATE_PREPARING
        
        self.players = [ Player(evManager) ]
        
        config = ConfigParser.ConfigParser()
        config.read(Game.CONF_FILE)
        wallsUp = [int(x) for x in config.get('Map', 'wallsUp').split(',')]
        wallsRight = [int(x) for x in config.get('Map', 'wallsRight').split(',')]
        wallsDown = [int(x) for x in config.get('Map', 'wallsDown').split(',')]
        wallsLeft = [int(x) for x in config.get('Map', 'wallsLeft').split(',')]

        self.map = Map(evManager, wallsUp, wallsRight, wallsLeft, wallsDown)

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

#------------------------------------------------------------------------------
class Player:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        #self.evManager.RegisterListener( self )

        self.charactors = [ Charactor(evManager) ]