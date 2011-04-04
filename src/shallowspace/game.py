'''
Created on Oct 31, 2010

@author: pekka
'''

from objects import Bullets
from player import Player
import constants
from event import GameStartedEvent, TickEvent, CharactorShootEvent, BulletPlaceEvent
from map import Map
import ConfigParser
import os

class Game:
    """..."""

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.state = Game.STATE_PREPARING
        
        self.id_generator = ObjectIdGenerator()
        
        self.players = [Player(event_manager, self.id_generator)]
        
        program_path = os.path.dirname(__file__)
        conf_file_path = os.path.abspath(os.path.join(program_path, "../../config/config.cfg"))
        config = ConfigParser.ConfigParser()
        config.read(conf_file_path)
        config.set("Images", "rootdir", os.path.abspath(os.path.join(program_path, "../../")))
        constants.CONFIG = config
        
        walls_up = [int(x) for x in constants.CONFIG.get('Map', 'walls_up')[0].split(',')]
        walls_right = [int(x) for x in constants.CONFIG.get('Map', 'walls_right')[0].split(',')]
        walls_down = [int(x) for x in constants.CONFIG.get('Map', 'walls_down')[0].split(',')]
        walls_left = [int(x) for x in constants.CONFIG.get('Map', 'walls_left')[0].split(',')]

        self.map = Map(event_manager, walls_up, walls_right, walls_left, walls_down)
        self.bullets = Bullets(event_manager)

    def start(self):
        self.map.build()
        self.state = Game.STATE_RUNNING
        event = GameStartedEvent()
        self.event_manager.post( event )

    def notify(self, event):
        if isinstance( event, TickEvent ):
            if self.state == Game.STATE_PREPARING:
                self.start()
        
        if isinstance( event, CharactorShootEvent ):
            bullet = self.bullets.create_bullet(event.charactor)
            new_event = BulletPlaceEvent(event.charactor.sector, bullet)
            self.event_manager.post(new_event)


class ObjectIdGenerator:
    """..."""
    def __init__(self):
        self.next_id = 0
    
    def get_id(self):
        result_id = self.next_id
        self.next_id = self.next_id + 1
        return result_id