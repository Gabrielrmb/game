import pygame
from pygame import Surface, Rect
from pygame.font import Font

pygame.init()

from code.const import WINDOW_WIDTH, WINDOW_HEIGHT, C_GRAY, C_RED, MENU_OPTION, PLAYER_SPRITE_SCALE


class _Parallax:
    def __init__(self, surf: pygame.Surface, speed: float):
        self.surf = pygame.transform.smoothscale(surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.speed = speed
        self.x = 0.0

    def update(self):
        self.x -= self.speed
        if self.x <= -WINDOW_WIDTH:
            self.x = 0.0

    def draw(self, window: pygame.Surface):
        window.blit(self.surf, (int(self.x), 0))
        window.blit(self.surf, (int(self.x) + WINDOW_WIDTH, 0))


class Menu:
    MENU_PARALLAX = [
        (0, 0.0),
        (1, 0.3),
        (2, 0.5),
        (3, 0.7),
        (4, 1.0),
        (5, 1.2),
        (6, 1.4),
        (7, 1.4),
    ]

    def __init__(self, window):

        self.window = window
        self.layers: list[_Parallax] = []
        for idx, speed in self.MENU_PARALLAX:
            raw = pygame.image.load(f'./assets/menubg{idx}.png').convert_alpha()
            self.layers.append(_Parallax(surf=raw, speed=speed))

        self.knight_frames: list[pygame.Surface] = []
        self.knight_frame = 0.0
        self.knight_speed = 0.12
        sprite_sheet = pygame.image.load('./assets/PlayerWalk.png').convert_alpha()
        fw = sprite_sheet.get_width() // 8
        fh = sprite_sheet.get_height()

        for i in range(8):
            frame = sprite_sheet.subsurface(i * fw, 0, fw, fh)
            frame = pygame.transform.scale(frame, (int(fw * PLAYER_SPRITE_SCALE), int(fh * PLAYER_SPRITE_SCALE)))
            self.knight_frames.append(frame)

    def run(self):
        menu_option = 0
        clock = pygame.time.Clock()
        pygame.mixer.music.load('./assets/menu.mp3')
        pygame.mixer.music.play(-1)

        while True:
            clock.tick(60)
            for layer in self.layers:
                layer.update()
                layer.draw(self.window)
            self.menu_text(100, 'Knight`s ', C_GRAY, ((WINDOW_WIDTH / 2), 120))
            self.menu_text(100, 'Heart', C_RED, ((WINDOW_WIDTH / 2), 200))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(50, MENU_OPTION[i], C_RED, ((WINDOW_WIDTH / 2), 500 + 50 * i))

                else:
                    self.menu_text(50, MENU_OPTION[i], C_GRAY, ((WINDOW_WIDTH / 2), 500 + 50 * i))

            self.menu_text(40, 'CONTROLS', C_GRAY, ((WINDOW_WIDTH // 2 + 350), 470))
            self.menu_text(30, 'Attack: SPACE', C_GRAY, ((WINDOW_WIDTH // 2 + 350), 510))
            self.menu_text(30, 'Walk: W,A,S,D', C_GRAY, ((WINDOW_WIDTH // 2 + 350), 550))
            self.menu_text(30, 'Menu: ENTER, ARROW KEYS', C_GRAY, ((WINDOW_WIDTH // 2 + 350), 590))
            self._draw_knight()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1

                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def _draw_knight(self):
        self.knight_frame = (self.knight_frame + self.knight_speed) % len(self.knight_frames)
        frame = self.knight_frames[int(self.knight_frame)]
        x = WINDOW_WIDTH // 2 - 220 - frame.get_width()
        y = 625 - frame.get_height()
        self.window.blit(frame, (x, y))

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Helvética", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
