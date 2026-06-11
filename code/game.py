import pygame

from code.const import WINDOW_WIDTH, WINDOW_HEIGHT, MENU_OPTION
from code.gameover import GameOver
from code.level import Level
from code.menu import Menu
from code.victory import Victory


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                level = Level(self.window, 'Level1', menu_return)
                result = level.run()

                if isinstance(result, tuple):
                   state,last_frame = result
                   if state =="GAME OVER":
                        game_over = GameOver(self.window, last_frame)
                        game_over.run()
                   elif state == "VICTORY":
                       victory = Victory(self.window, last_frame)
                       victory.run()
            elif menu_return == MENU_OPTION[1]:
                pygame.quit()
                quit()
            else:
                pass