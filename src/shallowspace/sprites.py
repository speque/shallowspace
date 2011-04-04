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
        self.image = pygame.Surface((70, 70))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 235))
        self.found = False

        self.sector = sector
        
    def dim(self):
        if self.found:
            self.image.fill((0, 0, 0, 100))
        
    def lit(self):
        self.image.fill((0, 0, 0, 0))
        self.found = True
#------------------------------------------------------------------------------
class BulletSprite(pygame.sprite.Sprite):
    """ A class representing a sprite for a bullet """
    
    def __init__(self, bullet, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        
        bullet_sprite_file_name = constants.CONFIG.get('Images', 'bullet')
        bullet_surf = pygame.image.load(bullet_sprite_file_name).convert()
        colorkey = bullet_surf.get_at((0, 0))
        bullet_surf.set_colorkey(colorkey, RLEACCEL)
        self.image = bullet_surf
        self.rect  = bullet_surf.get_rect()
        
        self.bullet = bullet
        self.move_to = None
        
    def update(self):
        if self.move_to:
            self.rect.center = self.move_to
            self.move_to = None

#------------------------------------------------------------------------------
class CharactorSprite(pygame.sprite.Sprite):
    """ A class representing a sprite for a charactor """
    
    def __init__(self, group=None, charactor_id=0):
        pygame.sprite.Sprite.__init__(self, group)
        
        marine_sprite_file_name = constants.CONFIG.get('Images', 'marine')
        charactor_surf = pygame.image.load(marine_sprite_file_name).convert()
        colorkey = charactor_surf.get_at((0, 0))
        charactor_surf.set_colorkey(colorkey, RLEACCEL)
        self.original_image = charactor_surf
        self.image = charactor_surf
        self.rect  = charactor_surf.get_rect()

        self.move_to = None
        self.turn_to = None
        self.charactor_id = charactor_id

    #----------------------------------------------------------------------
    def update(self):
        if self.move_to:
            self.rect.center = self.move_to
            self.move_to = None
            
        if self.turn_to != None:
            if self.turn_to == 0:
                self.turn_to = 2
            elif self.turn_to == 2:
                self.turn_to = 0
            self.image = pygame.transform.rotate(self.original_image, self.turn_to*90)
            self.turn_to = None 