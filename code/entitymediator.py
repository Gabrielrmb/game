import pygame
from pygame.mixer import Sound

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
                if player.attack_hitbox:
                    if player.attack_hitbox.colliderect(ent.hitbox):

                        if not player.hit_registered:
                            EntityMediator.sword_hit_sound.play()
                            player.hit_registered = True
                            print("inimigo atingido")
                            enemies_remove.append(ent)
                            # for enemy in enemies_remove:
                            #     entity_list.remove(enemy) <---- remove o inimigo quando derrotado

                if ent.attack_hitbox:  # ← fora do if player.attack_hitbox
                    if ent.attack_hitbox.colliderect(player.hitbox):
                        if not ent.hit_registered:
                            ent.hit_registered = True

                            print('Player atingido!')





    @staticmethod
    def draw_hitbox(window, entity_list):
        player = next((ent for ent in entity_list if isinstance(ent, Player)), None)

        #Player attack hitbox
        if player and player.attack_hitbox:
            pygame.draw.rect(window, (255,0,0), player.attack_hitbox, 2)
        if player:
            pygame.draw.rect(window, (0,0,255), player.hitbox, 2)





        #enemy body hitbox
        for ent in entity_list:
            if isinstance(ent, Enemy):
                pygame.draw.rect(window, (0,255,0), ent.hitbox, 2)

                if ent.attack_hitbox:
                    pygame.draw.rect(
                        window, (255,255,0), ent.attack_hitbox, 2)

