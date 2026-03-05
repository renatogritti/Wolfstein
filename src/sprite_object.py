"""
--------------------------------------------------------------------------------
Projeto: Wolfstein
Arquivo: sprite_object.py
Autor: Renato Gritti
Data: 2026-03-05
Descrição: Definição de objetos estáticos e interativos (powerups) no mundo 3D.
--------------------------------------------------------------------------------
"""


import pygame
import os
import math
from .settings import *

class SpriteObject:
    def __init__(self, game, path, pos, shift=0.27, scale=0.7):
        self.game = game
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.shift = shift
        self.scale = scale

    def update(self):
        pass

class Powerup(SpriteObject):
    def __init__(self, game, path, pos, type, value):
        super().__init__(game, path, pos)
        self.type = type
        self.value = value
        self.collected = False

    def update(self):
        self.check_collection()

    def check_collection(self):
        if self.collected or not self.game.player:
            return
        
        # Check proximity to player
        dx = self.x - self.game.player.x
        dy = self.y - self.game.player.y
        dist = math.hypot(dx, dy)
        
        if dist < 0.6: # Collection radius
            self.collect()

    def collect(self):
        self.collected = True
        if self.type == 'health':
            # 10% improvement
            self.game.player.health = min(PLAYER_MAX_HEALTH, self.game.player.health + 10)
            print(f"Health Powerup! +10% Health. Current: {self.game.player.health}")
        elif self.type == 'ammo':
            self.game.player.ammo += 10
            print(f"Ammo Powerup! +10 Ammo. Current: {self.game.player.ammo}")
        
        if self.game.snd_powerup:
            self.game.snd_powerup.play()
        
        if self in self.game.sprite_objects:
            self.game.sprite_objects.remove(self)
