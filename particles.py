from os import walk
from settings import *

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'fire': self.import_folder('images/particles/fire'),
            'heal': self.import_folder('images/particles/heal'),
            # attack
            'cut': self.import_folder('images/particles/cut'),
            'slashdouble': self.import_folder('images/particles/slashdouble'),
            # enemy death
            'bamboo': self.import_folder('images/particles/bamboo'),
            'boss1': self.import_folder('images/particles/boss1'),
            'beast': self.import_folder('images/particles/beast'),
            'flame': self.import_folder('images/particles/flame'),
            'mushroom': self.import_folder('images/particles/mushroom'),
            'knight': self.import_folder('images/particles/knight'),
            'gladiator': self.import_folder('images/particles/gladiator'),
            'skeleton': self.import_folder('images/particles/skeleton'),
            'skeletondemon': self.import_folder('images/particles/skeleton')
        }


    def create_particles(self, animation_type, pos, group):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, group)

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

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 6
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)