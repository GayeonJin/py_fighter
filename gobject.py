#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *

AIRCRAFT_SPEED = 5
BULLET_SPEED = 15
ENEMY_SPEED = -7
FIRE_SPEED = -15
NOFIRE_SPEED = -30

class game_object :
    global gctrl

    def __init__(self, x, y, resource_id) :
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

        self.dx = 0
        self.dy = 0
        self.life_count = 1

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
        if del_x == 0 :
            del_x = self.dx
        if del_y == 0 :
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
        self.boom_count = 10
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy_item, sound_object) :
        if self.object != None and enemy_item.object != None :
            if self.ex > enemy_item.x :
                if (self.y > enemy_item.y and self.y < enemy_item.ey) or (self.ey > enemy_item.y and self.ey < enemy_item.ey) :
                    #print("crashed1 : ",  self.x, self.y, self.ex, self.ey)
                    #print("crashed2 : ",  enemy_item.x, enemy_item.y, enemy_item.ex, enemy_item.ey)
                    if sound_object != None :
                        sound_object.play()
                    return True
        return False
    
class aircraft_object(game_object) :
    CRASH_LIFE = 0
    CRASH_ENERGY = 1

    def __init__(self, x, y, resource_id) :
        super().__init__(x, y, resource_id)

    def init_position(self) :
        self.set_position(gctrl.width * 0.05, gctrl.height / 2)

    def check_crash(self, enemy_item, sound_object, crash_type) :
        is_crash = super().check_crash(enemy_item, sound_object)
        if is_crash == True :
            if crash_type == self.CRASH_LIFE :
                self.kill_life()
            self.boom_count = 10

        return is_crash
    
    def draw(self) :
        super().draw()
        if self.boom_count > 0 :
            gctrl.surface.blit(self.boom, (self.x, self.y))
            self.boom_count -= 1

class enemy_object(game_object) :
    def __init__(self, x, y, resource_id, speed) :
        super().__init__(x, y, resource_id)

        self.set_speed(speed, 0)        
        self.kill_timer = 0

    def init_position(self) :
        self.set_position(gctrl.width, random.randrange(0, gctrl.height - self.height))
        self.kill_timer = 0

    def move(self) :
        if self.is_life() == True :
            super().move()
            if self.is_out_of_range() == True :
                self.init_position()

    def kill_time(self) :
        self.kill_timer += 1
        if self.kill_timer > 10 :
            return False
    
        return True

    def draw(self) :
        if self.is_life() == True :
            super().draw()
        else :
            gctrl.surface.blit(self.boom, (self.x, self.y))   

            if self.kill_time() == False :
                self.init_position()
                self.set_life_count(1)
   
class bulles_group :
    def __init__(self, speed = BULLET_SPEED) :
        self.bullets = []
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.speed = speed

    def add(self, x, y) :
        self.bullets.append(game_object(x, y, 'id_bullet'))

    def move(self, enemy) :
        crash = False 
        for i, bullet in enumerate(self.bullets) :
            bullet.move(self.speed, 0)

            if bullet.check_crash(enemy, self.snd_shot) == True :
                self.bullets.remove(bullet)
                crash = True

            if bullet.is_out_of_range() == True :
                try :
                    self.bullets.remove(bullet)
                except :
                    pass
        
        return crash

    def draw(self) :
        for i, bullet in enumerate(self.bullets) :
            bullet.draw()        

class fires_group :
    def __init__(self) :
        self.fires = []

        self.fires.append(enemy_object(0, 0, 'id_fire1', FIRE_SPEED))
        self.fires.append(enemy_object(0, 0, 'id_fire2', FIRE_SPEED))
        for i in range(3) :
            self.fires.append(enemy_object(0, 0, None, NOFIRE_SPEED))

    def get_fire(self) :
        random.shuffle(self.fires)
        fire = self.fires[0]
        fire.init_position()        

        return fire

if __name__ == '__main__' :
    print('game object')