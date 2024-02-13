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

if __name__ == '__main__' :
    print('stage object')
