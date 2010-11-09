'''
Created on Oct 31, 2010

@author: pekka
'''

from event import *

class Bullets:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.newListeners.append(self)
        self.bullets = []
        
    def create_bullet(self, shooter):
        newBullet = Bullet(shooter)
        self.bullets.append(newBullet)
        return newBullet
        
    def destroy_bullet(self, bullet):
        self.bullets.remove(bullet)
        ev = BulletDestroyedEvent(bullet)
        self.evManager.post(ev)
        
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
        for b in self.bullets:
            b.age = b.age + 1
        ev = BulletsMoveEvent()
        self.evManager.post(ev)

class Bullet:
    """..."""
    
    def __init__(self, shooter):
        self.sector = shooter.sector
        self.direction = shooter.direction
        self.speed = 10
        self.age = 0