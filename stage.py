#!/usr/bin/python

import sys
import pygame
import random
import time

from gresource import *

class backgroud_object :
    def __init__(self, ) :
        self.object = pygame.image.load(get_img_resource('id_background'))
        self.object2 = self.object.copy()

        self.width = self.object.get_width()
        self.height = self.object.get_height()

        self.x = 0
        self.x2 = self.width
        self.scroll_width = -2

    def scroll(self) :
        self.x += self.scroll_width
        self.x2 += self.scroll_width

        if self.x == -self.width:
            self.x = self.width

        if self.x2 == -self.width:
            self.x2 = self.width

    def draw(self) :
        gctrl.surface.blit(self.object, (self.x, 0))
        gctrl.surface.blit(self.object2, (self.x2, 0))

class stage :
    STATE_WAIT = 0
    STATE_RUN = 1
    STATE_NEXT = 2

    def __init__(self) :
        self.stage_no = 1
        self.state = stage.STATE_WAIT
        self.stage_timer = 0

        self.enemy_count = 0
        self.enemy_max = 40
        self.kill_enemy_count = 0
        self.kill_enemy_max = 10
        self.missed_enemy_count = 0

    def update_missed_enemy(self, num) :
        self.missed_enemy_count += num

    def update_kill_enemy(self) :
        self.kill_enemy_count += 1
        print('kill enemy : %d'%self.kill_enemy_count)
        if self.kill_enemy_count >= self.kill_enemy_max :
            self.stage_no += 1
            self.kill_enemy_count = 0
            #self.kill_enemy_max += 10
            self.missed_enemy_count = 0
            self.state = stage.STATE_NEXT
            print('go to next stage')

    def draw(self) :
        if self.state == stage.STATE_WAIT :
            gctrl.draw_string("Stage " + str(self.stage_no), 0, gctrl.height / 2, ALIGN_CENTER | ALIGN_TOP, 30, COLOR_BLACK)
            
            self.stage_timer += 1
            if self.stage_timer >= 3 * FPS : 
                self.state = stage.STATE_RUN
                self.stage_timer = 0

if __name__ == '__main__' :
    print('stage object')
