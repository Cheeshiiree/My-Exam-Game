# main.py

import pgzrun
# Importamos as cenas
from Scripts.Scenes import Scene1, Scene2, Menu
from Scripts.Utils.SoundManager import sound_manager

# Configurações da Janela diretamente no Main
WIDTH = 800  # Resolução HD
HEIGHT = 600  # Resolução HD
TITLE = "Demo Plataforma com Pygame Zero"

# Sistema de gerenciamento de cenas
current_scene = "menu"  # Começa no menu principal

# Controle de música
music_enabled = True
music_playing = False

def toggle_background_music():
    """Liga/desliga a música de fundo"""
    global music_enabled, music_playing
    
    music_enabled = not music_enabled
    
    if music_enabled and not music_playing:
        try:
            music.play('background_music')
            music.set_volume(0.4)
            music_playing = True
            
        except Exception as e:
            print(f"Erro ao tocar música: {e}")
    elif not music_enabled and music_playing:
        try:
            music.stop()
            music_playing = False
            
        except Exception as e:
            print(f"Erro ao parar música: {e}")

def init_background_music():
    """Inicializa a música de fundo"""
    global music_playing, music_enabled
    
    if music_enabled and not music_playing:
        try:
            music.play('background_music')
            music.set_volume(0.4)
            music_playing = True
            
        except Exception as e:
            print(f"Erro ao inicializar música: {e}")
            music_playing = False

def draw():
    global current_scene
    
    # Configura o sound manager na primeira execução
    if not hasattr(sound_manager, '_pgzero_sounds_set'):
        try:
            # No PgZero, 'sounds' é uma variável global disponível
            sound_manager._pgzero_sounds = sounds
            sound_manager._pgzero_sounds_set = True
        except NameError:
            # sounds ainda não está disponível
            pass
    
    if current_scene == "menu":
        Menu.draw_menu(screen)
    elif current_scene == "scene1":
        Scene1.draw(screen)
    elif current_scene == "scene2":
        Scene2.draw(screen)

def update(dt):
    global current_scene
    
    scene_transition = None
    
    if current_scene == "menu":
        scene_transition = Menu.update_menu(dt, keyboard)
    elif current_scene == "scene1":
        scene_transition = Scene1.update(dt, keyboard)
    elif current_scene == "scene2":
        scene_transition = Scene2.update(dt, keyboard)
    
    # Verifica se houve solicitação de mudança de cena
    if scene_transition == "scene1":
        if current_scene == "menu":
            # Do menu para o jogo - inicializa Scene1
            Scene1.init_game()
        else:
            # Volta para Scene1 de outra cena (reinicia)
            Scene1.init_game()
        current_scene = "scene1"
    elif scene_transition == "scene2":
        # Transição da Scene1 para Scene2 - passa o player
        player_from_scene1 = Scene1.player
        Scene2.init_scene2(player_from_scene1)
        current_scene = "scene2"
    elif scene_transition == "menu":
        # Volta ao menu
        Menu.init_menu()
        current_scene = "menu"
    elif scene_transition == "quit":
        # Para a música antes de sair
        if music_playing:
            try:
                music.stop()
            except:
                pass
        # Sai do jogo
        exit()
    elif scene_transition == "toggle_music":
        # Toggle da música
        toggle_background_music()
        # Sincroniza o estado com o Menu
        Menu.music_enabled = music_enabled
    elif scene_transition == "toggle_sounds":
        # Toggle dos efeitos sonoros
        sound_manager.toggle_sounds()
        # Toca um som de confirmação se os sons estiverem ligados
        sound_manager.play_sound('menu_toggle')


init_background_music()

pgzrun.go()