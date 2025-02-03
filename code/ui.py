from settings import *

class UI:
    def __init__(self, virtual_surface):
        self.virtual_surface = virtual_surface
        self.font = pygame.font.Font(UI_FONT, 8)

        # Bar setup
        self.health_bar_rect = pygame.Rect(5, 3, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(5, 12, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Previesť slovník zbraní
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            weapon = pygame.transform.scale(weapon, (12, 20))
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            magic = pygame.transform.scale(magic, (12, 20))
            self.magic_graphics.append(magic)

    def show_bar(self, current, max, bg_rect, color):
        # Kreslenie pozadia
        pygame.draw.rect(self.virtual_surface, UI_BG_COLOR, bg_rect)

        # Výpočet aktuálnej hodnoty
        ratio = current / max
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Bar kreslenie
        pygame.draw.rect(self.virtual_surface, color, current_rect)
        pygame.draw.rect(self.virtual_surface, UI_BORDER_COLOR, bg_rect, 2)

    def show_coin(self, coins):
        # Zobraziť mince
        text_surf = self.font.render('Coins: ' + str(int(coins)), False, TEXT_COLOR)
        x = self.virtual_surface.get_width() - 10
        y = self.virtual_surface.get_height() - 10
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.virtual_surface, UI_BG_COLOR, text_rect.inflate(1, 1))
        self.virtual_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.virtual_surface, UI_BORDER_COLOR, text_rect.inflate(1, 1), 1)

    def selection_box(self, left, top):
        # Kreslenie výberového poľa
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.virtual_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.virtual_surface, UI_BORDER_COLOR, bg_rect, 2)
        return bg_rect

    def weapon_overlay(self, weapon_index):
        # Kreslenie ikony zbrane
        bg_rect = self.selection_box(5, self.virtual_surface.get_height() - 35)
        weapon = self.weapon_graphics[weapon_index]
        weapon_rect = weapon.get_rect(center=bg_rect.center)
        self.virtual_surface.blit(weapon, weapon_rect)

    def magic_overlay(self, magic_index, player):
        # Kreslenie ikony magie
        if not player.magic:
            return

        current_magic = player.magic
        count = player.available_magics.get(current_magic, 0)

        bg_rect = self.selection_box(29, self.virtual_surface.get_height() - 31)

        try:
            magic_idx = list(magic_data.keys()).index(current_magic)
            magic = self.magic_graphics[magic_idx]
        except ValueError:
            return

        magic_rect = magic.get_rect(center=bg_rect.center)
        self.virtual_surface.blit(magic, magic_rect)

        # Číslo množstva
        text_surf = self.font.render(str(count), True, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=bg_rect.bottomright - pygame.Vector2(2, 2))
        self.virtual_surface.blit(text_surf, text_rect)

        # Prekrytie funkcie Cooldown
        if pygame.time.get_ticks() - player.last_magic_switch_time < player.magic_switch_cooldown:
            cooldown_alpha = 150
            overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, cooldown_alpha))
            self.virtual_surface.blit(overlay, bg_rect)

    def display_death(self):
        # Text o smrti
        death_text = self.font.render("YOU DIED!", True, (255, 0, 0))
        text_rect = death_text.get_rect(center=(self.virtual_surface.get_width() // 2,
                                               self.virtual_surface.get_height() // 2))
        self.virtual_surface.blit(death_text, text_rect)

    def display(self, player):
        # vykreslenie vsetky UI elementy
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_coin(player.coins)
        self.weapon_overlay(player.weapon_index)
        self.magic_overlay(player.magic_index, player)

        # varovanie
        if player.energy < 20:
            warning_surf = self.font.render("LOW ENERGY!", True, (255, 0, 0))
            warning_rect = warning_surf.get_rect(center=(self.virtual_surface.get_width() // 2, 50))
            self.virtual_surface.blit(warning_surf, warning_rect)