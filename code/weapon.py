from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.getState()
        self.sprite_type = 'weapon'

        #graphic
        full_path = f'images/weapon/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.Vector2(0, 5))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.Vector2(0, 5))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.Vector2(-1, 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.Vector2(-2, 1))
        self.hitbox = self.rect