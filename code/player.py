from settings import *
from entity import Entity
from pickups import Coin, Health, MagicPickup

class Player(Entity):
    def __init__(self, pos, groups, collision, create_attack, killWeapon, create_magic, coin_sprites):
        super().__init__(groups)
        self.load_images()
        self.sprite_type = 'player'
        self.state = 'down'
        self.image = pygame.image.load(join('images', 'player', 'down', '1.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox = self.rect.inflate(0, -14)
        self.pos = pygame.Vector2(self.rect.center)

        #movement
        self.collision_sprites = collision

        #attack
        self.attacking = False
        self.attack_cooldown = 800
        self.attack_time = None

        #weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.available_weapons = ['sword']
        self.killWeapon = killWeapon

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.available_magics = {'fire': 3, 'heal': 1}
        self.magic_switch_cooldown = 200
        self.last_magic_switch_time = 0


        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 120}
        self.max_health = self.stats['health']
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.coins = 0
        self.speed = self.stats['speed']

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_dur = 500

        #coin
        self.coin_sprites = coin_sprites

        #import sound
        self.weapon_sound = pygame.mixer.Sound('audio/attack/Sword.wav')
        self.weapon_sound.set_volume(0.2)
        self.coin_sound = pygame.mixer.Sound('audio/Coin.wav')
        self.coin_sound.set_volume(0.2)
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
        current_time = pygame.time.get_ticks()
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
                self.weapon_sound.play()

            if mouse_button[2]:
                if self.magic is not None:  # Only if magic available
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = self.magic
                    strength = magic_data[style]['strength'] + self.stats['magic']
                    cost = magic_data[style]['cost']

                    if self.try_use_magic(style, strength, cost):
                        self.attacking = True
                    else:
                        self.attacking = False
                else:
                    self.attacking = False

            if keys[pygame.K_q]:
                self.weapon_index = (self.weapon_index + 1) % len(self.available_weapons)
                self.weapon = self.available_weapons[self.weapon_index]

            if keys[pygame.K_e]:
                if current_time - self.last_magic_switch_time > self.magic_switch_cooldown:
                    self.last_magic_switch_time = current_time
                    all_magics = list(self.available_magics.keys())

                    if all_magics:
                        try:
                            current_idx = all_magics.index(self.magic)
                            new_idx = (current_idx + 1) % len(all_magics)
                        except ValueError:
                            new_idx = 0

                        self.magic = all_magics[new_idx]
                        self.magic_index = new_idx
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.killWeapon()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_dur:
                self.vulnerable = True
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

        #flicker
        if not self.vulnerable:
            alpha = self.waveVal()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    def getFullWeaponDamage(self):
        baseDamage = self.stats['attack']
        weaponDamage = weapon_data[self.weapon]['damage']

        return baseDamage + weaponDamage

    def getFullMagicDamage(self):
        if self.magic is None:
            return 0  # default value

        baseDamage = self.stats['magic']
        spellDamage = magic_data[self.magic]['strength']

        return baseDamage + spellDamage

    def stamina(self, dt):
        if self.energy < self.stats['energy']:
            self.energy += 1 * dt
        else:
            self.energy = self.stats['energy']

    def collect_pickups(self, dt):
        collided_pickups = pygame.sprite.spritecollide(
            self,
            self.coin_sprites,
            True,
            pygame.sprite.collide_rect
        )

        for pickup in collided_pickups:
            if isinstance(pickup, Coin):
                self.coins += pickup.value
                self.coin_sound.play()
            elif isinstance(pickup, Health):
                self.available_magics['heal'] += pickup.value
                self.coin_sound.play()
            elif isinstance(pickup, MagicPickup):
                self.available_magics['fire'] += pickup.value
                self.coin_sound.play()

    def try_use_magic(self, style, strength, cost):
        # Csak akkor engedj varázsolni, ha van töltés
        if self.available_magics.get(style, 0) > 0 and self.energy >= cost:
            self.available_magics[style] -= 1
            self.create_magic(style, strength, cost)
            return True
        return False

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.cooldowns()
        self.stamina(dt)
        self.collect_pickups(dt)
