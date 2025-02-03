import sys

from settings import *
from player import Player
from sprites import CollisionSprites, Sprite
from groups import AllSprites
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import Magic
from menu import Menu


class Game:
    def __init__(self):
        # Setup
        pygame.init()

        # Virtuálne rozlíšenie a skutočné rozlíšenie obrazovky
        self.virtual_width = WINDOW_WIDTH
        self.virtual_height = WINDOW_HEIGHT
        self.window_width = 1080
        self.window_height = 720

        # Inicializácia obrazovky
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Arcane Trials 🏹')

        # Virtuálne rozhranie
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = 'menu'

        # Inicializácia menu
        self.menu = Menu(self)

        # Inicializácia hry
        self.init_game()

        #music
        pygame.mixer.init()
        self.load_music()


    def init_game(self):
        # Groups
        self.all_sprites = AllSprites(self.virtual_surface)
        self.collision_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()

        # Setup
        self.setup()
        self.ui = UI(self.virtual_surface)

        # attack
        self.current_weapon = None

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = Magic(self.animation_player)



    def start_game(self):
        self.current_state = 'playing'
        pygame.mixer.music.play(-1)
        self.init_game()  # Spustenie novej hry
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Objects'):
            # Zmena veľkosti objektu
            scaled_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))

            # Vytvorenie CollisionSprites so správnou veľkosťou obrazu
            CollisionSprites((obj.x, obj.y), scaled_image, (self.all_sprites, self.collision_sprites))

        for x,y,image in map.get_layer_by_name('Buildings').tiles():
            CollisionSprites((x*TILE_SIZE, y*TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.collision_sprites))

        for mark in map.get_layer_by_name('Entities'):
            if mark.name == 'Player':
                self.player = Player((mark.x, mark.y),
                                     self.all_sprites,
                                     self.collision_sprites,
                                     self.create_attack,
                                     self.killWeapon,
                                     self.create_magic,
                                     self.coin_sprites)
            elif mark.name == 'Bamboo':
                Enemy('bamboo', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Boss':
                Enemy('boss1', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Beast':
                Enemy('beast', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Flame':
                Enemy('flame', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Mushroom':
                Enemy('mushroom', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Knight':
                Enemy('knight', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Gladiator':
                Enemy('gladiator', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Skeleton':
                Enemy('skeleton', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Skeletondemon':
                Enemy('skeletondemon', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)

    def create_attack(self):
        self.current_weapon = Weapon(self.player, [self.all_sprites, self.attack_sprites])

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite,
                    self.attackable_sprites,
                    False,
                    pygame.sprite.collide_mask  # Pixel-perfect collision
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.getDamage(self.player, attack_sprite.sprite_type)


    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,self.all_sprites)
            hit_sound = pygame.mixer.Sound(f'audio/attack/{attack_type}.wav')
            hit_sound.set_volume(0.2)
            hit_sound.play()

    def trigger_death_anim(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.all_sprites)

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.all_sprites])
        elif style == 'fire':
            self.magic_player.flame(self.player, cost, [self.all_sprites, self.attack_sprites])
    def killWeapon(self):
        if self.current_weapon:
            self.current_weapon.kill()
        self.current_weapon = None

    def handle_death(self):
        self.current_state = 'menu'
        self.ui.display_death()
        pygame.display.update()
        pygame.time.wait(2000)

    def load_music(self):
        try:
            pygame.mixer.music.load('audio/Chill.ogg')
            pygame.mixer.music.set_volume(0.1)
        except Exception as e:
            print(f"Error: {e}")

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.menu.handle_event(event)

            # Aktualizácie stavu
            if self.current_state == 'playing':
                self.all_sprites.update(dt)
                self.all_sprites.enemy_update(self.player)
                self.player_attack()

                if self.player.health <= 0:
                    self.handle_death()

            # Vykreslenie
            self.virtual_surface.fill('grey')

            if self.current_state == 'playing':
                self.all_sprites.draw(self.player.rect.center)
                self.ui.display(self.player)

            self.menu.draw()

            # Scale to window
            scaled_surface = pygame.transform.scale(self.virtual_surface,
                                                    (self.window_width, self.window_height))
            self.display_surface.blit(scaled_surface, (0, 0))
            pygame.display.update()


        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()