"""
--------------------------------------------------------------------------------
Projeto: Wolfstein
Arquivo: enemy.py
Autor: Renato Gritti
Data: 2026-03-05
Descrição: Lógica de inteligência artificial, movimentação e combate dos inimigos.
--------------------------------------------------------------------------------
"""


import pygame
import math
import os
from PIL import Image
from .settings import *

class Enemy:
    """
    Classe base para Inimigos.
    """
    def __init__(self, game, x, y, char_type):
        self.game = game
        self.x = x + 0.5  # Centraliza na célula
        self.y = y + 0.5
        self.char_type = char_type
        
        self.frames = []
        self.load_frames()
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 5
        
        self.state = 'idle' # idle, walking, attacking
        self.speed = 0.02
        self.size = 10  # Para raio de colisão simplificado
        
        self.health = 50
        self.attack_timer = 0
        self.attack_speed = 60 # Ataca a cada 60 frames (aprox 1s)
        self.damage = 10
        
    def load_frames(self):
        filename = f"assets/images/{self.char_type}.gif"
        path = os.path.join(os.path.dirname(__file__), '..', filename)
        try:
            img = Image.open(path)
            for index in range(img.n_frames):
                img.seek(index)
                frame_rgba = img.convert("RGBA")
                pygame_image = pygame.image.fromstring(
                    frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode).convert_alpha()
                self.frames.append(pygame_image)
        except Exception as e:
            print(f"Erro ao carregar inimigo {filename}: {e}")
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 0, 0), (32, 32), 32)
            self.frames = [surf]

    def update(self):
        self.animate()
        self.ai_logic()
        
    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def check_los(self):
        """Verifica se há linha de visão direta entre o inimigo e o jogador."""
        px, py = self.game.player.pos
        ex, ey = self.x, self.y
        
        dx = px - ex
        dy = py - ey
        distance = math.hypot(dx, dy)
        
        if distance == 0:
            return True
            
        dx /= distance
        dy /= distance
        
        # Percorre o caminho em pequenos passos para verificar colisão com paredes
        step = 0.2
        for i in range(1, int(distance / step)):
            check_x = ex + dx * (i * step)
            check_y = ey + dy * (i * step)
            if (int(check_x), int(check_y)) in self.game.map.world_map:
                return False
        return True

    def ai_logic(self):
        # Lógica de seguir o jogador
        px, py = self.game.player.pos
        dx = px - self.x
        dy = py - self.y
        distance = math.hypot(dx, dy)
        
        # Só age se tiver linha de visão
        has_los = self.check_los()
        
        # Aumentamos o range de ataque para uma distância mais realista.
        # Se ver o jogador (distância < 10) começa a seguir. 
        # Mas para atirar / atacar (distância <= 3.0), ele para de seguir e ataca.
        attack_range = 3.0
        collision_radius = 0.6
        
        if has_los and distance < 10 and distance > attack_range:
            self.state = 'walking'
            dx = dx / distance
            dy = dy / distance
            
            # Movimento com raio de colisão para evitar atravessar paredes
            check_x = self.x + dx * self.speed
            check_y = self.y + dy * self.speed
            
            # Wall collision check with radius
            if (int(check_x + (collision_radius if dx > 0 else -collision_radius)), int(self.y)) not in self.game.map.world_map:
                self.x = check_x
            if (int(self.x), int(check_y + (collision_radius if dy > 0 else -collision_radius))) not in self.game.map.world_map:
                self.y = check_y
        elif has_los and distance <= attack_range:
            self.state = 'attacking'
            # Lógica de combate - dano no Player
            self.attack_timer += 1
            if self.attack_timer >= self.attack_speed:
                self.attack_timer = 0
                self.game.player.health -= self.damage
                self.game.trigger_damage()
                print(f"Ai! Inimigo me atacou! Vida: {self.game.player.health}")
        else:
            self.state = 'idle'
            self.attack_timer = 0



