from .settings import *
from .enemy import Enemy


class Map:
    """
    Classe responsável pelo carregamento e gerenciamento do mapa do jogo.
    Lê arquivos de texto e converte em coordenadas para o mundo do jogo.
    """
    def __init__(self, game):
        self.game = game
        self.mini_map = []
        self.world_map = {}
        self.load_map(1) # Padrão nível 1

    def load_map(self, level_id):
        """
        Carrega o mapa de um arquivo e analisa para um conjunto de coordenadas.
        
        Args:
            level_id (int): O número do nível a ser carregado.
        """
        self.world_map = {} # Reinicia o mapa
        self.mini_map = []
        path = f'assets/maps/{level_id}.txt'
        try:
            with open(path, 'r') as f:
                self.mini_map = f.readlines()
                self.mini_map = [line.strip() for line in self.mini_map]
        except FileNotFoundError:
            raise FileNotFoundError(f"Mapa {path} não encontrado")
            
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value in ['1', '2', '3', '4', '5', '9']: # Parede e texturas
                    self.world_map[(i, j)] = value
                elif value in ['a', 'b', 'c', 'd', 'e', 'f']: # Inimigos
                    if hasattr(self.game, 'enemies'):
                        self.game.enemies.append(Enemy(self.game, i, j, value))

    def draw(self):
        """Opcional: Desenha o mapa 2D para depuração."""
        [pygame.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]
