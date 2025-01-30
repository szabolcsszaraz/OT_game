from settings import *
from random import randint

class Magic:
    def __init__(self, animation_player):
        self.sounds = {
            'heal': pygame.mixer.Sound('audio/attack/magic.wav'),
            'fire': pygame.mixer.Sound('audio/attack/fire.wav')
        }
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            self.sounds['heal'].set_volume(0.2)
            player.health += strength
            player.energy -= cost
            if player.health >= player.max_health:
                player.health = player.max_health
            self.animation_player.create_particles('heal', player.rect.center, groups)


    def flame(self, player, cost, groups):
        direction = player.getState()
        if player.energy >= cost:
            self.sounds['fire'].play()
            self.sounds['fire'].set_volume(0.2)
            # player.energy -= cost

            if direction == 'right':
                dir = pygame.Vector2(1,0)
            elif direction == 'left':
                dir = pygame.Vector2(-1,0)
            elif direction == 'up':
                dir = pygame.Vector2(0,-1)
            else:
                dir = pygame.Vector2(0,1)

            for i in range(1,6):
                if dir.x:
                    offset_x = (dir.x * i) * TILE_SIZE
                    x = player.rect.centerx + offset_x + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles('fire', (x, y), groups)
                else:
                    offset_y = (dir.y * i) * TILE_SIZE
                    x = player.rect.centerx + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILE_SIZE // 3, TILE_SIZE // 3)
                    self.animation_player.create_particles('fire', (x, y), groups)

