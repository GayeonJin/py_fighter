#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

INIT_POS_LEFT = 0
INIT_POS_RIGHT = 1

SCORE_UNIT = 10

AIRCRAFT_SPEED = 5
BULLET_SPEED = 15
ENEMY_SPEED = -7
FIRE_SPEED = -15
NOFIRE_SPEED = -30

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)

pad_width = 0
pad_height = 0

main_path = ''

resource = {
    'id_background' : 'image/background.png',
    'id_aircraft' : 'image/plane.png',
    'id_enemy' : 'image/enemy.png',
    'id_fire1' : 'image/fireball.png',
    'id_fire2' : 'image/fireball2.png',
    'id_bullet' : 'image/bullet.png',
    'id_boom' : 'image/boom.png'
}

class game_object :
    global gamepad

    def __init__(self, x, y, resource_id) :
        if resource_id != None :
            resource_path = main_path + resource[resource_id]
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width()
            self.height = self.object.get_height()
        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.set_position(x, y)

        self.life_count = 1

    def init_position(self, mode) :
        if mode == INIT_POS_LEFT :
            self.set_position(pad_width * 0.05, pad_height / 2)
        elif mode == INIT_POS_RIGHT :
            self.set_position(pad_width, random.randrange(0, pad_height - self.height))

    def set_position(self, x, y) : 
        self.x = x
        self.y = y        
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1
        
    def move(self, del_x, del_y) :
        self.x += del_x
        self.y += del_y

        if self.y < 0 :
            self.y = 0
        elif self.y > (pad_height - self.height) :
            self.y = (pad_height - self.height)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gamepad.blit(self.object, (self.x, self.y))            

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= pad_width :
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
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy_item) :
        if self.object != None and enemy_item.object != None :
            if self.ex > enemy_item.x :
                if (self.y > enemy_item.y and self.y < enemy_item.ey) or (self.ey > enemy_item.y and self.ey < enemy_item.ey) :
                    #print("crashed1 : ",  self.x, self.y, self.ex, self.ey)
                    #print("crashed2 : ",  enemy_item.x, enemy_item.y, enemy_item.ex, enemy_item.ey)
                    return True
        return False

class backgroud_object(game_object) :
    def __init__(self, resource_id) :
        resource_path = main_path + resource[resource_id]
        self.object = pygame.image.load(resource_path)
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
        gamepad.blit(self.object, (self.x, 0))
        gamepad.blit(self.object2, (self.x2, 0))

def draw_life(count) :
    global gamepad

    font = pygame.font.SysFont(None, 25)
    text = font.render("Life : " + str(count), True, COLOR_WHITE)
    gamepad.blit(text, (pad_width - 100, 0))

def draw_score(count) :
    global gamepad

    font = pygame.font.SysFont(None, 25)
    text = font.render("Score : " + str(count), True, COLOR_WHITE)
    gamepad.blit(text, (10, 0))

def game_over() :
    global gamepad

    font = pygame.font.Font('freesansbold.ttf', 80)
    text_suf = font.render('Game Over', True, COLOR_RED)
    text_rect = text_suf.get_rect()
    text_rect.center = ((pad_width / 2), (pad_height / 2))

    gamepad.blit(text_suf, text_rect)
    pygame.display.update()
    sleep(2)
    run_game()

def terminate() :
    pygame.quit()
    sys.exit()

def run_game() :
    global gamepad, pad_width, pad_height, clock
    global background, aircraft, enemy, fires, boom

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
                elif event.key == pygame.K_z :
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
        gamepad.fill(COLOR_WHITE)

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

                if bullet.check_crash(enemy) == True :
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
        if aircraft.check_crash(enemy) == True :
            enemy.init_position(INIT_POS_RIGHT)
            aircraft.kill_life()
            boom.set_position(aircraft.ex, aircraft.y)
            boom.draw()
          
        if aircraft.check_crash(fire) == True :
            boom.set_position(aircraft.ex, aircraft.y)
            boom.draw()

        aircraft.draw()
        fire.draw()

        pygame.display.update()
        clock.tick(60)
        
    terminate()

def start_game() :
    global gamepad

    # Clear gamepad
    gamepad.fill(COLOR_WHITE)

    font = pygame.font.Font('freesansbold.ttf', 80)
    text_suf = font.render("Py Fighter", True, COLOR_BLACK)
    text_rect = text_suf.get_rect()
    text_rect.center = ((pad_width / 2), (pad_height / 2))
    gamepad.blit(text_suf, text_rect)

    font1 = pygame.font.SysFont(None, 25)
    text_suf1 = font1.render("press any key", True, COLOR_RED)
    text_rect1 = text_suf1.get_rect()
    text_rect1.top = text_rect.bottom + 50
    text_rect1.centerx = pad_width / 2
    gamepad.blit(text_suf1, text_rect1)

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
    global gamepad, pad_width, pad_height, clock
    global background, aircraft, enemy, fires, boom

    fires = []

    pygame.init()
    clock = pygame.time.Clock()
    
    background = backgroud_object('id_background')
    pad_width = background.width
    pad_height = background.height

    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption("Py Fighter")

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

