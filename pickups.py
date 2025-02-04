from settings import *
import random

class Health(pygame.sprite.Sprite):
    def __init__(self, pos, value, groups):
        super().__init__(groups)
        self.value = value
        self.image = pygame.image.load(join('images', 'magic_scroll', 'Medipack.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-6, -6)

class MagicPickup(pygame.sprite.Sprite):
    def __init__(self, pos, value, groups):
        super().__init__(groups)
        self.value = value
        self.image = pygame.image.load(join('images', 'heal_scroll', 'ScrollFire.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-6, -6)

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, value, groups):
        super().__init__(groups)
        self.value = value

        # Animation
        self.frames = self.import_folder('images/coin')
        self.frame_index = 0
        self.animation_speed = 6

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-6, -6)

    @staticmethod
    def import_folder(path):
        surface_list = []
        for folder_path, _, img_files in walk(path):
            img_files = sorted(img_files, key=lambda x: int(x.split('.')[0]))
            for image in img_files:
                full_path = join(folder_path, image)
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)