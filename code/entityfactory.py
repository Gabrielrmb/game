from code.background import Background
from code.const import WINDOW_WIDTH


class EntityFactory:


    def __init__(self):
        pass

    @staticmethod
    def get_entity(entity_name: str, position = (0,0)):
        match entity_name:
            case 'level1bg':
                list_bg = []
                for i in range(7):
                    list_bg.append(Background(f'level1bg{i}', (0, 0)))
                    list_bg.append(Background(f'level1bg{i}', (WINDOW_WIDTH, 0)))
                return list_bg