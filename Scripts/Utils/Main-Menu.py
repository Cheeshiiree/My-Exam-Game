# Menu principal do jogo

import pgzero
from Scripts.Utils.Inputs import get_input

# Desenha a tela do jogo
def draw_menu():
    pgzero.screen.clear()
    pgzero.screen.fill((0, 0, 0))  # Preenche a tela com preto
    pgzero.screen.draw.text("Menu Principal", center=(pgzero.screen.width // 2, pgzero.screen.height // 2 - 50), fontsize=50, color=(255, 255, 255))
    
    

