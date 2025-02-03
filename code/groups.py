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

        enemies = [sprite for sprite in self.sprites() if
                   hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemies:
            if enemy.health > 0:
                # Výpočet polohy
                hp_bar_x = enemy.rect.centerx - HP_BAR_WIDTH // 2
                hp_bar_y = enemy.rect.top - HP_BAR_OFFSET
                offset_pos = pygame.Vector2(hp_bar_x, hp_bar_y) + self.offset

                # Kreslenie rámu
                pygame.draw.rect(self.display_surface, HP_BAR_BORDER_COLOR,
                                 (offset_pos.x - HP_BAR_BORDER_SIZE,
                                  offset_pos.y - HP_BAR_BORDER_SIZE,
                                  HP_BAR_WIDTH + HP_BAR_BORDER_SIZE * 2,
                                  HP_BAR_HEIGHT + HP_BAR_BORDER_SIZE * 2))

                # Pozadie
                pygame.draw.rect(self.display_surface, (255, 0, 0),
                                 (offset_pos.x, offset_pos.y, HP_BAR_WIDTH, HP_BAR_HEIGHT))

                # Súčasná hp
                current_hp_width = (enemy.health / enemy.max_health) * HP_BAR_WIDTH
                pygame.draw.rect(self.display_surface, (0, 255, 0),
                                 (offset_pos.x, offset_pos.y, current_hp_width, HP_BAR_HEIGHT))

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
