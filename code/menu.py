from settings import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.virtual_surface = game.virtual_surface
        self.font = pygame.font.Font(UI_FONT, 12)  # Vbeľkosť písma
        self.title_font = pygame.font.Font(UI_FONT, 16)  # Veľkosť názvu
        self.instructions_font = pygame.font.Font(UI_FONT, 12)
        self.buttons = []
        self.init_menu()

    def init_menu(self):
        button_width = 200
        button_height = 40
        center_x = self.virtual_surface.get_width() // 2 - button_width // 2
        center_y = self.virtual_surface.get_height() // 2

        self.buttons = [
            {'rect': pygame.Rect(center_x, center_y, button_width, button_height),
             'text': 'Play',
             'action': self.game.start_game},

            {'rect': pygame.Rect(center_x, center_y + 60, button_width, button_height),
             'text': 'How to Play',
             'action': self.show_instructions}
        ]

    def show_instructions(self):
        self.game.current_state = 'how_to_play'

    def draw_instructions(self):
        self.virtual_surface.fill((30, 30, 30))

        # Nazov
        title = self.title_font.render("How to Play", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.virtual_surface.get_width() // 2, 10))
        self.virtual_surface.blit(title, title_rect)

        # Instrukcion
        instructions = [
            "Objective: Liberate all 4",
            "cities from monsters!",
            "",
            "Controls:",
            "WASD - Move",
            "LMB - Attack",
            "RMB - Magic",
            "Q - Switch weapon",
            "E - Switch magic",
            "",
            "Gameplay:",
            "- Collect coins from enemies",
            "- Upgrade skills",
            "- Defeat bosses",
            "- Explore biomes"
        ]

        # text pos
        y = 30
        line_height = 10  # Rozstupy medzi riadkami
        for line in instructions:
            text_surf = self.instructions_font.render(line, False, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=(10, y))
            self.virtual_surface.blit(text_surf, text_rect)
            y += line_height

        # Back gombik
        back_btn = {
            'rect': pygame.Rect(10, self.virtual_surface.get_height() - 30, 50, 20),
            'text': 'Back',
            'action': lambda: setattr(self.game, 'current_state', 'menu')
        }

        mouse_pos = pygame.mouse.get_pos()
        scaled_mouse = (
            mouse_pos[0] * (self.virtual_surface.get_width() / self.game.window_width),
            mouse_pos[1] * (self.virtual_surface.get_height() / self.game.window_height)
        )

        # Gombik style
        btn_color = (100, 100, 200) if back_btn['rect'].collidepoint(scaled_mouse) else (50, 50, 150)
        pygame.draw.rect(self.virtual_surface, btn_color, back_btn['rect'], border_radius=3)
        text = self.font.render(back_btn['text'], True, (255, 255, 255))
        text_rect = text.get_rect(center=back_btn['rect'].center)
        self.virtual_surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            scaled_mouse = (
                mouse_pos[0] * (self.virtual_surface.get_width() / self.game.window_width),
                mouse_pos[1] * (self.virtual_surface.get_height() / self.game.window_height)
            )

            if self.game.current_state == 'menu':
                for btn in self.buttons:
                    if btn['rect'].collidepoint(scaled_mouse):
                        btn['action']()

            elif self.game.current_state == 'how_to_play':
                back_btn_rect = pygame.Rect(20, self.virtual_surface.get_height() - 40, 60, 20)
                if back_btn_rect.collidepoint(scaled_mouse):
                    self.game.current_state = 'menu'

    def draw(self):
        if self.game.current_state == 'menu':
            self.draw_main_menu()
        elif self.game.current_state == 'how_to_play':
            self.draw_instructions()

    def draw_main_menu(self):
        self.virtual_surface.fill((30, 30, 30))

        # nazov
        title = self.title_font.render("Arcane Trials", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.virtual_surface.get_width() // 2, 50))
        self.virtual_surface.blit(title, title_rect)

        # gombik
        mouse_pos = pygame.mouse.get_pos()
        scaled_mouse = (
            mouse_pos[0] * (self.virtual_surface.get_width() / self.game.window_width),
            mouse_pos[1] * (self.virtual_surface.get_height() / self.game.window_height)
        )

        for btn in self.buttons:
            color = (100, 100, 200) if btn['rect'].collidepoint(scaled_mouse) else (50, 50, 150)
            pygame.draw.rect(self.virtual_surface, color, btn['rect'])
            text = self.font.render(btn['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=btn['rect'].center)
            self.virtual_surface.blit(text, text_rect)