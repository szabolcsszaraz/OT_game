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
HP_BAR_BORDER_COLOR = (40, 40, 40)  # Sötét szürke keret
HP_BAR_BORDER_SIZE = 1

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 35, 'graphic': 'images/weapon/sword/full.png'}
}

magic_data = {
    'fire': {'strength': 10, 'cost': 20, 'graphic': 'images/particles/fire/2.png'},
    'heal': {'strength': 20, 'cost': 30, 'graphic': 'images/particles/heal/3.png'}
}

monster_data = {
    'bamboo': {
        'health': 100,
        'coin': 10,
        'damage': 20,
        'attack_type': 'cut',
        'speed': 30,  # Próbáld ezt az értéket
        'resistance': 5,
        'attack_radius': 16,
        'notice_radius': 120
    },
    'boss1': {
        'health': 400,
        'coin': 100,
        'damage': 50,
        'attack_type': 'slashdouble',
        'speed': 30,
        'resistance': 2,
        'attack_radius': 32,
        'notice_radius': 100,
        'loot_chances': {
            'coin': 0.7,
            'health': 0.2,
            'magic': 0.1
        }
    }
}

#ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80

#colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'