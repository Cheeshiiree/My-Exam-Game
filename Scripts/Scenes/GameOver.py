# Scripts/Scenes/GameOver.py
# 
# NOTA: Este arquivo foi mantido para referência, mas não está mais sendo usado.
# O sistema foi simplificado para reiniciar diretamente na fase 1 quando o jogador morre.
# As cenas Scene1 e Scene2 agora redirecionam automaticamente para "scene1" ao invés 
# de chamar esta tela de game over.

import math

# --- Constantes ---
WIDTH = 800
HEIGHT = 600

# --- Variáveis ---
animation_timer = 0.0
final_score = 0
enemies_defeated = 0

def init_game_over(score=0, defeated=0):
    """Inicializa a tela de game over."""
    global animation_timer, final_score, enemies_defeated
    animation_timer = 0.0
    final_score = score
    enemies_defeated = defeated

def update_game_over(dt, keyboard):
    """Atualiza a lógica da tela de game over."""
    global animation_timer
    
    animation_timer += dt
    
    # Controles
    if keyboard.r:
        return "scene1"  # Reinicia o jogo
    elif keyboard.escape or keyboard.m:
        return "menu"    # Volta ao menu
    elif keyboard.q:
        return "quit"    # Sai do jogo
    
    return None

def draw_game_over(screen):
    """Desenha a tela de game over."""
    # Fundo vermelho escuro
    screen.clear()
    screen.fill((50, 0, 0))
    
    # Efeito de fade
    fade_alpha = min(255, int(animation_timer * 100))
    
    # Título Game Over
    title_y = 150
    pulse = int(10 * math.sin(animation_timer * 4))
    
    # Sombra
    screen.draw.text("GAME OVER", center=(WIDTH//2 + 5, title_y + 5), color="black", fontsize=64)
    # Título principal
    screen.draw.text("GAME OVER", center=(WIDTH//2, title_y + pulse), color="red", fontsize=64)
    
    # Estatísticas
    stats_y = 280
    stats = [
        f"Pontuação Final: {final_score}",
        f"Inimigos Derrotados: {enemies_defeated}",
        f"Tempo de Jogo: {animation_timer:.1f}s"
    ]
    
    for i, stat in enumerate(stats):
        screen.draw.text(stat, center=(WIDTH//2, stats_y + i * 30), color="white", fontsize=20)
    
    # Controles
    controls_y = 420
    controls = [
        "R - Reiniciar Jogo",
        "M - Voltar ao Menu",
        "ESC - Sair"
    ]
    
    for i, control in enumerate(controls):
        screen.draw.text(control, center=(WIDTH//2, controls_y + i * 30), color="yellow", fontsize=18)
    
    # Mensagem motivacional
    if animation_timer > 3:
        message = "Não desista! Tente novamente!"
        glow = int(50 + 50 * math.sin(animation_timer * 6))
        color = (255, glow, glow)
        screen.draw.text(message, center=(WIDTH//2, HEIGHT - 60), color=color, fontsize=24)
