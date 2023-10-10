#!/usr/bin/python

import sys

resource_path = ''

resource_item = {
    'id_background' : 'image/background.png',
    'id_aircraft' : 'image/plane.png',
    'id_enemy' : 'image/enemy.png',
    'id_fire1' : 'image/fireball.png',
    'id_fire2' : 'image/fireball2.png',
    'id_bullet' : 'image/bullet.png',
    'id_boom' : 'image/boom.png'
}

def get_resource(resource_id) :
    return resource_path + resource_item[resource_id]

if __name__ == '__main__' :
    print('game resoure')