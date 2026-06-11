from code.background import Background
from code.const import WINDOW_WIDTH, WINDOW_HEIGHT
from code.enemy import Enemy
from code.player import Player


class EntityFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:
            case 'level1bg':
                list_bg = []
                for i in range(7):
                    list_bg.append(Background(f'level1bg{i}', (0, 0)))
                    list_bg.append(Background(f'level1bg{i}', (WINDOW_WIDTH, 0)))
                return list_bg
            case 'player':
                return Player('PlayerWalk', (10, WINDOW_HEIGHT / 2))
            case 'enemy':
                return Enemy('EnemyWalk', (WINDOW_WIDTH - 200, WINDOW_HEIGHT // 2))
