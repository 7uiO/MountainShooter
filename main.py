#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.menu import Menu
from code.level import Level

pygame.init()
window = pygame.display.set_mode((576, 324))
pygame.display.set_caption("Mountain Shooter")

while True:
    menu = Menu(window)
    choice = menu.run()

    if choice == "PLAY":
        level = Level(window, name="Level1", game_mode="NORMAL")
        level.run()
