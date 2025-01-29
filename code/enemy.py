
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, collision_sprite):
        # Eredeti inicializáció megtartása
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Grafika beállítása
        self.import_graphics(monster_name)
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]


        # Pozícionálás
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # Kisebb hitbox a jobb mozgásért
        self.collision_sprites = collision_sprite
        self.pos = pygame.Vector2(self.rect.center)

        # Monster adatok beállítása
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.coins = monster_info['coin']

    def import_graphics(self, monster_name):
        self.frames = {'idle': [], 'walk': [], 'attack': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', monster_name, state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def player_distance_direction(self, player):
        enemy_vec = pygame.Vector2(self.rect.center)
        player_vec = pygame.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.Vector2()

        return (distance, direction)


    def actions(self, player):
        if self.state == 'attack':
            print('attack')
        elif self.state == 'walk':
            self.direction = self.player_distance_direction(player)[1]
        else:
            self.direction = pygame.Vector2()

    def get_status(self, player):
        distance = self.player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.state = 'attack'
        elif distance <= self.notice_radius:
            self.state = 'walk'
        elif distance > self.notice_radius:
            self.state = 'idle'


    def update(self, dt):
        self.move(dt)


    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)  # CSAK A FRISSÍTÉS, NINCS UPDATE HIVÁS


