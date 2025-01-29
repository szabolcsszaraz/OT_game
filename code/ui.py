from settings import *

class UI:
    def __init__(self):
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 20)

        #bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 31, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        #convert weapon dic
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        #convert
        ratio = current / max
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_coin(self, exp):
        text_surf = self.font.render('coins: ' + str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_width() - 20
        y = self.display_surface.get_height() - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index):
        gb_rect = self.selection_box(10, 630)
        weapon = self.weapon_graphics[weapon_index]
        weapon_surf = pygame.transform.scale(weapon, (20,40))
        weapon_rect = weapon_surf.get_rect(center = gb_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index,):
        gb_rect = self.selection_box(80, 635)
        magic = self.magic_graphics[magic_index]
        magic_surf = pygame.transform.scale(magic, (20, 40))
        magic_rect = magic_surf.get_rect(center=gb_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)
    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_coin(player.exp)
        self.weapon_overlay(player.weapon_index)

        self.magic_overlay(player.magic_index)
