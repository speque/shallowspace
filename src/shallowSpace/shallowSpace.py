from utils import *
import ConfigParser
import pygame
from sprites import CharactorSprite, SectorSprite
from event import TickEvent, CharactorPlaceEvent, CharactorMoveEvent, MapBuiltEvent
from game import Game

#------------------------------------------------------------------------------
class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""
    def __init__(self ):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue= []

    #----------------------------------------------------------------------
    def RegisterListener( self, listener ):
        self.listeners[ listener ] = 1

    #----------------------------------------------------------------------
    def UnregisterListener( self, listener ):
        if listener in self.listeners:
            del self.listeners[ listener ]
        
    #----------------------------------------------------------------------
    def Post( self, event ):
        if not isinstance(event, TickEvent):
            Debug( "     Message: " + event.name )
        for listener in self.listeners:
            #NOTE: If the weakref has died, it will be 
            #automatically removed, so we don't have 
            #to worry about it.
            listener.Notify( event )

#------------------------------------------------------------------------------
class PygameView:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (700,700) )
        config = ConfigParser.ConfigParser()
        config.read(Game.CONF_FILE)
        gameTitle = config.get('Texts', 'gameTitle')
        pygame.display.set_caption(gameTitle)
        
        boardImageFileName = config.get('Images', 'board')
        
        self.background = pygame.image.load(boardImageFileName).convert()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()


    #----------------------------------------------------------------------
    def ShowMap(self, gameMap):
        squareRect = pygame.Rect( (-70,0, 70,70 ) )

        i = 0
        for sector in gameMap.sectors:
            if i < 10:
                squareRect = squareRect.move( 70,0 )
            else:
                i = 0
                squareRect = squareRect.move( -(70*9), 70 )
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
    def GetCharactorSprite(self, charactor):
        #there will be only one
        for s in self.frontSprites:
            return s
        return None

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
                
            self.Draw()

#------------------------------------------------------------------------------
from controllers import KeyboardController, CPUSpinnerController

def main():
    """..."""
    evManager = EventManager()

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    pygameView = PygameView( evManager )
    game = Game( evManager )
    
    spinner.Run()

if __name__ == "__main__":
    main()
