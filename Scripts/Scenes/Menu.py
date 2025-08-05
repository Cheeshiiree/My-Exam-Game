# Scripts/Scenes/Menu.py

import math
from Scripts.Utils.InputManager import input_manager
from Scripts.Utils.SoundManager import sound_manager

# --- Constantes ---
WIDTH = 800
HEIGHT = 600

# --- Variáveis do Menu ---
menu_option = 0  # 0 = Jogar, 1 = Música, 2 = Sons, 3 = Sair
menu_options = ["JOGAR", "MÚSICA", "SONS", "SAIR"]
animation_timer = 0.0

# Variável para controle de música (será sincronizada com Main.py)
music_enabled = True

def init_menu():
    """Inicializa o menu principal."""
    global menu_option, animation_timer
    menu_option = 0
    animation_timer = 0.0
    # Reseta o estado das teclas no InputManager
    input_manager.reset()
    
def update_menu(dt, keyboard):
    """Atualiza a lógica do menu."""
    global menu_option, animation_timer
    
    # Atualiza timer de animação
    animation_timer += dt
    
    # Navegação do menu usando InputManager
    if input_manager.is_key_pressed("up", keyboard):
        menu_option = (menu_option - 1) % len(menu_options)
        sound_manager.play_sound('menu_navigate')
        return None
    elif input_manager.is_key_pressed("down", keyboard):
        menu_option = (menu_option + 1) % len(menu_options)
        sound_manager.play_sound('menu_navigate')
        return None
    
    # Seleção da opção
    if input_manager.is_key_pressed("space", keyboard):
        sound_manager.play_sound('menu_select')
        if menu_option == 0:  # Jogar
            return "scene1"
        elif menu_option == 1:  # Música
            return "toggle_music"
        elif menu_option == 2:  # Sons
            return "toggle_sounds"
        elif menu_option == 3:  # Sair
            return "quit"
    
    # Atalhos diretos
    if input_manager.is_key_pressed("1", keyboard):
        sound_manager.play_sound('menu_select')
        return "scene1"
    elif input_manager.is_key_pressed("m", keyboard):
        sound_manager.play_sound('menu_toggle')
        return "toggle_music"
    
    return None

def draw_menu(screen):
    """Desenha o menu principal."""
    # Fundo 
    screen.clear()
    
    screen.blit('mainmenu', (0, 0))
    # # Fundo com gradiente simulado (azul escuro para preto)
    # for y in range(HEIGHT):
    #     intensity = int(50 * (1 - y / HEIGHT))
    #     color = (intensity, intensity, intensity + 20)
    #     screen.draw.line((0, y), (WIDTH, y), color)
    
    # # # Título principal
    # # title_y = 150
    # # title_text = "Demo Plataforma com Pygame Zero"
    
    # # # Efeito de brilho no título
    # # glow_offset = int(5 * math.sin(animation_timer * 3))
    
    # # # Sombra do título
    # # screen.draw.text(title_text, center=(WIDTH//2 + 3, title_y + 3), color="black", fontsize=48)
    # # Título principal
    # # screen.draw.text(title_text, center=(WIDTH//2, title_y), color="gold", fontsize=48)
    # # # Brilho do título
    # # screen.draw.text(title_text, center=(WIDTH//2 + glow_offset, title_y), color="yellow", fontsize=48)
    
    # # # Subtítulo
    # # subtitle = "Plataforma de Aventura"
    # # screen.draw.text(subtitle, center=(WIDTH//2, title_y + 60), color="cyan", fontsize=20)
    
    # Opções do menu
    menu_start_y = 300
    menu_spacing = 60

    # Imagem de fundo das opções
    screen.blit('purple_square', (WIDTH//2 - 130, menu_start_y - 30))
    
    for i, option in enumerate(menu_options):
        y_pos = menu_start_y + (i * menu_spacing)
        
        # Texto especial para as opções de áudio
        if i == 1:  # Opção de música
            music_status = "ON" if music_enabled else "OFF"
            option_text = f"MÚSICA: {music_status}"
        elif i == 2:  # Opção de sons
            sounds_status = "ON" if sound_manager.sounds_enabled else "OFF"
            option_text = f"SONS: {sounds_status}"
        else:
            option_text = option
        
        if i == menu_option:
            # Opção selecionada - com efeito pulsante
            pulse = int(10 * math.sin(animation_timer * 8))
            
            # Indicador de seleção
            screen.draw.text(">>>", (WIDTH//2 - 140, y_pos), color="purple", fontsize=24)
            # screen.draw.text("<<<", (WIDTH//2 + 100, y_pos), color="yellow", fontsize=24)
            # Texto da opção selecionada
            screen.draw.text(option_text, center=(WIDTH//2, y_pos + pulse), color="white", fontsize=32)
        else:
            # Opção não selecionada
            screen.draw.text(option_text, center=(WIDTH//2, y_pos), color="gray", fontsize=28)
    
    # # # Instruções de controle
    # # controls_y = HEIGHT - 140
    # # controls = [
    # #     "CONTROLES:",
    # #     "↑↓ ou W/S - Navegar",
    # #     "ESPAÇO - Selecionar",
    # #     "1 - Ir direto ao jogo",
    # #     "M - Toggle música"
    # # ]
    
    # # for i, control in enumerate(controls):
    # #     color = "white" if i == 0 else "lightgray"
    # #     fontsize = 16 if i == 0 else 14
    # #     screen.draw.text(control, center=(WIDTH//2, controls_y + i * 18), color=color, fontsize=fontsize)
    
    # # # Status da música
    # # music_status = "♪ MÚSICA ATIVA ♪" if music_enabled else "♪ MÚSICA DESATIVADA ♪"
    # # music_color = "lime" if music_enabled else "red"
    # # screen.draw.text(music_status, center=(WIDTH//2, HEIGHT - 60), color=music_color, fontsize=14)
    
    # # # Informações do jogo
    # # info_text = "Colete frutas, derrote inimigos e encontre o portal!"
    # # screen.draw.text(info_text, center=(WIDTH//2, HEIGHT - 40), color="lime", fontsize=16)
    
    # Versão
    version_text = "v1.0 - Anna Beatryz"
    screen.draw.text(version_text, (10, HEIGHT - 20), color="darkgray", fontsize=12)

# Inicializa o menu quando o módulo é carregado
init_menu()
