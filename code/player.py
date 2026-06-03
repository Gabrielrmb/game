import pygame

from code.const import WINDOW_HEIGHT, PLAYER_MOVE_LIM, WINDOW_WIDTH, PLAYER_VELOCITY
from code.entity import Entity

class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        #Walk
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.15
        sprite_sheet = pygame.image.load(f'./assets/{name}.png').convert_alpha()
        frame_width = sprite_sheet.get_width() // 8
        frame_height = sprite_sheet.get_height()

        #Attack
        self.attack_frames = []
        self.attacking = False
        self.attack_key_pressed = False
        self.attack_frame = 0
        self.attack_speed = 0.1
        attack_sheet = pygame.image.load('./assets/PlayerAttack.png').convert_alpha()
        attack_frame_width = attack_sheet.get_width() // 5
        attack_frame_height = attack_sheet.get_height()


        for i in range(5):
            frame = attack_sheet.subsurface( i * attack_frame_width, 0, attack_frame_width, attack_frame_height)
            frame = pygame.transform.scale(frame, (frame_width, frame_height))
            self.attack_frames.append(frame)


        for i in range(8):
            frame = sprite_sheet.subsurface(i * frame_width, 0, frame_width, frame_height)
            frame = pygame.transform.scale(frame, (frame_width, frame_height))
            self.frames.append(frame)

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft = position)
        self.speed = PLAYER_VELOCITY

    def animation(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        center = self.rect.center
        self.surf = self.frames[int(self.current_frame)]
        self.rect = self.surf.get_rect(center=center)

    def attack_animation(self):
        self.attack_frame += self.attack_speed

        if self.attack_frame >= len(self.attack_frames):
            self.attack_frame = 0
            self.attacking = False
            center = self.rect.center
            self.surf = self.frames[0]
            self.rect = self.surf.get_rect(center=center)
            return

        center = self.rect.center
        self.surf = self.attack_frames[int(self.attack_frame)]
        self.rect = self.surf.get_rect(center=center)

    def move(self):
        if self.attacking:
            self.attack_animation()
            return

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_SPACE] and not self.attack_key_pressed:
            self.attacking = True
            self.attack_key_pressed = True
            self.attack_frame = 0
            return
        if not pressed_key[pygame.K_SPACE]:
            self.attack_key_pressed = False

        moving = False

        if pressed_key[pygame.K_LEFT] and self.rect.left >= 0:
            self.rect.centerx -= self.speed
            moving = True

        if pressed_key[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH + 125:
            self.rect.centerx += self.speed
            moving = True

        if pressed_key[pygame.K_UP] and self.rect.top > PLAYER_MOVE_LIM:
            self.rect.centery -= self.speed
            moving = True

        if pressed_key[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.centery += self.speed
            moving = True

        if moving:
            self.animation()
        else:
            self.current_frame = 0
            center = self.rect.center
            self.surf = self.frames[0]
            self.rect = self.surf.get_rect(center=center)
