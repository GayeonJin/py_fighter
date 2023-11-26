#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gobject import *
from gresource import *

TITLE_STR = "Py Fighter"

SCORE_UNIT = 10

STATUS_XOFFSET = 10
STATUS_YOFFSET = 5

def draw_life(count) :
    gctrl.draw_string("Life : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_RIGHT)

def draw_score(count) :
    gctrl.draw_string("Score : " + str(count), STATUS_XOFFSET, STATUS_YOFFSET, ALIGN_LEFT)

def game_over() :
    gctrl.draw_string("Game Over", 0, 0, ALIGN_CENTER, 80, COLOR_RED)

    pygame.display.update()
    sleep(2)
    run_game()

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global background
    global snd_explosion

    start_game()

    score_count = 0

    # aircraft
    aircraft = aircraft_object(0, 0, 'id_aircraft')
    aircraft.init_position()
    aircraft.set_life_count(3)

    bullets = bulles_group()

    # enemy
    enemy = enemy_object(0, 0, 'id_enemy', ENEMY_SPEED)
    enemy.init_position()
    enemy.set_life_count(1)

    fires = fires_group()
    fire = fires.get_fire()

    boom = None

    crashed = False
    while not crashed :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                crashed = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP:
                    aircraft.set_speed(0, -1 * AIRCRAFT_SPEED)
                elif event.key == pygame.K_DOWN :
                    aircraft.set_speed(0, AIRCRAFT_SPEED)
                elif event.key == pygame.K_SPACE :
                    bullet_x = aircraft.ex
                    bullet_y = aircraft.y + aircraft.height / 2
                    bullets.add(bullet_x, bullet_y)
                elif event.key == pygame.K_F10 :
                    gctrl.save_scr_capture(TITLE_STR)

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                    aircraft.set_speed(0, 0)

        # Update aircraft
        aircraft.move()

        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)

        # Draw background
        background.scroll()
        background.draw()

        draw_life(aircraft.get_life_count())
        draw_score(score_count)

        if aircraft.is_life() == False :
            game_over()

        # Draw enemy
        enemy.move(ENEMY_SPEED, 0)
        if enemy.is_out_of_range() == True :
            enemy.init_position()

        if enemy.is_life() == True :
            enemy.draw()
        else :
            if boom == None :
                boom = boom_object(enemy.x, enemy.y, 'id_boom')

            if enemy.kill_time() == False :
                enemy.init_position()
                enemy.set_life_count(1)

        # Draw fireball
        fire.move()

        if fire.is_out_of_range() == True :
            fire = fires.get_fire()

        # Draw bullet
        if bullets.move(enemy) == True :
            enemy.kill_life()
            score_count += SCORE_UNIT

        bullets.draw()

        # Check crash
        if aircraft.check_crash(enemy, snd_explosion) == True :
            enemy.init_position()
            aircraft.kill_life()
            boom = boom_object(aircraft.ex, aircraft.y, 'id_boom')
          
        if aircraft.check_crash(fire, snd_explosion) == True :
            boom = boom_object(aircraft.ex, aircraft.y, 'id_boom')

        aircraft.draw()
        fire.draw()
        
        if boom != None :
            if boom.draw() == False :
                boom = None

        pygame.display.update()
        gctrl.clock.tick(FPS)
        
    terminate()

def start_game() :
    # Clear gamepad
    gctrl.surface.fill(COLOR_WHITE)

    title_bg = pygame.image.load(get_img_resource('id_title_bg'))
    rect = pygame.Rect(0, 0, gctrl.width, gctrl.height)
    gctrl.surface.blit(title_bg, rect)

    title = pygame.image.load(get_img_resource('id_title'))
    rect = title.get_rect()
    rect.center = ((gctrl.width / 2), (gctrl.height / 2))
    rect.top = rect.top - 40
    gctrl.surface.blit(title, rect)

    gctrl.draw_string("Press any key", 0, 100, ALIGN_CENTER | ALIGN_BOTTOM, 40, COLOR_RED)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        gctrl.clock.tick(FPS)    
       
def init_game() :
    global background
    global snd_explosion
   
    # backgroud and screen
    background = backgroud_object('id_background')
    pad_width = background.width
    pad_height = background.height

    gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
    pygame.display.set_caption(TITLE_STR)

    # sound resource
    snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))

if __name__ == '__main__' :
    init_game()
    run_game()

