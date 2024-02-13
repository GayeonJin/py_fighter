#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *
from gobject import *

CRASH_TYPE_NONE = 0
CRASH_TYPE_LIFE = 1
CRASH_TYPE_ENERGY = 2

AIRCRAFT_SPEED = 5
  
class aircraft_object(game_object) :
    def __init__(self, x, y, resource_id) :
        super().__init__(x, y, resource_id)

        self.init_position();
        self.set_life_count(3)

    def init_position(self) :
        self.set_position(gctrl.width * 0.05, gctrl.height / 2)

    def check_crash(self, enemy, sound_object) :
        is_crash = super().check_crash(enemy, sound_object)
        if is_crash == True :
            if enemy.type == CRASH_TYPE_LIFE :
                self.kill_life()
                enemy.kill_life()
            self.boom_count = 10

        return is_crash
    
    def draw(self) :
        super().draw()
        if self.boom_count > 0 :
            gctrl.surface.blit(self.boom, (self.x, self.y))
            self.boom_count -= 1

class bulles_group :
    BULLET_SPEED = 15
    SHOT_ENEMY = 1

    def __init__(self, speed = BULLET_SPEED) :
        self.bullets = []
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.speed = speed

    def add(self, x, y) :
        self.bullets.append(game_object(x, y, 'id_bullet'))

    def move(self, enemy) :
        is_shot = 0 
        for i, bullet in enumerate(self.bullets) :
            bullet.move(self.speed, 0)

            if bullet.check_crash(enemy, self.snd_shot) == True :
                self.bullets.remove(bullet)
                enemy.kill_life()
                is_shot = self.SHOT_ENEMY

            if bullet.is_out_of_range() == True :
                try :
                    self.bullets.remove(bullet)
                except :
                    pass
        
        return is_shot

    def draw(self) :
        for i, bullet in enumerate(self.bullets) :
            bullet.draw()        

if __name__ == '__main__' :
    print('fighter object')