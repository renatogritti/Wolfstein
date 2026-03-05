import pygame
import sys
import os
from .settings import *
from .map import Map
from .player import Player
from .raycasting import RayCasting
from .renderer import Renderer
from .weapon import Weapon
from .hud import HUD
from .sprite_object import SpriteObject, Powerup

class Game:
    """
    Classe principal do jogo.
    Inicializa o Pygame, gerencia o fluxo do jogo (loop principal) e instancia os componentes.
    Agora inclui gerenciamento de estados para Splash, Fases e Fim de Jogo.
    """
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.current_level = 1
        
        # Load Images
        self.load_images()
        # Load Sounds
        self.load_sounds()
        
        # Game State: SPLASH, PHASE, GAME, GAME_OVER, VICTORY
        self.state = 'SPLASH'
        self.play_splash_music()
        
        # Game objects will be initialized in new_game but we need them for some logic
        self.map = None
        self.player = None
        self.renderer = None
        self.raycasting = None
        self.weapon = None
        self.enemies = []
        self.sprite_objects = []
        
        # Timers for visual effects
        self.shot_timer = 0
        self.damage_timer = 0

    def load_images(self):
        """Carrega e escala as imagens de interface."""
        img_dir = os.path.join(os.path.dirname(__file__), '../assets/images')
        
        try:
            self.splash_img = pygame.image.load(os.path.join(img_dir, 'Splash.jpg')).convert()
            self.splash_img = pygame.transform.scale(self.splash_img, RES)
            
            self.phase_img = pygame.image.load(os.path.join(img_dir, 'phase.jpg')).convert()
            self.phase_img = pygame.transform.scale(self.phase_img, RES)
            
            self.end_img = pygame.image.load(os.path.join(img_dir, 'End.jpg')).convert()
            self.end_img = pygame.transform.scale(self.end_img, RES)
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
            # Fallback to simple colors or creation if missing (optional, but requested to use existing)
            self.splash_img = pygame.Surface(RES)
            self.splash_img.fill(BLACK)
            self.phase_img = pygame.Surface(RES)
            self.phase_img.fill(DARKGRAY)
            self.end_img = pygame.Surface(RES)
            self.end_img.fill(YELLOW)

        # Font for text
        self.font = pygame.font.SysFont('Arial', 64, bold=True)

    def load_sounds(self):
        """Carrega todos os sons do jogo."""
        snd_dir = os.path.join(os.path.dirname(__file__), '../assets/sounds')

        def load(filename):
            path = os.path.join(snd_dir, filename)
            try:
                return pygame.mixer.Sound(path)
            except Exception as e:
                print(f"[SOM] Erro ao carregar {filename}: {e}")
                return None

        self.snd_splash = load('Splash.mp3')
        self.snd_background = load('Background.mp3')
        self.snd_fire = load('Fire.wav')
        self.snd_die = load('Die.mp3')
        self.snd_nextlevel = load('Nextlevel.mp3')
        self.snd_door = load('Door.mp3')
        self.snd_powerup = load('Powerup.mp3')
        if self.snd_powerup:
            self.snd_powerup.set_volume(0.2)

    def play_splash_music(self):
        """Toca a música de Splash uma única vez."""
        pygame.mixer.stop()
        if self.snd_splash:
            self.snd_splash.play()

    def play_phase_music(self):
        """Toca o som de passagem de fase uma única vez."""
        pygame.mixer.stop()
        if self.snd_nextlevel:
            self.snd_nextlevel.play()

    def play_background_music(self):
        """Toca a música de fundo em loop."""
        pygame.mixer.stop()
        if self.snd_background:
            self.snd_background.play(loops=-1)


    def new_game(self):
        """Inicializa ou reinicia o jogo/nível."""
        self.enemies = []
        self.sprite_objects = []
        self.map = Map(self)
        try:
            self.map.load_map(self.current_level)
            self.player = Player(self)
            self.renderer = Renderer(self)
            self.raycasting = RayCasting(self)
            self.weapon = Weapon(self)
            self.hud = HUD(self)
            self.state = 'GAME'
            self.play_background_music()
        except Exception as e:
            print(f"Erro ao carregar mapa {self.current_level}: {e}")
            self.state = 'VICTORY'

    def update(self):
        """Atualiza a lógica do jogo dependendo do estado."""
        if self.state == 'GAME':
            self.player.update()
            self.raycasting.update()
            self.weapon.update()
            for enemy in self.enemies:
                enemy.update()
            for sprite in self.sprite_objects:
                sprite.update()
            
            # Update visual effects timers
            if self.shot_timer > 0:
                self.shot_timer -= self.delta_time
            if self.damage_timer > 0:
                self.damage_timer -= self.delta_time
        
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw_text_centered(self, text, y_offset=0, color=WHITE):
        text_surface = self.font.render(text, True, color)
        rect = text_surface.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + y_offset))
        self.screen.blit(text_surface, rect)

    def draw(self):
        """Renderiza o jogo ou telas dependendo do estado."""
        if self.state == 'SPLASH':
            self.screen.blit(self.splash_img, (0, 0))
            # Opcional: Texto "Pressione ESPAÇO"
            #self.draw_text_centered("Pressione ESPAÇO", 200, WHITE)

        elif self.state == 'GAME_OVER':
            self.screen.blit(self.end_img, (0, 0))
            self.draw_text_centered("GAME OVER", 200, (255, 0, 0))
            #self.draw_text_centered("Pressione ESPAÇO para reiniciar", 100, WHITE)
            
        elif self.state == 'VICTORY':
            self.screen.blit(self.end_img, (0, 0))
            self.draw_text_centered("CONGRATULATIONS", 200, WHITE)
            #self.draw_text_centered("Pressione ESPAÇO para Sair/Reiniciar", 100, WHITE)

        elif self.state == 'PHASE':
            self.screen.blit(self.phase_img, (0, 0))
            self.draw_text_centered(f"Phase {self.current_level}", 400, WHITE)
            #self.draw_text_centered("Pressione ENTER para iniciar", 100, WHITE)

        elif self.state == 'GAME':
            self.renderer.draw()
            if self.weapon:
                self.weapon.draw()
            if hasattr(self, 'hud') and self.hud:
                self.hud.draw()
            

    def check_events(self):
        """Verifica eventos de entrada (teclado, sair)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.state == 'SPLASH':
                    if event.key == pygame.K_SPACE:
                        self.state = 'PHASE'
                        self.play_phase_music()
                
                elif self.state == 'PHASE':
                    if event.key == pygame.K_SPACE:
                        self.new_game()
                
                elif self.state == 'GAME':
                    if event.key == pygame.K_SPACE:
                        self.check_interaction()
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.weapon.shoot()
                        if self.snd_fire:
                            self.snd_fire.play()
                
                elif self.state in ['GAME_OVER', 'VICTORY']:
                    if event.key == pygame.K_SPACE:
                        self.current_level = 1
                        self.state = 'SPLASH'
                        self.play_splash_music()
    def check_hit(self):
        """Lógica de acerto (Hitscan)."""
        center_ray_index = NUM_RAYS // 2
        
        # Procura inimigo na mira (metade da tela) com tolerância de FOV
        hit_enemy = None
        min_dist = float('inf')
        
        for enemy in self.enemies:
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            dist = math.hypot(dx, dy)
            
            theta = math.atan2(dy, dx)
            delta = theta - self.player.angle
            delta = (delta + math.pi) % math.tau - math.pi
            
            # Tolerância para o tiro (se ele está perto do centro da visão)
            if abs(delta) < 0.1 and dist < min_dist:
                hit_enemy = enemy
                min_dist = dist
                
        # Hitscan bate na parede
        depth_to_wall = float('inf')
        if self.raycasting and hasattr(self, 'raycasting') and self.raycasting.ray_casting_result:
            depth_to_wall = self.raycasting.ray_casting_result[center_ray_index][0]
            
        if hit_enemy and min_dist < depth_to_wall:
            # Acertou o inimigo (ele estava na frente da parede)
            hit_enemy.health -= PLAYER_SHOT_DAMAGE
            print(f"Acertou Inimigo! Vida do Inimigo: {hit_enemy.health}")
            if hit_enemy.health <= 0:
                print("Inimigo morto!")
                # Drop ammo powerup
                ammo_path = os.path.join('assets/images', '!.png')
                self.sprite_objects.append(Powerup(self, ammo_path, (hit_enemy.x, hit_enemy.y), 'ammo', 10))
                
                self.enemies.remove(hit_enemy)
                self.player.score += 100  # Score por kill
                if self.snd_die:
                    self.snd_die.play()
        else:
            print(f"Bang! Tiro disparado! Parede atingida a {depth_to_wall:.2f}")

        # Trigger visual shooting effect
        self.shot_timer = 50 # millisecond duration

    def check_interaction(self):

        """Verifica se o jogador pode interagir com o objeto à frente."""
        ix, iy = self.player.get_interaction_tile()
        if (ix, iy) in self.map.world_map:
            # Check for Door
            if self.map.world_map[(ix, iy)] == '2':
                 # Open door (remove from map for now)
                 del self.map.world_map[(ix, iy)]
                 if self.snd_door:
                     self.snd_door.play()
            # Check for Exit
            elif self.map.world_map[(ix, iy)] == '9':
                next_level = self.current_level + 1
                next_map_path = os.path.join(
                    os.path.dirname(__file__), '..', 'assets', 'maps', f'{next_level}.txt'
                )
                if os.path.exists(next_map_path):
                    self.current_level = next_level
                    self.state = 'PHASE'
                    self.play_phase_music()
                else:
                    pygame.mixer.stop()
                    self.state = 'VICTORY'

    def trigger_damage(self):
        """Ativa o efeito visual de dano."""
        self.damage_timer = 100 # duration in ms

    def run(self):
        """Loop principal do jogo."""
        while True:
            self.check_events()
            self.draw() # Draw first
            self.update() # Then update (and flip display)

if __name__ == '__main__':
    game = Game()
    game.run()