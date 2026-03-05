# Wolfstein - Motor Raycasting Clássico v1.0
**Autor: Renato Gritti**

Bem-vindo ao Wolfstein, um clone de FPS retrô desenvolvido em Python. Este projeto utiliza a biblioteca **Pygame** para implementar um motor gráfico de **Raycasting**, criando uma experiência pseudo-3D inspirada nos clássicos dos anos 90.

---

## 🎮 Funcionalidades Principais
- **Renderização Retro**: Paredes, portas e objetos (sprites) renderizados com profundidade e perspectiva.
- **Combat Feedback**: Animações de tiro no centro da tela e lampejo vermelho ao receber dano.
- **Múltiplos Níveis**: Três fases completas com progressão automática via interruptores de saída.
- **IA de Inimigos**: Inimigos com linha de visão (Line-of-Sight), evitando ataques através de paredes.
- **Sistema de HUD**: Interface completa exibindo Saúde, Vidas, Munição e Score.

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior.
- Pip (gerenciador de pacotes do Python).

### Passos
1. **Prepare o ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # ou
   .venv\Scripts\activate     # Windows
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o jogo:**
   ```bash
   python main.py
   ```

## ⌨️ Controles
| Tecla | Ação |
|-------|------|
| **W/S** | Mover para Frente / Trás |
| **A/D** | Strafe (Mover Lateralmente) |
| **Setas** | Rotacionar Câmera |
| **Ctrl** | Atirar |
| **Espaço** | Interagir (Portas / Próxima Fase) |
| **Esc** | Sair do Jogo |

---

## 🏗️ Guia para Desenvolvedores

### Estrutura de Pastas
- `src/`: Lógica central (Player, Raycasting, Renderer, Enemy).
- `assets/maps/`: Arquivos `.txt` que definem os layouts das fases.
- `assets/textures/`: Imagens de paredes e decorações.
- `assets/images/`: GIFs e PNGs de inimigos e itens.
- `assets/sounds/`: Efeitos sonoros e trilha sonora.

### Mapeamento de Assets (Arquivos de Mapa)
Os mapas funcionam através de caracteres específicos em uma grade de texto:
- `1`: Parede padrão.
- `2`: Porta (interativa).
- `3, 4, 5`: Objetos de decoração.
- `9`: Saída de fase.
- `a, b, c, d, e`: Tipos variados de inimigos.
- `f`: Inimigo Boss (chefe).
- `@`: Powerup de Saúde (+10%).
- `!`: Powerup de Munição (+10).

### Dicas de Extensão
Para adicionar novas texturas de parede ou inimigos, basta atualizar os dicionários de carregamento nos módulos `renderer.py` ou `enemy.py`.

---

## 📝 Contribuição e Licença
Desenvolvido por **Renato Gritti**. Este projeto é de código aberto sob a licença MIT. Sinta-se à vontade para fork e modificação para fins educacionais.

