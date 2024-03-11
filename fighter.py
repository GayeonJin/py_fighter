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

        self.init_position()

    def init_position(self) :
        self.set_position(gctrl.width * 0.05, gctrl.height / 2)

    def callback_kill(self) :
        if self.energy == 0 :
            self.init_position()
            self.status = game_object.STATUS_KILL
        else :
            self.status = game_object.STATUS_ACTIVE

    def check_crash(self, enemies, sound_object) :
        for i, enemy in enumerate(enemies) :
            is_crash = super().check_crash(enemy, sound_object)
            if is_crash == True :
                if enemy.type == CRASH_TYPE_LIFE :
                    self.energy = 0
                    self.set_inactive()
                    enemy.set_inactive()
                elif enemy.type == CRASH_TYPE_ENERGY and self.status == game_object.STATUS_ACTIVE :
                    print('decrease energy')
                    self.energy -= 20
                    self.set_inactive()

                return is_crash
        
        return False

if __name__ == '__main__' :
    print('fighter object')