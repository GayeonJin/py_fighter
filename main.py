#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gobject import *
from gresource import *

SCORE_UNIT = 10

AIRCRAFT_SPEED = 5
BULLET_SPEED = 15
ENEMY_SPEED = -7
FIRE_SPEED = -15
NOFIRE_SPEED = -30

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)

def draw_life(count) :
    font = pygame.font.SysFont(None, 25)
    text = font.render("Life : " + str(count), True, COLOR_WHITE)
    gctrl.gamepad.blit(text, (gctrl.pad_width - 100, 0))

def draw_score(count) :
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score : " + str(count), True, COLOR_WHITE)
    gctrl.gamepad.blit(text, (10, 0))

def game_over() :
    font = pygame.font.Font('freesansbold.ttf', 80)
    text_suf = font.render('Game Over', True, COLOR_RED)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))

    gctrl.gamepad.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)
    run_game()

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global clock
    global background, aircraft, enemy, fires, boom
    global snd_shot, snd_explosion

    start_game()

    boom_count = 0
    score_count = 0

    bullets = []

    aircraft.init_position(INIT_POS_LEFT)
    aircraft.set_life_count(3)
    y_change = 0

    enemy.init_position(INIT_POS_RIGHT)
    enemy.set_life_count(1)

    random.shuffle(fires)
    fire = fires[0]
    fire.init_position(INIT_POS_RIGHT)

    crashed = False
    while not crashed :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                crashed = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP:
                    y_change = -1 * AIRCRAFT_SPEED
                elif event.key == pygame.K_DOWN :
                    y_change = AIRCRAFT_SPEED
                elif event.key == pygame.K_SPACE :
                    bullet_x = aircraft.ex
                    bullet_y = aircraft.y + aircraft.height / 2
                    bullets.append(game_object(bullet_x, bullet_y, 'id_bullet'))
                elif event.key == pygame.K_SPACE :
                    sleep(5)

            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                    y_change = 0

        aircraft.move(0, y_change)

        # Clear gamepad
        gctrl.gamepad.fill(COLOR_WHITE)

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
            enemy.init_position(INIT_POS_RIGHT)

        if enemy.is_life() == True :
            enemy.draw()
        else :
            boom.set_position(enemy.x, enemy.y)
            boom.draw()
            boom_count += 1
            if boom_count > 5 :
                boom_count = 0
                enemy.init_position(INIT_POS_RIGHT)
                enemy.set_life_count(1)

        # Draw fireball
        if fire.object == None :
            fire.move(NOFIRE_SPEED, 0)
        else :
            fire.move(FIRE_SPEED, 0)

        if fire.is_out_of_range() == True :
            random.shuffle(fires)
            fire = fires[0]
            fire.init_position(INIT_POS_RIGHT)

        # Draw bullet
        if len(bullets) != 0 :
            for i, bullet in enumerate(bullets) :
                bullet.move(BULLET_SPEED, 0)

                if bullet.check_crash(enemy, snd_shot) == True :
                    bullets.remove(bullet)
                    enemy.kill_life()
                    score_count += SCORE_UNIT

                if bullet.is_out_of_range() == True :
                    try :
                        bullets.remove(bullet)
                    except :
                        pass

        if len(bullets) != 0 :
            for i, bullet in enumerate(bullets) :
                bullet.draw()

        # Check crash
        if aircraft.check_crash(enemy, snd_explosion) == True :
            enemy.init_position(INIT_POS_RIGHT)
            aircraft.kill_life()
            boom.set_position(aircraft.ex, aircraft.y)
            boom.draw()
          
        if aircraft.check_crash(fire, snd_explosion) == True :
            boom.set_position(aircraft.ex, aircraft.y)
            boom.draw()

        aircraft.draw()
        fire.draw()

        pygame.display.update()
        clock.tick(60)
        
    terminate()

def start_game() :
    # Clear gamepad
    gctrl.gamepad.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 80)
    text_suf = font.render("Py Fighter", True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((gctrl.pad_width / 2), (gctrl.pad_height / 2))
    gctrl.gamepad.blit(text_suf, text_rect)

    font1 = pygame.font.SysFont(None, 25)
    text_suf1 = font1.render("press any key", True, COLOR_RED)
    text_rect1 = text_suf1.get_rect()
    text_rect1.top = text_rect.bottom + 50
    text_rect1.centerx = gctrl.pad_width / 2
    gctrl.gamepad.blit(text_suf1, text_rect1)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        clock.tick(60)    
       
def init_game() :
    global clock
    global background, aircraft, enemy, fires, boom
    global snd_shot, snd_explosion

    fires = []

    # initialize
    pygame.init()
    clock = pygame.time.Clock()
    
    # backgroud and screen
    background = backgroud_object('id_background')
    pad_width = background.width
    pad_height = background.height

    gctrl.set_param(pygame.display.set_mode((pad_width, pad_height)), pad_width, pad_height)
    pygame.display.set_caption("Py Fighter")

    # sound resource
    snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
    snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))

    # aircraft
    aircraft = game_object(0, 0, 'id_aircraft')

    # enemy
    enemy = game_object(pad_width, random.randrange(0, pad_height), 'id_enemy')

    fires.append(game_object(0, 0, 'id_fire1'))
    fires.append(game_object(0, 0, 'id_fire2'))

    for i in range(3) :
        fires.append(game_object(0, 0, None))

    # effect
    boom = game_object(0, 0, 'id_boom')

if __name__ == '__main__' :
    init_game()
    run_game()

