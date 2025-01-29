import pygame
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 320, 240
TILE_SIZE = 16

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'images/weapon/sword/full.png'}
}

magic_data = {
    'fire': {'strength': 20, 'cost': 20, 'graphic': 'images/particles/fire/2.png'}
}

monster_data = {
    'bamboo': {
        'health': 100,
        'coin': 10,
        'damage': 20,
        'attack_type': 'claw',
        'attack_sound': 'audio/attack/claw.wav',
        'speed': 30,  # Próbáld ezt az értéket
        'resistance': 3,
        'attack_radius': 16,
        'notice_radius': 64
    },
    'boss1': {
        'health': 100,
        'coin': 10,
        'damage': 20,
        'attack_type': 'claw',
        'attack_sound': 'audio/attack/claw.wav',
        'speed': 30,
        'resistance': 3,
        'attack_radius': 16,
        'notice_radius': 64}
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