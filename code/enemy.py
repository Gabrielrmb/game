from random import uniform
import pygame
from code.entity import Entity
from code.const import ENEMY_SPRITE_SCALE, ENEMY_ATTACK_RANGE, ENEMY_VELOCITY


class Enemy(Entity):



    def __init__(self, name:str, position:tuple):
        super().__init__(name, position)

        #Walk
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.10
        self.speed = ENEMY_VELOCITY
        sprite_sheet = pygame.image.load(f"./assets/EnemyWalk.png").convert_alpha()
        frame_width = sprite_sheet.get_width() // 7
        frame_height = sprite_sheet.get_height()

        #Attack
        self.attack_frames = []
        self.attacking = False
        self.attack_frame = 0
        self.attack_speed = 0.10
        self.attack_hitbox = None
        self.hit_registered = False
        attack_sheet = pygame.image.load('./assets/EnemyAttack.png').convert_alpha()
        attack_frame_width = attack_sheet.get_width() // 5
        attack_frame_height = attack_sheet.get_height()


        #Collision
        self.hitbox = self.rect.inflate(-60, -20)



        for i in range(7):
            frame = sprite_sheet.subsurface(i * frame_width, 0, frame_width, frame_height )
            frame = pygame.transform.scale(frame,(int(frame_width * ENEMY_SPRITE_SCALE), int(frame_height * ENEMY_SPRITE_SCALE)))
            self.frames.append(frame)

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)
        self.hitbox = pygame.Rect(self.rect.x + 60, self.rect.y + 20, 60, 140)

        for i in range(5):
            frame = attack_sheet.subsurface(i * attack_frame_width, 0, attack_frame_width, attack_frame_height)
            frame = pygame.transform.scale(frame,(int(attack_frame_width * ENEMY_SPRITE_SCALE ), int(attack_frame_height * ENEMY_SPRITE_SCALE)))
            self.attack_frames.append(frame)
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft = position)


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
                self.rect.top + 100 ,60, 70
            )
        else:
            self.attack_hitbox = None

    def update_enemy_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def move(self):
        self.rect.centerx -= self.speed
        self.walk_animation(facing_left = True)



    def chase(self, player_rect: pygame.Rect):

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery- self.rect.centery
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
            self.walk_animation(facing_left = True)
            return

        if distance != 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
        self.rect.centerx += round(dx)
        self.rect.centery += round(dy)


        self.walk_animation(facing_left)

