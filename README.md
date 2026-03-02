# Doom 3D Clone (Python + Pygame) - v1.0

Este é um projeto de um jogo de tiro em primeira pessoa (FPS) estilo retro ("Doom-like"), desenvolvido inteiramente em Python utilizando a biblioteca Pygame. O jogo demonstra a implementação de um motor de **Raycasting** clássico para renderização pseudo-3D.

## 🚀 Funcionalidades da Versão 1.0

- **Motor Gráfico Raycasting**: Renderização de paredes e objetos com perspectiva 3D a partir de um mapa 2D.
- **Texturização**: Suporte completo a texturas para paredes e pisos, proporcionando um visual retro autêntico.
- **Sistema de Níveis**: Carregamento dinâmico de mapas via arquivos de texto, permitindo múltiplos níveis.
- **Interação**: 
  - Portas funcionais (abrem com interação).
  - Interruptores de saída para transição de nível.
- **Controles Clássicos**: Movimentação fluida com teclado (WASD + Setas).

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| **W** / Seta Cima | Mover para Frente |
| **S** / Seta Baixo | Mover para Trás |
| **A** / **D** | *Strafe* (Mover Lateralmente) |
| **<** / **>** | Girar Câmera |
| **Espaço** | Interagir (Abrir Portas / Ativar Saída) |
| **Esc** | Sair do Jogo |

## 🛠️ Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/doom3d-python.git
   cd doom3d-python
   ```

2. **Configure o ambiente virtual (recomendado):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o jogo:**
   ```bash
   python main.py
   ```

## 📂 Estrutura do Projeto

- `src/`: Código fonte do motor e lógica do jogo.
- `assets/`: Recursos gráficos (texturas) e mapas.
- `main.py`: Ponto de entrada da aplicação.

## 📝 Licença

Este projeto é distribuído sob a licença MIT. Sinta-se livre para usar, estudar e modificar.

