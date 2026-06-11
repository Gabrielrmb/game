import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.const import C_GRAY
from code.enemy import Enemy
from code.entity import Entity
from code.entityfactory import EntityFactory
from code.entitymediator import EntityMediator
from code.player import Player


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('level1bg'))
        self.entity_list.append(EntityFactory.get_entity('enemy'))
        self.entity_list.append(EntityFactory.get_entity('player'))



    def run(self):
        pygame.mixer_music.load(f'./assets/{self.name}.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            player = next(ent for ent in self.entity_list if isinstance(ent, Player))

            enemies = [ent for ent in self.entity_list if isinstance(ent, Enemy)]
            if player.dead:
                pygame.mixer_music.stop()
                return "GAME OVER", self.window.copy()
            if len(enemies) == 0:
                pygame.mixer_music.stop()
                return "VICTORY", self.window.copy()

            for ent in self.entity_list:
                if isinstance(ent, Enemy):
                    ent: Enemy
                    ent.chase(player.rect)
                else:
                    ent.move()

                self.window.blit(source=ent.surf, dest=ent.rect)

            EntityMediator.verify_collision(self.entity_list)
            EntityMediator.draw_life_bar(self.window, self.entity_list)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level_text(14, f'Health: ', C_GRAY, (10, 5))

            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
