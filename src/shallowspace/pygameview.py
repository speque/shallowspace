'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
from sprites import CharactorSprite, SectorSprite, BulletSprite
from event import BulletChangedSectorEvent, TickEvent, CharactorPlaceEvent, MapBuiltEvent, \
CharactorMoveEvent, CharactorTurnEvent, BulletPlaceEvent, BulletsMoveEvent, BulletDestroyedEvent, \
SectorsLitRequest, DimAllSectorsRequest
import constants
import math

class PygameView:
    """A class representing the game view"""
    
    def __init__(self, ev_manager):
        self.event_manager = ev_manager
        self.event_manager.register_listener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (constants.GRID_SIZE*10, constants.GRID_SIZE*10) )
        game_title = constants.CONFIG.get('Texts', 'game_title')
        pygame.display.set_caption(game_title)
        
        board_image_file_name = constants.CONFIG.get('Images', 'board')
        
        self.background = pygame.image.load(board_image_file_name).convert()

        self.back_sprites = pygame.sprite.RenderUpdates()
        self.front_sprites = pygame.sprite.RenderUpdates()


    #----------------------------------------------------------------------
    def show_map(self, game_map):
        square_rect = pygame.Rect((-1*constants.GRID_SIZE, 0, constants.GRID_SIZE, constants.GRID_SIZE))

        i = 0
        for sector in game_map.sectors:
            if i < 10:
                square_rect = square_rect.move( constants.GRID_SIZE, 0 )
            else:
                i = 0
                square_rect = square_rect.move( -(constants.GRID_SIZE*9), constants.GRID_SIZE )
            i += 1
            new_sprite = SectorSprite( sector, self.back_sprites )
            new_sprite.rect = square_rect
            new_sprite = None

    #----------------------------------------------------------------------
    def show_charactor(self, charactor):
        charactor_sprite = CharactorSprite(self.front_sprites, charactor.sector.charactor_id)

        sector = charactor.sector
        sector_sprite = self.get_sector_sprite( sector )
        charactor_sprite.rect.center = sector_sprite.rect.center
        sector_sprite.lit()

    #----------------------------------------------------------------------
    def move_charactor(self, charactor):
        charactor_sprite = self.get_charactor_sprite( charactor )

        sector = charactor.sector
        sector_sprite = self.get_sector_sprite( sector )

        charactor_sprite.move_to = sector_sprite.rect.center
        
    #----------------------------------------------------------------------
    def turn_charactor(self, charactor):
        charactor_sprite = self.get_charactor_sprite( charactor )
        
        charactor_sprite.turn_to = charactor.direction
        
    #----------------------------------------------------------------------
    def show_bullet(self, sector, bullet):
        bullet_sprite = BulletSprite(bullet, self.front_sprites)
        bullet_sprite.rect.center = self.get_sector_sprite(sector).rect.center
        
    #----------------------------------------------------------------------
    def move_bullets(self):
        bullet_sprites = self.get_bullet_sprites()
        for bullet_sprite in bullet_sprites:
            if bullet_sprite.bullet.direction == constants.DIRECTION_UP:
                delta_x = 0
                delta_y = -1*bullet_sprite.bullet.speed
            elif bullet_sprite.bullet.direction == constants.DIRECTION_RIGHT:
                delta_x = bullet_sprite.bullet.speed
                delta_y = 0
            elif bullet_sprite.bullet.direction == constants.DIRECTION_DOWN:
                delta_x = 0
                delta_y = bullet_sprite.bullet.speed
            elif bullet_sprite.bullet.direction == constants.DIRECTION_LEFT:
                delta_x = -1*bullet_sprite.bullet.speed
                delta_y = 0
            center_x, center_y = bullet_sprite.rect.center
            bullet_sprite.move_to = (center_x + delta_x, center_y + delta_y)
            if math.floor(center_x/constants.GRID_SIZE) != math.floor((center_x + delta_x)/constants.GRID_SIZE) or \
            math.floor(center_y/constants.GRID_SIZE) != math.floor((center_y + delta_y) / constants.GRID_SIZE):
                new_event = BulletChangedSectorEvent(bullet_sprite.bullet)
                self.event_manager.post(new_event)
                
    #----------------------------------------------------------------------
    def destroy_bullet(self, bullet):
        bullet_sprites = self.get_bullet_sprites()
        for bullet_sprite in bullet_sprites:
            if bullet_sprite.bullet == bullet:
                bullet_sprite.remove(self.front_sprites)
        
    #----------------------------------------------------------------------
    def get_charactor_sprite(self, charactor):
        for sprite in self.front_sprites:
            if isinstance(sprite, CharactorSprite) and sprite.charactor_id == charactor.charactor_id:
                return sprite
        return None

    #----------------------------------------------------------------------
    def get_bullet_sprites(self):
        return [x for x in self.front_sprites if isinstance(x, BulletSprite)]
    
    #----------------------------------------------------------------------
    def dim_all_sectors(self):
        for sprite in self.back_sprites:
            if hasattr(sprite, "sector"):
                sprite.dim()
        
    #----------------------------------------------------------------------
    def lit_sectors(self, sectors):
        for sector in sectors:
            sector_sprite = self.get_sector_sprite(sector)
            sector_sprite.lit()
        
    #----------------------------------------------------------------------
    def get_sector_sprite(self, sector):
        for sprite in self.back_sprites:
            if hasattr(sprite, "sector") and sprite.sector == sector:
                return sprite

    #----------------------------------------------------------------------
    def draw(self):
        #draw Everything
        self.back_sprites.clear(self.window, self.background)
        self.front_sprites.clear(self.window, self.background)

        self.back_sprites.update()
        self.front_sprites.update()

        dirty_rects_1 = self.back_sprites.draw( self.window )
        dirty_rects_2 = self.front_sprites.draw( self.window )
        
        dirty_rects = dirty_rects_1 + dirty_rects_2
        pygame.display.update( dirty_rects )

    #----------------------------------------------------------------------
    def notify(self, event):
        if not isinstance( event, TickEvent):
            if isinstance( event, MapBuiltEvent):
                game_map = event.map
                self.show_map( game_map )

            elif isinstance( event, CharactorPlaceEvent ):
                self.show_charactor( event.charactor )

            elif isinstance( event, CharactorMoveEvent ):
                self.move_charactor( event.charactor )

            elif isinstance( event, CharactorTurnEvent ):
                self.turn_charactor( event.charactor )
                
            elif isinstance( event, BulletPlaceEvent ):
                self.show_bullet( event.sector, event.bullet )

            elif isinstance( event, BulletsMoveEvent ):
                self.move_bullets()
                
            elif isinstance( event, BulletDestroyedEvent ):
                self.destroy_bullet(event.bullet)
                
            elif isinstance( event, DimAllSectorsRequest ):
                self.dim_all_sectors()
                
            elif isinstance( event, SectorsLitRequest ):
                self.lit_sectors(event.sectors)
                
            self.draw()
