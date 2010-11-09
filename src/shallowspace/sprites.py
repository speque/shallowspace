'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
from pygame.locals import RLEACCEL
import constants
#------------------------------------------------------------------------------
class SectorSprite(pygame.sprite.Sprite):
    """ A class representing a sprite for board sector """
    
    def __init__(self, sector, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface( (70,70) )
        self.image = self.image.convert_alpha()
        self.image.fill( (0,0,0,0) )

        self.sector = sector
        
#------------------------------------------------------------------------------
class BulletSprite(pygame.sprite.Sprite):
    """ A class representing a sprite for a bullet """
    
    def __init__(self, bullet, sector, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        
        bulletSpriteFileName = constants.CONFIG.get('Images', 'bullet')
        bulletSurf = pygame.image.load(bulletSpriteFileName).convert()
        colorkey = bulletSurf.get_at((0,0))
        bulletSurf.set_colorkey(colorkey, RLEACCEL)
        self.image = bulletSurf
        self.rect  = bulletSurf.get_rect()
        
        self.bullet = bullet
        self.moveTo = None
        
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None

#------------------------------------------------------------------------------
class CharactorSprite(pygame.sprite.Sprite):
    """ A class representing a sprite for a charactor """
    
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        
        marineSpriteFileName = constants.CONFIG.get('Images', 'marine')
        charactorSurf = pygame.image.load(marineSpriteFileName).convert()
        colorkey = charactorSurf.get_at((0,0))
        charactorSurf.set_colorkey(colorkey, RLEACCEL)
        self.originalImage = charactorSurf
        self.image = charactorSurf
        self.rect  = charactorSurf.get_rect()

        self.moveTo = None
        self.turnTo = None

    #----------------------------------------------------------------------
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
            
        if self.turnTo != None:
            if self.turnTo == 0:
                self.turnTo = 2
            elif self.turnTo == 2:
                self.turnTo = 0
            self.image = pygame.transform.rotate(self.originalImage, self.turnTo*90)
            self.turnTo = None 