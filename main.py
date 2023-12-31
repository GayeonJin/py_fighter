#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gobject import *
from gresource import *
from stage import *

TITLE_STR = "Py Fighter"

class player :
    SCORE_UNIT = 10

    STATUS_XOFFSET = 10
    STATUS_YOFFSET = 5

    def __init__(self) :
        self.life = 3
        self.score = 0

    def update_life(self, life) :
        self.life = life

    def update_score(self) :
        self.score += player.SCORE_UNIT

    def draw_life(self) :
        gctrl.draw_string("Life : " + str(self.life), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_RIGHT)

    def draw_score(self) :
        gctrl.draw_string("Score : " + str(self.score), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_LEFT)

class fighter_game :
    def __init__(self) :  
        # backgroud and screen
        self.background = backgroud_object()
        pad_width = self.background.width
        pad_height = self.background.height

        gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
        pygame.display.set_caption(TITLE_STR)

    def game_over(self) :
        gctrl.draw_string("Game Over", 0, 0, ALIGN_CENTER, 80, COLOR_RED)

        pygame.display.update()
        sleep(2)
        self.run_game()

    def terminate(self) :
        pygame.quit()
        sys.exit()

    def run(self) :
        self.start_game()

        # sound resource
        snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))

        # player
        game_player = player() 

        # aircraft
        aircraft = aircraft_object(0, 0, 'id_aircraft')
        bullets = bulles_group()

        # enemy
        enemy = enemy_object(0, 0, ('id_enemy', ENEMY_SPEED, CRASH_TYPE_LIFE))

        fires_res = fires_resource()
        fire = enemy_object(0, 0, fires_res.get_info())

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

            # Clear gamepad
            gctrl.surface.fill(COLOR_WHITE)

            # Draw background
            self.background.scroll()
            self.background.draw()

            game_player.draw_life()
            game_player.draw_score()

            # Draw enemy
            enemy.move()
            enemy.draw()

            # Draw fireball
            if fire.move() == enemy_object.OFF_COURSE :
                fire = enemy_object(0, 0, fires_res.get_info())
            fire.draw()

            # Draw bullet
            if bullets.move(enemy) == bulles_group.SHOT_ENEMY :
                game_player.update_score()

            bullets.draw()

            # Update aircraft
            aircraft.move()

            # Check crash
            aircraft.check_crash(enemy, snd_explosion)
            aircraft.check_crash(fire, snd_explosion)
            aircraft.draw()

            game_player.update_life(aircraft.get_life_count())
            if game_player.life == 0 :
                self.game_over()

            pygame.display.update()
            gctrl.clock.tick(FPS)
            
        self.terminate()

    def start_game(self) :
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
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    return

            pygame.display.update()
            gctrl.clock.tick(FPS)
       
if __name__ == '__main__' :
    game = fighter_game()
    game.run()

