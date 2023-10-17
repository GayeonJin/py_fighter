#!/usr/bin/python

import sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)

resource_path = ''

resource_image = {
    'id_background' : 'image/background.png',
    'id_aircraft' : 'image/plane.png',
    'id_enemy' : 'image/enemy.png',
    'id_fire1' : 'image/fireball.png',
    'id_fire2' : 'image/fireball2.png',
    'id_bullet' : 'image/bullet.png',
    'id_boom' : 'image/boom.png'
}

resource_sound = {
    'snd_shot' : 'sound/shot.wav',
    'snd_explosion' : 'sound/explosion.wav'
}

def get_img_resource(resource_id) :
    return resource_path + resource_image[resource_id]

def get_snd_resource(resource_id) :
    return resource_path + resource_sound[resource_id]

if __name__ == '__main__' :
    print('game resoure')