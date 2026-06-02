import pygame
from pygame import Surface, Rect
from pygame.font import Font

pygame.init()

from code.const import WINDOW_WIDTH, WINDOW_HEIGHT, C_GRAY, C_VERMELHO, MENU_OPTION


class Menu():

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/menubg.png').convert()
        self.surf = pygame.transform.scale(self.surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def run(self):
        pygame.mixer.music.load('./assets/menu.mp3')
        pygame.mixer.music.play(-1)

        while True:
            self.window.blit(self.surf, (0, 0))
            self.menu_text(100, 'Knight`s ', C_GRAY, ((WINDOW_WIDTH / 2), 120))
            self.menu_text(100, 'Heart', C_VERMELHO, ((WINDOW_WIDTH / 2), 200))

            for i in range(len(MENU_OPTION)):
                self.menu_text(50, MENU_OPTION[i], C_GRAY, ((WINDOW_WIDTH / 2), 500 + 50 * i))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Helvética", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
