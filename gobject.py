#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *

SOUND_MUTE = True

class game_object :
    global gctrl

    def __init__(self, x, y, resource_id, dx = 0, dy = 0) :
        if resource_id != None :
            resource_path = get_img_resource(resource_id)
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width()
            self.height = self.object.get_height()
        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.set_position(x, y)

        self.dx = dx
        self.dy = dy
        self.life_count = 1
        self.energy = 100

        self.boom = pygame.image.load(get_img_resource('id_boom'))
        self.boom_count = 0        

    def set_position(self, x, y) : 
        self.x = x
        self.y = y        
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1
        
    def set_speed(self, del_x, del_y) :
        self.dx = del_x
        self.dy = del_y

    def move(self, del_x = 0, del_y = 0) :
        if del_x == 0 and del_y == 0 : 
            del_x = self.dx
            del_y = self.dy

        self.x += del_x
        self.y += del_y

        if self.y < 0 :
            self.y = 0
        elif self.y > (gctrl.height - self.height) :
            self.y = (gctrl.height - self.height)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gctrl.surface.blit(self.object, (self.x, self.y))            

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= gctrl.width :
            return True
        else :
            return False

    def is_life(self) :
        if self.life_count > 0 :
            return True
        else :
            return False
    
    def set_life_count(self, count) :
        self.life_count = count
        if self.life_count > 0 :
            self.life = True

    def get_life_count(self) :
        return self.life_count
    
    def kill_life(self) :
        self.energy = 100
        self.boom_count = 10
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy, sound_object) :
        if enemy.is_life() == False :
            return False
        
        if self.object != None and enemy.object != None :
            if self.ex > enemy.x :
                if (self.y > enemy.y and self.y < enemy.ey) or (self.ey > enemy.y and self.ey < enemy.ey) :
                    #print("crashed1 : ",  self.x, self.y, self.ex, self.ey)
                    #print("crashed2 : ",  enemy.x, enemy.y, enemy.ex, enemy.ey)
                    if sound_object != None and SOUND_MUTE == False:
                        sound_object.play()
                    return True
        return False

if __name__ == '__main__' :
    print('game object')