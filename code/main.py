from settings import *
from player import Player
from sprites import CollisionSprites, Sprite
from groups import AllSprites
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import Magic
from random import randint


class Game:
    def __init__(self):
        # Setup
        pygame.init()

        # Virtuális felbontás és valódi képernyő felbontása
        self.virtual_width = WINDOW_WIDTH
        self.virtual_height = WINDOW_HEIGHT
        self.window_width = 1080  # Nagyobb ablakméret (változtatható)
        self.window_height = 720

        # Képernyő inicializálása
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Szabi')

        # Virtuális felület
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))

        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = AllSprites(self.virtual_surface)
        self.collision_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()

        # Setup
        self.setup()
        self.ui = UI()

        # Attack
        self.current_weapon = None


    def setup(self):
        map = load_pygame(join('data', 'maps', 'basic.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Objects'):
            # Az objektum méretének átméretezése
            scaled_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))

            # CollisionSprites létrehozása a megfelelő méretű képpel
            CollisionSprites((obj.x, obj.y), scaled_image, (self.all_sprites, self.collision_sprites))

        for x,y,image in map.get_layer_by_name('Plants and rocks').tiles():
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
            elif mark.name == 'Enemy':
                Enemy('bamboo', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)
            elif mark.name == 'Boss':
                Enemy('boss1', (mark.x, mark.y), [self.all_sprites, self.attackable_sprites], self.collision_sprites, self.damage_player, self.trigger_death_anim, self.coin_sprites)

    def create_attack(self):
        self.current_weapon = Weapon(self.player, [self.all_sprites, self.attack_sprites])

    def player_attack(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
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

    def trigger_death_anim(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.all_sprites)

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.all_sprites])
        if style == 'fire':
            self.magic_player.flame(self.player, cost, [self.all_sprites, self.attack_sprites])
    def killWeapon(self):
        if self.current_weapon:
            self.current_weapon.kill()
        self.current_weapon = None
    def run(self):
        while self.running:
            # Delta time
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update
            self.all_sprites.update(dt)
            self.all_sprites.enemy_update(self.player)
            self.player_attack()


            # Virtuális képernyőre rajzolás
            self.virtual_surface.fill('grey')
            self.all_sprites.draw(self.player.rect.center)

            # for sprite in self.all_sprites:
            #     if hasattr(sprite, 'sprite_type'):
            #         # Hozz létre egy másolatot a hitbox-ról és alkalmazd az offset-et
            #         offset_hitbox = sprite.hitbox.move(self.all_sprites.offset)
            #         pygame.draw.rect(self.virtual_surface, (255, 0, 0), offset_hitbox, 2)

            # Virtuális képernyő felskálázása a valódi képernyőre
            scaled_surface = pygame.transform.scale(self.virtual_surface, (self.window_width, self.window_height))
            self.display_surface.blit(scaled_surface, (0, 0))
            self.ui.display(self.player)

            #particles
            self.animation_player = AnimationPlayer()
            self.magic_player = Magic(self.animation_player)

            # Frissítés
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()