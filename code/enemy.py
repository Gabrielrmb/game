from random import randint, uniform

import pygame
import math

from code.entity import Entity
from code.const import ENEMY_VELOCITY_MIN, ENEMY_VELOCITY_MAX


class Enemy(Entity):



    def __init__(self, name:str, position:tuple):
        super().__init__(name, position)

        #Walk
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.10
        self.speed = round(uniform(ENEMY_VELOCITY_MIN, ENEMY_VELOCITY_MAX), 1)


        sprite_sheet = pygame.image.load(f"./assets/EnemyWalk.png").convert_alpha()
        frame_width = sprite_sheet.get_width() // 7
        frame_height = sprite_sheet.get_height()
        scale = 2.0
        for i in range(7):
            frame = sprite_sheet.subsurface(i * frame_width, 0, frame_width, frame_height )
            frame = pygame.transform.scale(frame,(int(frame_width * scale), int(frame_height * scale)))
            self.frames.append(frame)

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft = position)



    def animation(self, facing_left: bool):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        center = self.rect.center
        frame = self.frames[int(self.current_frame)]
        self.surf = pygame.transform.flip(frame, facing_left, False)
        self.rect = self.surf.get_rect(center=center)


    def move(self):
        self.rect.centerx -= self.speed
        self.animation(facing_left = True)



    def chase(self, player_rect: pygame.Rect):

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery- self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 1.1:
            self.animation(facing_left = True)
            return

        if distance != 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
        self.rect.centerx += round(dx)
        self.rect.centery += round(dy)

        facing_left = dx < 0
        self.animation(facing_left)

