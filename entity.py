from settings import *
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 5
        self.direction = pygame.Vector2()
        self.pos = pygame.Vector2()  # Skutočná pozícia
        self.mask = None


    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

        # Aktualizácia Hitboxu na základe skutočnej polohy
        self.hitbox.centerx = self.pos.x
        self.collision("horizontal")
        self.hitbox.centery = self.pos.y
        self.collision("vertical")

        #Aktualizácia Rekta z pozície HITBOX (nie z pozície!)
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.centerx
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.centerx
                    self.direction.x = 0

                elif direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.centery
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.centery
                    self.direction.y = 0

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def waveVal(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0