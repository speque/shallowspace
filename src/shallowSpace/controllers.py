'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
from pygame.locals import *
from map import Map
from event import *
#------------------------------------------------------------------------------
class KeyboardController:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

    #----------------------------------------------------------------------
    def Notify(self, event):
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
                     and event.key == K_UP:
                    direction = Map.DIRECTION_UP
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                     and event.key == K_DOWN:
                    direction = Map.DIRECTION_DOWN
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                     and event.key == K_LEFT:
                    direction = Map.DIRECTION_LEFT
                    ev = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN \
                     and event.key == K_RIGHT:
                    direction = Map.DIRECTION_RIGHT
                    ev = CharactorMoveRequest(direction)

                if ev:
                    self.evManager.Post( ev )


#------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.keepGoing = 1

    #----------------------------------------------------------------------
    def Run(self):
        clock = pygame.time.Clock()
        while self.keepGoing:
            clock.tick(10)
            event = TickEvent()
            self.evManager.Post( event )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, QuitEvent ):
            #this will stop the while loop from running
            self.keepGoing = False