import os
import pygame
from .settings import *


class HUD:
    """
    HUD retro-style sem fundo, com:
      - Barra de energia gradiente (HP)
      - Ícones de vida (Lifes.ico)
      - Munição como número puro
      - Score estilo terminal
    Todos os elementos têm drop-shadow para legibilidade sobre qualquer cenário.
    """

    def __init__(self, game):
        self.game   = game
        self.screen = game.screen

        pygame.font.init()
        self.font_label = pygame.font.SysFont(HUD_FONT_FAMILY, HUD_FONT_SIZE_LABEL, bold=True)
        self.font_value = pygame.font.SysFont(HUD_FONT_FAMILY, HUD_FONT_SIZE_VALUE, bold=True)

        # Ícone de vida — carrega e escala
        self.life_icon = self._load_life_icon()

        # Superfície totalmente transparente para composição
        self.panel = pygame.Surface((WIDTH, HUD_HEIGHT), pygame.SRCALPHA)

    # ────────────────────────────────────────────────────────────
    #  Carregamento de assets
    # ────────────────────────────────────────────────────────────

    def _load_life_icon(self):
        """Carrega Lifes.ico e redimensiona para HUD_LIFE_ICON_SIZE."""
        try:
            path = os.path.join(os.path.dirname(__file__),
                                '../assets/images/Lifes.ico')
            icon = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(
                icon, (HUD_LIFE_ICON_SIZE, HUD_LIFE_ICON_SIZE))
        except Exception as e:
            print(f"[HUD] Falha ao carregar Lifes.ico: {e}")
            # Fallback: quadrado vermelho com 'V'
            surf = pygame.Surface((HUD_LIFE_ICON_SIZE, HUD_LIFE_ICON_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, (200, 30, 30), surf.get_rect(), border_radius=5)
            return surf

    # ────────────────────────────────────────────────────────────
    #  Helpers de renderização
    # ────────────────────────────────────────────────────────────

    def _lerp_color(self, c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

    def _hp_color(self, ratio):
        if ratio > 0.5:
            return self._lerp_color(HUD_HP_COLOR_MID, HUD_HP_COLOR_HIGH, (ratio - 0.5) * 2)
        else:
            return self._lerp_color(HUD_HP_COLOR_LOW, HUD_HP_COLOR_MID, ratio * 2)

    def _text_with_shadow(self, surface, font, text, color, cx, cy, shadow=True):
        """
        Renderiza texto com drop-shadow centralizado em (cx, cy).
        Retorna o rect do texto.
        """
        tsurf = font.render(text, True, color)
        rect  = tsurf.get_rect(center=(cx, cy))
        if shadow:
            shadow_surf = font.render(text, True, HUD_SHADOW_COLOR)
            surface.blit(shadow_surf, (rect.x + 2, rect.y + 2))
        surface.blit(tsurf, rect)
        return rect

    def _draw_hp_bar(self, cx, cy, w, h, ratio, color):
        """
        Barra de HP sem fundo sólido — apenas a barra preenchida com glow.
        Contorno fino para delimitar sem poluir.
        """
        bar_w = int(w * max(0.0, ratio))
        x     = cx - w // 2
        y     = cy - h // 2

        # Contorno
        pygame.draw.rect(self.panel, (*color, 90), (x - 1, y - 1, w + 2, h + 2), border_radius=5)
        # Fill principal
        if bar_w > 0:
            pygame.draw.rect(self.panel, (*color, 220), (x, y, bar_w, h), border_radius=4)
            # Glow topo
            glow = tuple(min(255, c + 100) for c in color)
            pygame.draw.rect(self.panel, (*glow, 200), (x, y, bar_w, max(2, h // 4)),
                             border_radius=3)

    def _draw_separator(self, x):
        """Linha vertical pontilhada separadora estilo retro."""
        for yy in range(8, HUD_HEIGHT - 8, 8):
            pygame.draw.line(self.panel, (*HUD_SEPARATOR_COLOR, 160),
                             (x, yy), (x, yy + 4), 1)

    # ────────────────────────────────────────────────────────────
    #  Draw principal
    # ────────────────────────────────────────────────────────────

    def draw(self):
        player = self.game.player

        # Limpa com alpha zero (totalmente transparente)
        self.panel.fill((0, 0, 0, 0))

        # ── Divisão em 4 seções iguais ──────────────────────────
        section_w = WIDTH // 4
        mid_y     = HUD_HEIGHT // 2       # centro vertical da barra
        label_y   = mid_y - 18           # y do label (acima do valor)
        value_y   = mid_y + 12           # y do valor (abaixo do label)

        # Centro X de cada seção
        cx = [section_w * i + section_w // 2 for i in range(4)]

        # ============================================================
        #  SEÇÃO 0 — ENERGIA (HP)
        # ============================================================
        hp_ratio = max(0.0, player.health / PLAYER_MAX_HEALTH)
        hp_color  = self._hp_color(hp_ratio)

        # Label
        self._text_with_shadow(self.panel, self.font_label,
                               "HEALTH", HUD_LABEL_COLOR, cx[0], label_y)
        # Barra de HP
        bar_w = section_w - HUD_PADDING * 4
        bar_h = 14
        self._draw_hp_bar(cx[0], value_y - 4, bar_w, bar_h, hp_ratio, hp_color)

        # ============================================================
        #  SEÇÃO 1 — VIDAS (ícones)
        # ============================================================
        self._text_with_shadow(self.panel, self.font_label,
                               "LIVES", HUD_LABEL_COLOR, cx[1], label_y)

        icon_sz   = HUD_LIFE_ICON_SIZE
        gap       = HUD_LIFE_ICON_GAP
        n_lives   = max(0, player.lives)
        total_w   = n_lives * icon_sz + max(0, n_lives - 1) * gap
        ix_start  = cx[1] - total_w // 2
        icon_y    = value_y - icon_sz // 2 + 2

        for i in range(n_lives):
            ix = ix_start + i * (icon_sz + gap)
            self.panel.blit(self.life_icon, (ix, icon_y))

        if n_lives == 0:
            self._text_with_shadow(self.panel, self.font_value,
                                   "☠", (180, 60, 60), cx[1], value_y)

        # ============================================================
        #  SEÇÃO 2 — MUNIÇÃO (somente número)
        # ============================================================
        self._text_with_shadow(self.panel, self.font_label,
                               "AMMO", HUD_LABEL_COLOR, cx[2], label_y)

        ammo_txt = str(max(0, player.ammo))
        # Muda cor conforme nível crítico
        a_ratio  = player.ammo / PLAYER_START_AMMO
        if a_ratio <= 0.2:
            ammo_color = HUD_HP_COLOR_LOW
        elif a_ratio <= 0.4:
            ammo_color = HUD_HP_COLOR_MID
        else:
            ammo_color = HUD_AMMO_COLOR

        self._text_with_shadow(self.panel, self.font_value,
                               ammo_txt, ammo_color, cx[2], value_y)

        # ============================================================
        #  SEÇÃO 3 — SCORE
        # ============================================================
        self._text_with_shadow(self.panel, self.font_label,
                               "SCORE", HUD_LABEL_COLOR, cx[3], label_y)

        score_str = f"{player.score:07d}"
        self._text_with_shadow(self.panel, self.font_value,
                               score_str, HUD_SCORE_COLOR, cx[3], value_y)

        # ── Blit na tela ──
        self.screen.blit(self.panel, (0, 0))
