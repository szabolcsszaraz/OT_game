from settings import *
from player import Player
from sprites import CollisionSprites, Sprite
from groups import AllSprites
from weapon import Weapon
from ui import UI
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
                                     self.create_magic)

    def create_attack(self):
        self.current_weapon = Weapon(self.player, self.all_sprites)

    def create_magic(self, style, strength, cost):
        print(style, strength, cost)
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


            # Virtuális képernyőre rajzolás
            self.virtual_surface.fill('grey')
            self.all_sprites.draw(self.player.rect.center)

            # Virtuális képernyő felskálázása a valódi képernyőre
            scaled_surface = pygame.transform.scale(self.virtual_surface, (self.window_width, self.window_height))
            self.display_surface.blit(scaled_surface, (0, 0))
            self.ui.display(self.player)

            # Frissítés
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()