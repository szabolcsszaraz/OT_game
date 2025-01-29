from settings import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, collision, create_attack, killWeapon, create_magic):
        super().__init__(groups)
        self.load_images()
        self.state = 'down'
        self.image = pygame.image.load(join('images', 'player', 'down', '1.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(0, -14)
        self.pos = pygame.Vector2(self.rect.center)

        #movement
        self.collision_sprites = collision

        #attack
        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None

        #weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.killWeapon = killWeapon

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]


        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 60}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']
    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': [],
                       'left_attack': [], 'right_attack': [], 'up_attack': [], 'down_attack': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_button = pygame.mouse.get_pressed()
        if not self.attacking:
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            self.direction = self.direction.normalize() if self.direction else self.direction

            #attack
            if mouse_button[0]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if mouse_button[2]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.killWeapon()

    def getState(self):
        return self.state.split('_')[0]
    def animate(self, dt):
        #get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.state:
                self.state = self.state + '_attack'
        else:
            if 'attack' in self.state:
                self.state = self.state.replace('_attack', '')

        #animate
        self.frame_index += self.animation_speed * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.cooldowns()
