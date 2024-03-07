#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *
from gobject import *

class bullets_group :
    BULLET_DX = 15
    BULLET_DY = 0
    SHOT_ENEMY = 1

    def __init__(self) :
        self.bullets = []
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))

    def add(self, x, y, id = 'id_bullet', dx = BULLET_DX, dy = BULLET_DY) :
        self.bullets.append(game_object(x, y, id, dx, dy))
        #self.bullets.append(game_object(x, y, id, dx-1, dy+1))
        #self.bullets.append(game_object(x, y, id, dx-1, dy-1))

    def move(self, enemies) :
        is_shot = 0 

        for i, bullet in enumerate(self.bullets) :
            bullet.move(bullet.dx, bullet.dy)

            for j, enemy in enumerate(enemies) :
                if bullet.check_crash(enemy, self.snd_shot) == True :
                    self.bullets.remove(bullet)
                    enemy.kill_life()
                    is_shot = self.SHOT_ENEMY

                if bullet.is_out_of_range() == True :
                    try :
                        self.bullets.remove(bullet)
                    except :
                        pass

                if is_shot == self.SHOT_ENEMY :
                    return is_shot
        return 0

    def draw(self) :
        for i, bullet in enumerate(self.bullets) :
            bullet.draw()        

if __name__ == '__main__' :
    print('fighter object')