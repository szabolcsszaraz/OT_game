import pygame
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 320, 240
TILE_SIZE = 16

#enemy hp bar
HP_BAR_WIDTH = 20
HP_BAR_HEIGHT = 3
HP_BAR_OFFSET = 6
HP_BAR_BORDER_COLOR = (40, 40, 40)  # Tmavosivý rám
HP_BAR_BORDER_SIZE = 1

weapon_data = {
    'sword': {'cooldown': 300, 'damage': 35, 'graphic': 'images/weapon/sword/full.png'}
}

magic_data = {
    'fire': {'strength': 10, 'cost': 20, 'graphic': 'images/particles/fire/2.png'},
    'heal': {'strength': 25, 'cost': 30, 'graphic': 'images/particles/heal/3.png'}
}

monster_data = {
    'bamboo': {
        'health': 100,
        'coin': 10,
        'damage': 20,
        'attack_type': 'cut',
        'speed': 30,
        'resistance': 4,
        'attack_radius': 16,
        'notice_radius': 120
    },
    'beast': {
        'health': 140,
        'coin': 10,
        'damage': 25,
        'attack_type': 'cut',
        'speed': 25,
        'resistance': 3,
        'attack_radius': 20,
        'notice_radius': 80
    },
    'flame': {
        'health': 50,
        'coin': 10,
        'damage': 10,
        'attack_type': 'cut',
        'speed': 60,
        'resistance': 5,
        'attack_radius': 16,
        'notice_radius': 140
    },
    'mushroom': {
        'health': 90,
        'coin': 10,
        'damage': 15,
        'attack_type': 'cut',
        'speed': 0,
        'resistance': 0,
        'attack_radius': 16,
        'notice_radius': 50
    },
    'boss1': {
        'health': 400,
        'coin': 100,
        'damage': 50,
        'attack_type': 'slashdouble',
        'speed': 30,
        'resistance': 2,
        'attack_radius': 16,
        'notice_radius': 100,
    },
    'knight': {
        'health': 500,
        'coin': 100,
        'damage': 40,
        'attack_type': 'slashdouble',
        'speed': 32,
        'resistance': 2,
        'attack_radius': 16,
        'notice_radius': 120,
    },
    'gladiator': {
        'health': 450,
        'coin': 100,
        'damage': 45,
        'attack_type': 'slashdouble',
        'speed': 34,
        'resistance': 2,
        'attack_radius': 16,
        'notice_radius': 125,
    },
    'skeleton': {
        'health': 250,
        'coin': 100,
        'damage': 30,
        'attack_type': 'slashdouble',
        'speed': 38,
        'resistance': 2.5,
        'attack_radius': 16,
        'notice_radius': 110,
    },
    'skeletondemon': {
        'health': 350,
        'coin': 100,
        'damage': 40,
        'attack_type': 'slashdouble',
        'speed': 40,
        'resistance': 2.5,
        'attack_radius': 16,
        'notice_radius': 110,
    }
}

#ui
BAR_HEIGHT = 8
HEALTH_BAR_WIDTH = 80
ENERGY_BAR_WIDTH = 60
ITEM_BOX_SIZE = 30
UI_FONT = 'data/font/SourGummy_Expanded-ExtraLight.ttf'

#colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'