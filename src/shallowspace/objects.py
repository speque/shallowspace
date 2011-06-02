'''
Created on Oct 31, 2010

@author: pekka
'''

from event import BulletDestroyedEvent, BulletChangedSectorEvent, TickEvent, BulletsMoveEvent

class Bullets:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.bullets = []
        
    def create_bullet(self, sector, direction):
        new_bullet = Bullet(sector, direction)
        self.bullets.append(new_bullet)
        return new_bullet
        
    def destroy_bullet(self, bullet):
        self.bullets.remove(bullet)
        event = BulletDestroyedEvent(bullet)
        self.event_manager.post(event)
        
    def notify(self, event):
        if len(self.bullets) != 0 and isinstance(event, TickEvent):
            self.move_bullets()
        elif isinstance(event, BulletChangedSectorEvent):
            bullet = event.bullet
            if bullet.sector.neighbors[bullet.direction]:
                bullet.sector = bullet.sector.neighbors[bullet.direction]
            else:
                self.destroy_bullet(bullet)
            
    def move_bullets(self):
        event = BulletsMoveEvent()
        self.event_manager.post(event)

class Bullet:
    """..."""
    
    def __init__(self, sector, direction):
        self.sector = sector
        self.direction = direction
        self.speed = 20
