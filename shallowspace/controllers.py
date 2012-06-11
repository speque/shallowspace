'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
import constants
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_SPACE, K_UP, K_DOWN, K_RIGHT, K_LEFT, \
MOUSEBUTTONUP
from event import TickEvent, QuitEvent, CharactorShootRequest, CharactorMoveRequest, \
CharactorMoveToRequest, ActiveCharactorChangeRequest

#------------------------------------------------------------------------------
class KeyboardController:
    """..."""
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance( event, TickEvent ):
            #Handle Input Events
            for event in pygame.event.get():
                new_event = None
                if event.type == QUIT:
                    new_event = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    new_event = QuitEvent()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    new_event = CharactorShootRequest()
                elif event.type == KEYDOWN and event.key == K_UP:
                    direction = constants.DIRECTION_UP
                    new_event = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    direction = constants.DIRECTION_DOWN
                    new_event = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    direction = constants.DIRECTION_LEFT
                    new_event = CharactorMoveRequest(direction)
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    direction = constants.DIRECTION_RIGHT
                    new_event = CharactorMoveRequest(direction)
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    new_event = CharactorMoveToRequest(event.pos)
                elif event.type == MOUSEBUTTONUP and event.button == 3:
                    new_event = ActiveCharactorChangeRequest(event.pos)

                if new_event:
                    self.event_manager.post(new_event)


#------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener( self )

        self.keep_going = True

    #----------------------------------------------------------------------
    def run(self):
        clock = pygame.time.Clock()
        while self.keep_going:
            clock.tick(60)
            event = TickEvent()
            self.event_manager.post(event)

    #----------------------------------------------------------------------
    def notify(self, event):
        if isinstance( event, QuitEvent ):
            #this will stop the while loop from running
            self.keep_going = False
