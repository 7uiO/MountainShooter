#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, WIN_WIDTH
from code.enemy import Enemy
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.entityMediator import entityMediator
from code.player import Player


class Level:
    def __init__(self, window, name, game_mode):
        self.timeout = 20000  # 20 segundos
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.entity_list.append(EntityFactory.get_entity('Player1'))

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

    def run(self):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()
        game_over = False

        while True:
            clock.tick(60)
            self.window.fill((0, 0, 0))

            for ent in self.entity_list:
                if ent.health > 0:
                    ent.move()
                    self.window.blit(source=ent.surf, dest=ent.rect)
                    if isinstance(ent, (Player, Enemy)):
                        shoot = ent.shoot()
                        if shoot is not None:
                            self.entity_list.append(shoot)
                    if ent.name == 'Player1':
                        self.level_text(25, f'Health: {ent.health} | Score: {ent.score}', C_GREEN, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY and not game_over:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            # Verifica se o jogador está vivo
            player = next((ent for ent in self.entity_list if ent.name == 'Player1'), None)
            if player and player.health <= 0:
                game_over = True
                self.display_game_over(player.score)
                pygame.display.flip()
                pygame.time.delay(5000)
                pygame.quit()
                sys.exit()

            # Textos informativos
            #self.level_text(30, f'{self.name} - Timeout: {self.timeout / 100 :.1f}s', C_WHITE, (10, 5))
            #self.level_text(15, f'fps: {clock.get_fps(): 0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            #self.level_text(15, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()

            # Colisões e remoções
            entityMediator.verify_collision(entity_list=self.entity_list)
            entityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)

    def display_game_over(self, score: int):
        font_big = pygame.font.SysFont("Lucida Sans Typewriter", 36)
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 24)

        game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
        score_text = font_small.render(f"Score: {score}", True, C_WHITE)

        go_rect = game_over_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 20))
        score_rect = score_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20))

        self.window.blit(game_over_text, go_rect)
        self.window.blit(score_text, score_rect)
