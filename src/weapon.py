"""
--------------------------------------------------------------------------------
Projeto: Wolfstein
Arquivo: weapon.py
Autor: Renato Gritti
Data: 2026-03-05
Descrição: Gerenciamento de animações e lógica de disparo da arma do jogador.
--------------------------------------------------------------------------------
"""


import os
import pygame
from PIL import Image
from .settings import *

class Weapon:
    """
    Classe para gerenciar a arma do jogador.
    Carrega o GIF, extrai os frames e os renderiza na tela sem necessidade de spritesheets externas.
    """
    def __init__(self, game):
        self.game = game
        self.frames = []
        self.load_frames()
        
        self.is_firing = False
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 3  # Ticks por frame. Ajuste para a velocidade certa

    def load_frames(self):
        """Carrega e converte os frames do GIF para superfícies do Pygame."""
        try:
            gif_path = os.path.join(os.path.dirname(__file__), '../assets/images/Fire.gif')
            img = Image.open(gif_path)
            
            for index in range(img.n_frames):
                img.seek(index)
                frame_rgba = img.convert("RGBA")
                
                pygame_image = pygame.image.fromstring(
                    frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode).convert_alpha()
                
                # Vamos escalar a arma para que fique em um tamanho agradável na tela 
                # (aproximadamente 60% da altura da tela, no formato da resolução atual)
                target_height = int(HEIGHT * 0.6)
                scale_factor = target_height / pygame_image.get_height()
                target_width = int(pygame_image.get_width() * scale_factor)
                
                pygame_image = pygame.transform.scale(pygame_image, (target_width, target_height))
                
                self.frames.append(pygame_image)
        except Exception as e:
            print(f"Atenção, erro ao carregar arma Fire.gif: {e}")
            # Fallback seguro caso não tenha PIL ou a imagem
            surface = pygame.Surface((300, 400))
            surface.fill((100, 100, 100))
            self.frames = [surface]

    def shoot(self):
        """Inicia a sequência de tiro se não estiver atirando no momento."""
        if not self.is_firing:
            player = self.game.player
            if player.ammo <= 0:
                print("Sem munição!")
                return
            player.ammo -= 1
            self.is_firing = True
            self.current_frame = 0
            self.animation_timer = 0
            # Dispara a lógica de hitscan no jogo
            self.game.check_hit()

    def update(self):
        """Atualiza a animação da arma se estiver atirando."""
        if self.is_firing:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame += 1
                
                # Fim da animação
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0
                    self.is_firing = False

    def draw(self):
        """Desenha o frame atual da arma na tela centralizado horizontalmente na parte inferior."""
        if not self.frames:
            return
            
        frame_to_draw = self.frames[self.current_frame] if self.is_firing else self.frames[0]
        
        # Centraliza a imagem na base da tela
        x = HALF_WIDTH - frame_to_draw.get_width() // 2
        y = HEIGHT - frame_to_draw.get_height()
        
        self.game.screen.blit(frame_to_draw, (x, y))
