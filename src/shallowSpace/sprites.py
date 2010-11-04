'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
from pygame.locals import RLEACCEL
from game import Game
import ConfigParser
#------------------------------------------------------------------------------
class SectorSprite(pygame.sprite.Sprite):
    def __init__(self, sector, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface( (70,70) )
        self.image = self.image.convert_alpha()
        self.image.fill( (0,0,0,0) )

        self.sector = sector

#------------------------------------------------------------------------------
class CharactorSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        #charactorSurf = pygame.Surface( (70,70) )
        #charactorSurf = charactorSurf.convert_alpha()
        #charactorSurf.fill((0,0,0,0)) #make transparent
        #pygame.draw.circle( charactorSurf, (255,0,0), (35,35), 22 )
        
        config = ConfigParser.ConfigParser()
        config.read(Game.CONF_FILE)
        gameTitle = config.get('Texts', 'gameTitle')
        
        boardImageFileName = config.get('Images', 'board')
        charactorSurf = pygame.image.load('../../data/img/marine.png').convert()
        colorkey = charactorSurf.get_at((0,0))
        charactorSurf.set_colorkey(colorkey, RLEACCEL)
        self.image = charactorSurf
        self.rect  = charactorSurf.get_rect()

        self.moveTo = None

    #----------------------------------------------------------------------
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
