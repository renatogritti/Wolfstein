"""
config.py — Configurações ajustáveis do jogador e da HUD.
Modifique este arquivo para alterar valores sem tocar no código do jogo.
"""

# ─────────────────────────────────────────────
#  Player defaults
# ─────────────────────────────────────────────
PLAYER_MAX_HEALTH   = 100   # HP máximo do jogador
PLAYER_START_LIVES  = 3     # Vidas iniciais
PLAYER_START_AMMO   = 50    # Munição inicial
PLAYER_START_SCORE  = 0     # Score inicial

# Dano causado por cada tiro do jogador em um inimigo
PLAYER_SHOT_DAMAGE  = 25

# ─────────────────────────────────────────────
#  HUD — dimensões
# ─────────────────────────────────────────────
HUD_HEIGHT          = 72    # Altura total da barra de HUD em pixels
HUD_PADDING         = 20    # Padding interno horizontal entre seções
HUD_LIFE_ICON_SIZE  = 38    # Tamanho dos ícones de vida em pixels
HUD_LIFE_ICON_GAP   = 6     # Espaço entre ícones de vida

# ─────────────────────────────────────────────
#  HUD — cores retro
# ─────────────────────────────────────────────
# Barra de saúde — gradiente dinâmico
HUD_HP_COLOR_HIGH   = ( 60, 255,  80)   # verde néon
HUD_HP_COLOR_MID    = (255, 200,   0)   # âmbar
HUD_HP_COLOR_LOW    = (255,  30,  30)   # vermelho quente

# Separadores
HUD_SEPARATOR_COLOR = (255, 120,   0)   # laranja retro

# Labels (letras acima)
HUD_LABEL_COLOR     = (255, 160,   0)   # laranja-âmbar
# Valores grandes
HUD_VALUE_COLOR     = (255, 255, 200)   # branco-quente
# Score
HUD_SCORE_COLOR     = (255, 210,  50)   # dourado
# Ammo
HUD_AMMO_COLOR      = ( 80, 220, 255)   # ciano elétrico

# Drop shadow dos textos
HUD_SHADOW_COLOR    = (0, 0, 0)

# ─────────────────────────────────────────────
#  HUD — tipografia retro
# ─────────────────────────────────────────────
HUD_FONT_FAMILY     = 'Courier New'     # monospace / terminal feel
HUD_FONT_SIZE_LABEL = 24               # labels (ENERGIA, VIDAS…)
HUD_FONT_SIZE_VALUE = 32               # números grandes
