'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
import constants
from pygame.locals import *
from event import *

#------------------------------------------------------------------------------
class KeyboardController:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener( self )

    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance( event, TickEvent ):
            #Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                     and event.key == K_ESCAPE:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                     and event.key == K_SPACE:
                    ev = CharactorShootRequest()
                elif event.type == KEYDOWN \
                     and event.key == K_UP:
                    direction = constants.DIRECTION_UP
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                     and event.key == K_DOWN:
                    direction = constants.DIRECTION_DOWN
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                     and event.key == K_LEFT:
                    direction = constants.DIRECTION_LEFT
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                     and event.key == K_RIGHT:
                    direction = constants.DIRECTION_RIGHT
                    ev = CharactorMoveRequest(direction)

                if ev:
                    self.evManager.post( ev )


#------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.register_listener( self )

        self.keepGoing = 1

    #----------------------------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()
        while self.keepGoing:
            self.evManager.update_listeners()
            clock.tick(60)
            event = TickEvent()
            self.evManager.post( event )

    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance( event, QuitEvent ):
            #this will stop the while loop from running
            self.keepGoing = False
