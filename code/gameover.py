import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WINDOW_WIDTH, WINDOW_HEIGHT, C_RED, C_GRAY


class GameOver:
    def __init__(self, window, last_frame):
        self.window = window
        self.last_frame = last_frame
        self.fade_alpha = 0
        self.fade_duration = 3000
        self.text_alpha = 0
        self.player_died_sound = pygame.mixer.Sound('./assets/youdied.mp3')
        self.sound_played = False


    def draw_fade_text(self, text, size, color, center, alpha):
        font=pygame.font.SysFont("Times New Roman", size, bold=True)
        text_surface = font.render(text, True, color).convert_alpha()
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=center)
        self.window.blit(text_surface, text_rect)


    def run(self):
        clock = pygame.time.Clock()
        fade_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        start_time = pygame.time.get_ticks()

        while True:
            clock.tick(60)
            self.window.blit(self.last_frame, (0, 0))
            elapsed = pygame.time.get_ticks() - start_time
            progress = min(1, elapsed / self.fade_duration)
            self.fade_alpha = int(progress * 255)
            if progress >= 0.25 and not self.sound_played:
                self.player_died_sound.play()
                self.sound_played = True
            fade_surface.fill((0,0,0, self.fade_alpha))
            self.window.blit(fade_surface, (0, 0))
            if self.fade_alpha >= 140:
                self.text_alpha = min(255, self.text_alpha + 2)
            if self.text_alpha:
                self.draw_fade_text('YOU DIED', 110, C_RED, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 -50), self.text_alpha)

            if self.text_alpha >= 255:
                self.draw_text(40, "press ENTER to main menu", C_GRAY,(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 +50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.text_alpha:
                        return



    def draw_text(self, size, text, color, center):
         font: Font = pygame.font.SysFont("Arial", size)
         surf: Surface = font.render(text, True, color).convert_alpha()
         rect: Rect = surf.get_rect(center=center)
         self.window.blit(source=surf, dest=rect)

