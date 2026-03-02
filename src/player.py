from .settings import *
import pygame
import math

class Player:
    """
    Classe que representa o jogador.
    Gerencia movimento, colisão e câmera.
    """
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.lives  = PLAYER_START_LIVES
        self.ammo   = PLAYER_START_AMMO
        self.score  = PLAYER_START_SCORE


    def movement(self):
        """Calcula o movimento do jogador baseado nas teclas pressionadas."""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]: # Strafe esquerda
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]: # Strafe direita
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau # Mantém o ângulo entre 0 e 2PI

    def check_wall_collision(self, dx, dy):
        """Simples detecção de colisão contra paredes no mapa."""
        if not (int(self.x + dx), int(self.y)) in self.game.map.world_map:
            self.x += dx
        if not (int(self.x), int(self.y + dy)) in self.game.map.world_map:
            self.y += dy

    def draw(self):
        """Opcional: Desenha o jogador no mapa 2D para depuração."""
        # pygame.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #                (self.x * 100 + WIDTH * math.cos(self.angle),
        #                 self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'green', (int(self.x * 100), int(self.y * 100)), 15)

    def update(self):
        if self.health <= 0:
            self.game.state = 'GAME_OVER'
            return
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def get_interaction_tile(self):
        """Retorna as coordenadas do bloco à frente do jogador para interação."""
        # Verificação simples: bloco imediatamente à frente
        dx = math.cos(self.angle)
        dy = math.sin(self.angle)
        check_x = int(self.x + dx * 0.8) # 0.8 é a distância de interação
        check_y = int(self.y + dy * 0.8)
        return check_x, check_y

