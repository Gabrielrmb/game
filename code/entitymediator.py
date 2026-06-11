import pygame

from code.enemy import Enemy
from code.player import Player


class EntityMediator:
    pygame.init()
    sword_hit_sound = pygame.mixer.Sound('./assets/swordHit.mp3')

    @staticmethod
    def verify_collision(entity_list):
        player = next((ent for ent in entity_list if isinstance(ent, Player)), None)
        if player is None:
            return
        enemies_remove = []
        for ent in entity_list:
            if isinstance(ent, Enemy):
                if ent.dead:
                    enemies_remove.append(ent)
                    continue
                if ent.dying:
                    continue
                if player.attack_hitbox:
                    if player.attack_hitbox.colliderect(ent.hitbox):

                        if not player.hit_registered:
                            EntityMediator.sword_hit_sound.play()
                            EntityMediator.sword_hit_sound.set_volume(0.8)

                            player.hit_registered = True
                            ent.take_damage(1)

                if ent.attack_hitbox:
                    if ent.attack_hitbox.colliderect(player.hitbox):
                        if not ent.hit_registered:
                            ent.hit_registered = True
                            player.take_damage(1)

        for enemy in enemies_remove:
            entity_list.remove(enemy)

    @staticmethod
    def draw_life_bar(window, entity_list):
        player = next((ent for ent in entity_list if isinstance(ent, Player)), None)

        if player:
            player.player_health_bar(window)

        for ent in entity_list:
            if isinstance(ent, Enemy):
                if not ent.dead:
                    ent.enemy_health_bar(window)
