'''
Created on Dec 11, 2010

@author: pekka
'''

from actors import Charactor
from event import GameStartedEvent, CharactorMoveRequest, CharactorTurnAndMoveRequest, CharactorMoveToRequest, \
CalculatePathRequest, CharactorShootRequest, ActiveCharactorChangeRequest, TickEvent, FreeSectorActionRequest, \
ActiveCharactorChangeEvent

class Player:
    """..."""
    def __init__(self, evManager, idManager):
        self.evManager = evManager
        self.game = None
        self.name = ""
        self.evManager.register_listener(self)

        self.charactors = range(4)
        for index in range(len(self.charactors)):  
            self.charactors[index] = Charactor(evManager, idManager.getId())
        self.active_charactor = self.charactors[3]

    def __str__(self):
        return '<Player %s %s>' % (self.name, id(self))

    def notify(self, event):
        if not isinstance(event, TickEvent):
            if isinstance(event, GameStartedEvent):
                gameMap = event.game.map
                for index, charactor in enumerate(self.charactors):
                    charactor.place(gameMap.sectors[gameMap.startSectorIndices[index]])
            
            elif isinstance(event, CharactorMoveToRequest):
                ev = CalculatePathRequest(self.active_charactor.sector, event.pos)
                self.active_charactor.evManager.post(ev)
                    
            elif isinstance(event, CharactorShootRequest):
                self.active_charactor.shoot()
                
            elif isinstance(event, ActiveCharactorChangeRequest):
                if event.charactor in self.charactors:
                    self.active_charactor = event.charactor
                    ev = ActiveCharactorChangeEvent(self.active_charactor)
                    self.active_charactor.evManager.post(ev)
                        
            elif isinstance(event, CharactorMoveRequest) or isinstance(event, CharactorTurnAndMoveRequest):
                
                def MoveIfPossible(movePossible):
                    if movePossible:
                        self.active_charactor.move(event.direction)
            
                if isinstance(event, CharactorMoveRequest):
                    if self.active_charactor.direction != event.direction and not event.force:
                        # turn instead of move
                        self.active_charactor.turn(event.direction)
                    else:
                        # the charactor already faces that direction, let's move there, if the sector is free
                        f = MoveIfPossible
                        ev = FreeSectorActionRequest(self.active_charactor.sector.neighbors[event.direction], f)
                        self.evManager.post(ev)
                        
                elif isinstance(event, CharactorTurnAndMoveRequest):
                    if self.active_charactor.direction != event.direction:
                        self.active_charactor.turn(event.direction)
                    
                    f = MoveIfPossible
                    ev = FreeSectorActionRequest(self.active_charactor.sector.neighbors[event.direction], f)
                    self.evManager.post(ev)
                        
