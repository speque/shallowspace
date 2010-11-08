'''
Created on Oct 31, 2010

@author: pekka
'''

import pygame
from sprites import CharactorSprite, SectorSprite, BulletSprite
from event import *
import constants
import math

class PygameView:
    """A class representing the game view"""
    
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (constants.GRID_SIZE*10, constants.GRID_SIZE*10) )
        gameTitle = constants.CONFIG.get('Texts', 'gameTitle')
        pygame.display.set_caption(gameTitle)
        
        boardImageFileName = constants.CONFIG.get('Images', 'board')
        
        self.background = pygame.image.load(boardImageFileName).convert()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()


    #----------------------------------------------------------------------
    def ShowMap(self, gameMap):
        squareRect = pygame.Rect( ( -1*constants.GRID_SIZE,0, constants.GRID_SIZE, constants.GRID_SIZE ) )

        i = 0
        for sector in gameMap.sectors:
            if i < 10:
                squareRect = squareRect.move( constants.GRID_SIZE, 0 )
            else:
                i = 0
                squareRect = squareRect.move( -(constants.GRID_SIZE*9), constants.GRID_SIZE )
            i += 1
            newSprite = SectorSprite( sector, self.backSprites )
            newSprite.rect = squareRect
            newSprite = None

    #----------------------------------------------------------------------
    def ShowCharactor(self, charactor):
        charactorSprite = CharactorSprite( self.frontSprites )

        sector = charactor.sector
        sectorSprite = self.GetSectorSprite( sector )
        charactorSprite.rect.center = sectorSprite.rect.center

    #----------------------------------------------------------------------
    def MoveCharactor(self, charactor):
        charactorSprite = self.GetCharactorSprite( charactor )

        sector = charactor.sector
        sectorSprite = self.GetSectorSprite( sector )

        charactorSprite.moveTo = sectorSprite.rect.center
        
    #----------------------------------------------------------------------
    def TurnCharactor(self, charactor):
        charactorSprite = self.GetCharactorSprite( charactor )
        
        charactorSprite.turnTo = charactor.direction
        
    #----------------------------------------------------------------------
    def ShowBullet(self, sector, bullet):
        bulletSprite = BulletSprite(bullet, sector, self.frontSprites)
        bulletSprite.rect.center = self.GetSectorSprite(sector).rect.center
        
    #----------------------------------------------------------------------
    def MoveBullets(self):
        bulletSprites = self.GetBulletSprites()
        for b in bulletSprites:
            if b.bullet.direction == constants.DIRECTION_UP:
                deltaX = 0
                deltaY = -1*b.bullet.speed
            elif b.bullet.direction == constants.DIRECTION_RIGHT:
                deltaX = b.bullet.speed
                deltaY = 0
            elif b.bullet.direction == constants.DIRECTION_DOWN:
                deltaX = 0
                deltaY = b.bullet.speed
            elif b.bullet.direction == constants.DIRECTION_LEFT:
                deltaX = -1*b.bullet.speed
                deltaY = 0
            x, y = b.rect.center
            b.moveTo = (x + deltaX, y + deltaY)
            if math.floor(x/constants.GRID_SIZE) != math.floor((x + deltaX)/constants.GRID_SIZE) or \
            math.floor(y/constants.GRID_SIZE) != math.floor((y + deltaY) / constants.GRID_SIZE):
                ev = BulletChangedSectorEvent(b.bullet)
                self.evManager.Post(ev)
                
    #----------------------------------------------------------------------
    def DestroyBullet(self, bullet):
        bulletSprites = self.GetBulletSprites()
        for b in bulletSprites:
            if b.bullet == bullet:
                b.remove(self.frontSprites)
        
    #----------------------------------------------------------------------
    def GetCharactorSprite(self, charactor):
        for s in self.frontSprites:
            if isinstance(s, CharactorSprite):
                #currently there is only one
                return s
        return None

    #----------------------------------------------------------------------
    def GetBulletSprites(self):
        return [x for x in self.frontSprites if isinstance(x, BulletSprite)]
        
    #----------------------------------------------------------------------
    def GetSectorSprite(self, sector):
        for s in self.backSprites:
            if hasattr(s, "sector") and s.sector == sector:
                return s

    #----------------------------------------------------------------------
    def Draw(self):
        #Draw Everything
        self.backSprites.clear( self.window, self.background )
        self.frontSprites.clear( self.window, self.background )

        self.backSprites.update()
        self.frontSprites.update()

        dirtyRects1 = self.backSprites.draw( self.window )
        dirtyRects2 = self.frontSprites.draw( self.window )
        
        dirtyRects = dirtyRects1 + dirtyRects2
        pygame.display.update( dirtyRects )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if not isinstance( event, TickEvent ):
            if isinstance( event, MapBuiltEvent ):
                gameMap = event.map
                self.ShowMap( gameMap )

            elif isinstance( event, CharactorPlaceEvent ):
                self.ShowCharactor( event.charactor )

            elif isinstance( event, CharactorMoveEvent ):
                self.MoveCharactor( event.charactor )

            elif isinstance( event, CharactorTurnEvent ):
                self.TurnCharactor( event.charactor )
                
            elif isinstance( event, BulletPlaceEvent ):
                self.ShowBullet( event.sector, event.bullet )

            elif isinstance( event, BulletsMoveEvent ):
                self.MoveBullets()
                
            elif isinstance( event, BulletDestroyedEvent ):
                self.DestroyBullet(event.bullet)
                
            self.Draw()
