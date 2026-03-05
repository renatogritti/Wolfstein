import pygame
import math
from .settings import *

class Renderer:
    """
    Classe responsável pela renderização.
    Gerencia texturas e desenho de paredes e chão.
    """
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.floor_texture = pygame.image.load('assets/textures/floor.png').convert()
        self.sky_texture = pygame.Surface((WIDTH, HALF_HEIGHT))
        self.sky_texture.fill((50, 50, 50)) # Céu simples por enquanto

    def load_wall_textures(self):
        """Carrega e retorna um dicionário com as texturas das paredes."""
        return {
            '1': pygame.image.load('assets/textures/1.png').convert(),
            '2': pygame.image.load('assets/textures/2.png').convert(),
            '3': pygame.image.load('assets/textures/3.png').convert(),
            '4': pygame.image.load('assets/textures/4.png').convert(),
            '5': pygame.image.load('assets/textures/5.png').convert(),
            '9': pygame.image.load('assets/textures/9.png').convert(),
        }

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.render_sprites()
        self.draw_crosshair()
        self.draw_shot_effect()
        self.draw_damage_effect()

    def draw_crosshair(self):
        """Desenha uma mira (+) no centro da tela."""
        color = (0, 255, 0)
        length = 20
        # Horizontal line
        pygame.draw.line(self.screen, color, (HALF_WIDTH - length, HALF_HEIGHT), (HALF_WIDTH + length, HALF_HEIGHT), 2)
        # Vertical line
        pygame.draw.line(self.screen, color, (HALF_WIDTH, HALF_HEIGHT - length), (HALF_WIDTH, HALF_HEIGHT + length), 2)

    def draw_shot_effect(self):
        """Desenha um lampejo sutil quando o jogador atira."""
        if self.game.shot_timer > 0:
            # Subtle yellow flash in the center
            s = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 0, 100), (50, 50), 40)
            self.screen.blit(s, (HALF_WIDTH - 50, HALF_HEIGHT - 50))

    def draw_damage_effect(self):
        """Desenha um piscar vermelho na tela quando o jogador é atingido."""
        if self.game.damage_timer > 0:
            s = pygame.Surface(RES)
            s.set_alpha(100) # Semi-transparent
            s.fill((255, 0, 0))
            self.screen.blit(s, (0, 0))


    def draw_background(self):
        self.screen.blit(self.sky_texture, (0, 0))
        # Simple floor for now (solid color fallback if floor casting is too heavy)
        # We will implement floor casting separately if we can optimize it
        pygame.draw.rect(self.screen, (20, 20, 20), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def render_game_objects(self):
        list_objects = self.game.raycasting.ray_casting_result
        for ray, values in enumerate(list_objects):
            depth, proj_height, texture_id, offset = values

            if proj_height < HEIGHT:
                wall_column = self.wall_textures[texture_id].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, int(proj_height)))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.wall_textures[texture_id].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, int(texture_height)
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # Shadowing
            shade = 255 / (1 + depth ** 5 * 0.00002)
            if shade > 255: shade = 255
            if shade < 30: shade = 30
            
            # Apply shadow mask
            wall_column.fill((shade, shade, shade), special_flags=pygame.BLEND_MULT)
            
            self.screen.blit(wall_column, wall_pos)

            # Floor Casting
            wall_bottom = HALF_HEIGHT + proj_height // 2
            wall_bottom = max(wall_bottom, HALF_HEIGHT)
            wall_bottom = int(min(wall_bottom, HEIGHT))
            
            # Angle calculations
            ray_angle = self.game.player.angle - HALF_FOV + ray * DELTA_ANGLE
            cos_angle = math.cos(ray_angle)
            sin_angle = math.sin(ray_angle)
            # Fix fishbowl
            cos_beta = math.cos(self.game.player.angle - ray_angle)

            # Draw floor
            pos_x, pos_y = self.game.player.pos
            
            # Optimizing: Draw in chunks or skip pixels
            # For 1600 width, this is still 800 rays.
            # We will perform this loop only if wall_bottom < HEIGHT
            if wall_bottom < HEIGHT:
                 # Calculate distance for the bottom of the wall
                 # and the bottom of the screen
                 for y in range(wall_bottom, HEIGHT, 4): # Step 4 for performance
                     dist = SCREEN_DIST / (y - HALF_HEIGHT) / cos_beta
                     
                     texture_x = (pos_x + dist * cos_angle) * TEXTURE_SIZE % TEXTURE_SIZE
                     texture_y = (pos_y + dist * sin_angle) * TEXTURE_SIZE % TEXTURE_SIZE
                     
                     color = self.floor_texture.get_at((int(texture_x), int(texture_y)))
                     # Draw a 4px high rect
                     pygame.draw.rect(self.screen, color, (ray * SCALE, y, SCALE, 4))

    def render_sprites(self):
        sprite_list = []
        # Add enemies
        if hasattr(self.game, 'enemies'):
            for enemy in self.game.enemies:
                dx = enemy.x - self.game.player.x
                dy = enemy.y - self.game.player.y
                dist = math.hypot(dx, dy)
                if dist > 0.2:
                    # Enemy default scale 1.0, shift 0.0
                    sprite_list.append((dist, dx, dy, enemy, 1.0, 0.0))
        
        # Add sprite objects
        if hasattr(self.game, 'sprite_objects'):
            for sprite in self.game.sprite_objects:
                dx = sprite.x - self.game.player.x
                dy = sprite.y - self.game.player.y
                dist = math.hypot(dx, dy)
                if dist > 0.2:
                    sprite_list.append((dist, dx, dy, sprite, sprite.scale, sprite.shift))

        # Ordena do mais longe para o mais perto
        sprite_list.sort(key=lambda x: x[0], reverse=True)
        
        for dist, dx, dy, obj, scale, shift in sprite_list:
            theta = math.atan2(dy, dx)
            delta = theta - self.game.player.angle
            
            # Normalizar delta entre -PI e PI
            delta = (delta + math.pi) % math.tau - math.pi
            
            if abs(delta) < HALF_FOV + 0.5:
                proj_dist = dist * math.cos(delta)
                if proj_dist <= 0: continue
                
                proj_height = (SCREEN_DIST / proj_dist) * scale
                sprite_w = int(proj_height)
                # Handle ratio if it was defined, but for now assuming square
                # Actually for Powerups/Decorations, we might need ratio.
                # Let's check image ratio.
                if hasattr(obj, 'image'):
                    image = obj.image
                else: # Enemy
                    image = obj.frames[obj.current_frame]
                
                ratio = image.get_width() / image.get_height()
                sprite_w = int(proj_height * ratio)
                sprite_h = int(proj_height)
                
                screen_x = HALF_WIDTH + math.tan(delta) * SCREEN_DIST
                start_x = int(screen_x - sprite_w // 2)
                
                height_shift = sprite_h * shift
                start_y = int(HALF_HEIGHT - sprite_h // 2 + height_shift)
                
                if start_x + sprite_w < 0 or start_x > WIDTH:
                    continue
                    
                if image.get_width() > 0:
                    try:
                        # Scale image
                        frame = pygame.transform.scale(image, (sprite_w, sprite_h))
                        
                        # Z-buffer simplificado via colunas da textura original
                        for screen_col in range(start_x, start_x + sprite_w, SCALE):
                            if 0 <= screen_col < WIDTH:
                                ray_idx = screen_col // SCALE
                                if ray_idx < NUM_RAYS and ray_idx < len(self.game.raycasting.ray_casting_result):
                                    if proj_dist < self.game.raycasting.ray_casting_result[ray_idx][0]:
                                        tex_x = screen_col - start_x
                                        col_w = min(SCALE, sprite_w - tex_x)
                                        if col_w > 0:
                                            col_surf = frame.subsurface((tex_x, 0, col_w, sprite_h))
                                            self.screen.blit(col_surf, (screen_col, start_y))
                    except (ValueError, pygame.error):
                        pass
