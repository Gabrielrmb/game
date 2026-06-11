import pygame

from code.const import WINDOW_HEIGHT, PLAYER_MOVE_LIM, WINDOW_WIDTH, PLAYER_VELOCITY, PLAYER_SPRITE_SCALE, PLAYER_HEALTH
from code.entity import Entity


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Walk
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.15
        sprite_sheet = pygame.image.load(f'./assets/{name}.png').convert_alpha()
        frame_width = sprite_sheet.get_width() // 8
        frame_height = sprite_sheet.get_height()
        scale = PLAYER_SPRITE_SCALE

        # Attack
        self.attack_frames = []
        self.attacking = False
        self.attack_key_pressed = False
        self.attack_frame = 0
        self.attack_speed = 0.1
        self.attack_hitbox = None
        attack_sheet = pygame.image.load('./assets/PlayerAttack.png').convert_alpha()
        attack_frame_width = attack_sheet.get_width() // 5
        attack_frame_height = attack_sheet.get_height()

        # Sound Attack:
        self.sword_attack_sound = pygame.mixer.Sound('./assets/swordAttack.mp3')
        self.hit_registered = False

        # health
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.dead_frames = []
        self.dead_frame = 0
        self.dead_speed = 0.06
        self.dying = False
        self.dead = False
        dead_sheet = pygame.image.load('./assets/PlayerDead.png').convert_alpha()
        dead_frame_width = dead_sheet.get_width() // 6
        dead_frame_height = dead_sheet.get_height()

        for i in range(8):
            frame = sprite_sheet.subsurface(i * frame_width, 0, frame_width, frame_height)
            frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
            self.frames.append(frame)

        for i in range(5):
            frame = attack_sheet.subsurface(i * attack_frame_width, 0, attack_frame_width, attack_frame_height)
            frame = pygame.transform.scale(frame, (int(frame_width * scale), int(frame_height * scale)))
            self.attack_frames.append(frame)

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)
        self.surf = self.frames[0]
        self.hitbox = pygame.Rect(self.rect.x - 0, self.rect.y + 0, 60, 145)
        self.speed = PLAYER_VELOCITY

        for i in range(6):
            frame = dead_sheet.subsurface(i * dead_frame_width, 0, dead_frame_width, dead_frame_height)
            frame = pygame.transform.scale(frame, (int(dead_frame_width * PLAYER_SPRITE_SCALE),
                                                   int(attack_frame_height * PLAYER_SPRITE_SCALE)))
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

    def player_health_bar(self, window: pygame.Surface):
        bar_w, bar_h = 250, 15
        bx = 10
        by = 30
        pygame.draw.rect(window, (80, 0, 0), (bx, by, bar_w, bar_h))
        filled = int(bar_w * self.health / self.max_health)

        pygame.draw.rect(window, (0, 255, 0), (bx, by, filled, bar_h))
        pygame.draw.rect(window, (200, 200, 200), (bx, by, bar_w, bar_h), 1)

    def death_animation(self):
        self.dead_frame += self.dead_speed
        if self.dead_frame >= len(self.dead_frames):
            self.dead = True
            self.dying = False
            return
        feet = self.rect.midbottom
        frame = self.dead_frames[int(self.dead_frame)]
        self.surf = frame
        self.rect = self.surf.get_rect(midbottom=feet)

    def animation(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        feet = self.rect.midbottom
        self.surf = self.frames[int(self.current_frame)]
        self.rect = self.surf.get_rect(midbottom=feet)
        self.update_player_hitbox()

    def attack_animation(self):
        self.attack_frame += self.attack_speed
        if self.attack_frame >= len(self.attack_frames):
            self.attack_frame = 0
            self.attacking = False
            self.attack_hitbox = None
            feet = self.rect.midbottom
            self.surf = self.frames[0]
            self.rect = self.surf.get_rect(midbottom=feet)
            self.update_player_hitbox()
            return

        feet = self.rect.midbottom
        self.surf = self.attack_frames[int(self.attack_frame)]
        self.rect = self.surf.get_rect(midbottom=feet)
        self.update_player_hitbox()

        if 4 <= int(self.attack_frame) <= 5:
            self.attack_hitbox = pygame.Rect(
                self.rect.right - 90,
                self.rect.top + 140, 85, 85
            )
        else:
            self.attack_hitbox = None

    def update_player_hitbox(self):
        self.hitbox.centerx = self.rect.centerx - 65
        self.hitbox.bottom = self.rect.bottom

    def move(self):
        if self.dying:
            self.death_animation()
            return
        if self.dead:
            return
        if self.attacking:
            self.attack_animation()
            return

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_SPACE] and not self.attack_key_pressed:
            self.attacking = True
            self.attack_key_pressed = True
            self.attack_frame = 0
            self.hit_registered = False
            self.sword_attack_sound.play()
            return
        if not pressed_key[pygame.K_SPACE]:
            self.attack_key_pressed = False

        moving = False

        if pressed_key[pygame.K_a] and self.rect.left >= 0:
            self.rect.centerx -= self.speed
            moving = True

        if pressed_key[pygame.K_d] and self.rect.right < WINDOW_WIDTH + 125:
            self.rect.centerx += self.speed
            moving = True

        if pressed_key[pygame.K_w] and self.rect.top > PLAYER_MOVE_LIM:
            self.rect.centery -= self.speed
            moving = True

        if pressed_key[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.centery += self.speed
            moving = True

        if moving:
            self.animation()
        else:
            self.current_frame = 0
            center = self.rect.center
            self.surf = self.frames[0]
            self.rect = self.surf.get_rect(center=center)
            self.update_player_hitbox()
