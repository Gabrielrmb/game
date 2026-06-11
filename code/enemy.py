import pygame

from code.const import ENEMY_SPRITE_SCALE, ENEMY_ATTACK_RANGE, ENEMY_VELOCITY, ENEMY_HEALTH
from code.entity import Entity


class Enemy(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # Walk
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.10
        self.speed = ENEMY_VELOCITY
        sprite_sheet = pygame.image.load(f"./assets/EnemyWalk.png").convert_alpha()
        frame_width = sprite_sheet.get_width() // 7
        frame_height = sprite_sheet.get_height()

        # Attack
        self.attack_frames = []
        self.attacking = False
        self.attack_frame = 0
        self.attack_speed = 0.10
        self.attack_hitbox = None
        self.hit_registered = False
        attack_sheet = pygame.image.load('./assets/EnemyAttack.png').convert_alpha()
        attack_frame_width = attack_sheet.get_width() // 5
        attack_frame_height = attack_sheet.get_height()

        # Health
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        self.dead_frames = []
        self.dead_frame = 0
        self.dead_speed = 0.08
        self.dying = False
        self.dead = False
        dead_sheet = pygame.image.load('./assets/EnemyDead.png').convert_alpha()
        dead_frame_width = dead_sheet.get_width() // 4
        dead_frame_height = dead_sheet.get_height()

        # Walk
        for i in range(7):
            frame = sprite_sheet.subsurface(i * frame_width, 0, frame_width, frame_height)
            frame = pygame.transform.scale(frame, (int(frame_width * ENEMY_SPRITE_SCALE),
                                                   int(frame_height * ENEMY_SPRITE_SCALE)))
            self.frames.append(frame)

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)
        self.hitbox = pygame.Rect(self.rect.x + 60, self.rect.y + 20, 60, 140)

        # Attack
        for i in range(5):
            frame = attack_sheet.subsurface(i * attack_frame_width, 0, attack_frame_width, attack_frame_height)
            frame = pygame.transform.scale(frame, (int(attack_frame_width * ENEMY_SPRITE_SCALE),
                                                   int(attack_frame_height * ENEMY_SPRITE_SCALE)))
            self.attack_frames.append(frame)
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)

        # Dead
        for i in range(4):
            frame = dead_sheet.subsurface(i * dead_frame_width, 0, dead_frame_width, dead_frame_height)
            frame = pygame.transform.scale(frame, (int(dead_frame_width * ENEMY_SPRITE_SCALE),
                                                   int(attack_frame_height * ENEMY_SPRITE_SCALE)))
            self.dead_frames.append(frame)
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)

    def take_damage(self, amount: int = 1):
        if self.dead or self.dying:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.dying = True
            self.dead_frame = 0
            self.attack_hitbox = None

    def enemy_health_bar(self, window: pygame.Surface):
        bar_w, bar_h = 60, 8
        bx = self.rect.centerx - bar_w // 2
        by = self.rect.top - 14
        pygame.draw.rect(window, (80, 0, 0), (bx, by, bar_w, bar_h))
        filled = int(bar_w * self.health / self.max_health)
        if filled > 0:
            pygame.draw.rect(window, (220, 20, 60), (bx, by, filled, bar_h))
        pygame.draw.rect(window, (200, 200, 200), (bx, by, bar_w, bar_h), 1)

    def death_animation(self):
        self.dead_frame += self.dead_speed
        if self.dead_frame >= len(self.dead_frames):
            self.dead = True
            self.dying = False
            return
        feet = self.rect.midbottom
        frame = self.dead_frames[int(self.dead_frame)]
        self.surf = pygame.transform.flip(frame, True, False)
        self.rect = self.surf.get_rect(midbottom=feet)

    def walk_animation(self, facing_left: bool):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        frame = self.frames[int(self.current_frame)]
        feet = self.rect.midbottom
        self.surf = pygame.transform.flip(frame, facing_left, False)
        self.rect = self.surf.get_rect(midbottom=feet)
        self.hitbox.center = self.rect.center
        self.update_enemy_hitbox()

    def attack_animation(self, facing_left: bool):
        self.attack_frame += self.attack_speed
        if self.attack_frame >= len(self.attack_frames):
            self.attack_frame = 0
            self.attacking = False
            self.attack_hitbox = None
            self.hit_registered = False
            feet = self.rect.midbottom
            self.surf = self.frames[0]
            self.rect = self.surf.get_rect(midbottom=feet)
            self.update_enemy_hitbox()

            return

        feet = self.rect.midbottom
        frame = self.attack_frames[int(self.attack_frame)]
        self.surf = pygame.transform.flip(frame, facing_left, False)
        self.rect = self.surf.get_rect(midbottom=feet)
        self.update_enemy_hitbox()

        if 3 <= int(self.attack_frame) <= 4:
            self.attack_hitbox = pygame.Rect(
                self.rect.left - 10,
                self.rect.top + 100, 80, 70
            )
        else:
            self.attack_hitbox = None

    def update_enemy_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def move(self):
        if self.dying:
            self.death_animation()
            return
        if self.dead:
            return

        self.rect.centerx -= self.speed
        self.walk_animation(facing_left=True)

    def chase(self, player_rect: pygame.Rect):
        if self.dying:
            self.death_animation()
            return
        if self.dead:
            return

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        facing_left = True

        if distance < ENEMY_ATTACK_RANGE:
            if not self.attacking:
                self.attacking = True
                self.attack_frame = 0

        if self.attacking:
            self.attack_animation(facing_left)
            return

        if distance < self.speed:
            self.rect.centerx = player_rect.centerx
            self.rect.centery = player_rect.centery
            self.walk_animation(facing_left=True)
            return

        if distance != 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
        self.rect.centerx += round(dx)
        self.rect.centery += round(dy)

        self.walk_animation(facing_left)
