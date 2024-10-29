'''
Created on SEP 08, 2024

@author: APOORV
'''

import os

FPS = 100

SCREENSIZE = (640, 480)

Imagees = {
    'man': os.path.join(os.getcwd(), 'resources/images/man.png'),
    'grass': os.path.join(os.getcwd(), 'resources/images/grass.png'),
    'tree': os.path.join(os.getcwd(), 'resources/images/tree1.png'),
    'arrow': os.path.join(os.getcwd(), 'resources/images/bullet.png'),
    'badguy': os.path.join(os.getcwd(), 'resources/images/jcb1.png'),
    'healthbar': os.path.join(os.getcwd(), 'resources/images/healthbar.png'),
    'health': os.path.join(os.getcwd(), 'resources/images/health.png'),
    'gameover': os.path.join(os.getcwd(), 'resources/images/gameover.png'),
    'youwin': os.path.join(os.getcwd(), 'resources/images/youwin.png')
}

Sounds = {
    'hit': os.path.join(os.getcwd(), 'resources/audio/explode.wav'),
    'enemy': os.path.join(os.getcwd(), 'resources/audio/enemy.wav'),
    'shoot': os.path.join(os.getcwd(), 'resources/audio/shoot.wav'),
    'moonlight': os.path.join(os.getcwd(), 'resources/audio/moonlight.wav')
}






