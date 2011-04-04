'''
Created on Dec 11, 2010

@author: pekka
'''

from actors import Charactor
from event import GameStartedEvent, CharactorMoveRequest, CharactorTurnAndMoveRequest, CharactorMoveToRequest, \
CalculatePathRequest, CharactorShootRequest, ActiveCharactorChangeRequest, TickEvent, FreeSectorAction, \
ActiveCharactorChangeEvent, OccupiedSectorAction, CharactorPlaceRequest

class Player:
    """..."""
    def __init__(self, event_manager, id_manager):
        self.event_manager = event_manager
        self.game = None
        self.name = ""
        self.event_manager.register_listener(self)

        self.charactors = range(4)
        for index in range(len(self.charactors)):  
            self.charactors[index] = Charactor(event_manager, id_manager.get_id())
        self.active_charactor = self.charactors[3]

    def __str__(self):
        return '<Player %s %s>' % (self.name, id(self))

    def notify(self, event):
        if not isinstance(event, TickEvent):
            if isinstance(event, GameStartedEvent):
                for charactor in self.charactors:
                    request = CharactorPlaceRequest(charactor)
                    self.event_manager.post(request)
            
            elif isinstance(event, CharactorMoveToRequest):
                new_event = CalculatePathRequest(self.active_charactor.sector, event.pos)
                self.event_manager.post(new_event)
                    
            elif isinstance(event, CharactorShootRequest):
                self.active_charactor.shoot()
                
            elif isinstance(event, ActiveCharactorChangeRequest):
                def change_active_charactor(charactor):
                    if not charactor == None and charactor in self.charactors and not charactor == self.active_charactor:
                        self.active_charactor = charactor
                        new_event = ActiveCharactorChangeEvent(self.active_charactor)
                        self.active_charactor.event_manager.post(new_event)
                        
                function = change_active_charactor
                new_event = OccupiedSectorAction(event.pos, function)
                self.event_manager.post(new_event)
                        
            elif isinstance(event, CharactorMoveRequest) or isinstance(event, CharactorTurnAndMoveRequest):
                
                def move_if_possible(move_possible):
                    if move_possible:
                        self.active_charactor.move(event.direction)
            
                if isinstance(event, CharactorMoveRequest):
                    if self.active_charactor.direction != event.direction and not event.force:
                        # turn instead of move
                        self.active_charactor.turn(event.direction)
                    else:
                        # the charactor already faces that direction, let's move there, if the sector is free
                        function = move_if_possible
                        new_event = FreeSectorAction(self.active_charactor.sector.neighbors[event.direction], function)
                        self.event_manager.post(new_event)
                        
                elif isinstance(event, CharactorTurnAndMoveRequest):
                    if self.active_charactor.direction != event.direction:
                        self.active_charactor.turn(event.direction)
                    
                    function = move_if_possible
                    new_event = FreeSectorAction(self.active_charactor.sector.neighbors[event.direction], function)
                    self.event_manager.post(new_event)
                        
