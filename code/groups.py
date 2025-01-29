from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, display_surface):
        super().__init__()
        self.display_surface = display_surface
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - (self.display_surface.get_width()/2))
        self.offset.y = -(target_pos[1] - (self.display_surface.get_height() / 2))

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
