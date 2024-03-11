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

class enemy_object(game_object) :
    AREA_IN = 0
    AREA_OUT = 1

    def __init__(self, x, y, info) :
        super().__init__(x, y, info[0])

        self.set_speed(info[1], 0)
        self.init_position()

        self.type = info[2]

    def init_position(self) :
        self.set_position(gctrl.width, random.randrange(0, gctrl.height - self.height))
        self.shoot_timer = 0

    def move(self) :
        if self.status == game_object.STATUS_ACTIVE :
            super().move()
            if self.is_out_of_range() == True :
                self.init_position()
                return self.AREA_OUT
            
        return self.AREA_IN

    def callback_kill(self) :
        self.init_position()
        self.set_life()

    def draw(self) :
        if self.status == game_object.STATUS_ACTIVE :
            super().draw()

class enemy_group :
    def __init__(self) :
        self.enemies = []

    def add(self, enemy) :
        self.enemies.append(enemy)

    def clear(self) :
        self.enemies = []

    def move(self) :
        remove_count = 0
        for i, enemy in enumerate(self.enemies) :
            if enemy.move() == enemy_object.AREA_OUT : 
                self.enemies.remove(enemy)
                remove_count += 1
                
        return remove_count

    def draw(self) :
        for i, enemy in enumerate(self.enemies) :
            enemy.draw()    

class fires_resource :
    FIRE_SPEED = -15
    NOFIRE_SPEED = -30

    def __init__(self) :
        self.fires = [
            ('id_fire1', self.FIRE_SPEED, CRASH_TYPE_ENERGY),
            ('id_fire2', self.FIRE_SPEED, CRASH_TYPE_ENERGY),
            (None, self.NOFIRE_SPEED, CRASH_TYPE_NONE),
            (None, self.NOFIRE_SPEED, CRASH_TYPE_NONE), 
            (None, self.NOFIRE_SPEED, CRASH_TYPE_NONE),           
        ]

    def get_info(self) :
        random.shuffle(self.fires)   
        return self.fires[0]

if __name__ == '__main__' :
    print('enemy object')