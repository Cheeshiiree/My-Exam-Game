# Scripts/Scenes/Scene2.py

# --- Importações Essenciais ---
from Scripts.Actors.Player import Player
from Scripts.Actors.Enemies import BlueBird, FireBall, Ghost
from Scripts.Components import Platform, DangerPlatform, Heart, PowerFruit
from Scripts.Utils.Movement import update_player_movement
from Scripts.Utils.SoundManager import sound_manager

# --- Constantes ---
WIDTH = 800   # Resolução HD padrão
HEIGHT = 600  # Resolução HD padrão

# --- Configurações da Câmera ---
camera_x = 0
camera_y = 0

# --- Background Simples ---
background_image = None

# --- Listas de Objetos do Jogo ---
player = None
platforms = []
enemies = []
hearts = []  # Lista de corações coletáveis
power_fruits = []  # Lista de power fruits

# --- Sistema de Mensagens ---
message_text = ""
message_timer = 0.0
message_duration = 3.0  # Mensagem fica 3 segundos na tela

def show_message(text):
    """Exibe uma mensagem na tela por alguns segundos."""
    global message_text, message_timer
    message_text = text
    message_timer = message_duration

def init_scene2(player_from_scene1=None):
    """
    Prepara a Scene2 - Fase do Castelo Flutuante
    """
    global player, platforms, enemies, hearts, power_fruits, camera_x, camera_y, background_image

    # Define o background simples da fase 2
    background_image = 'bg_fase2_orig_big'

    # Se player veio da Scene1, mantém a vida e power-ups
    if player_from_scene1:
        player = player_from_scene1
        player.x = 100  # Reposiciona no início da fase
        player.y = HEIGHT - 100
        player.vx = 0
        player.vy = 0
        player.is_grounded = False
        show_message("BEM-VINDO À FASE 2: CASTELO FLUTUANTE!")
    else:
        # Cria novo player se iniciando direto na Scene2
        player = Player(pos=(100, HEIGHT - 100))

    # Reseta câmera
    camera_x = 0
    camera_y = 0

    # Limpa as listas
    platforms = []
    enemies = []
    hearts = []
    power_fruits = []
    
    # --- CRIAÇÃO DO MAPA DA FASE 2: CASTELO FLUTUANTE ---
    
    # SEÇÃO 1: Entrada do Castelo (0-800)
    # Chão de entrada com tiles de rocha
    for i in range(0, 800, 64):
        platforms.append(Platform('rock_tiles_00', (i, HEIGHT - 32), (64, 32)))
    
    # Torres de entrada com variação de tiles
    for j in range(6):
        tile_type = 'rock_tiles_15' if j % 2 == 0 else 'rock_tiles_30'
        platforms.append(Platform(tile_type, (100, HEIGHT - 80 - j*60), (64, 32)))
        platforms.append(Platform(tile_type, (700, HEIGHT - 80 - j*60), (64, 32)))
    
    # SEÇÃO 2: Plataformas Flutuantes (800-1600)
    # Série de plataformas flutuantes em zigue-zague com tiles variados
    platforms.append(Platform('rock_tiles_45', (900, HEIGHT - 150), (80, 32)))
    platforms.append(Platform('rock_tiles_15', (1100, HEIGHT - 250), (80, 32)))
    platforms.append(Platform('rock_tiles_30', (1300, HEIGHT - 180), (80, 32)))
    platforms.append(Platform('rock_tiles_00', (1500, HEIGHT - 320), (80, 32)))
    
    # Plataformas perigosas flutuantes
    platforms.append(DangerPlatform((1000, HEIGHT - 200), (64, 32)))
    platforms.append(DangerPlatform((1400, HEIGHT - 280), (64, 32)))
    
    # SEÇÃO 3: O Grande Salto (1600-2400)
    # Apenas algumas plataformas muito espaçadas com tiles especiais
    platforms.append(Platform('rock_tiles_45', (1700, HEIGHT - 200), (64, 32)))
    platforms.append(Platform('rock_tiles_30', (1950, HEIGHT - 400), (64, 32)))
    platforms.append(Platform('rock_tiles_15', (2200, HEIGHT - 300), (64, 32)))
    platforms.append(Platform('rock_tiles_00', (2400, HEIGHT - 150), (64, 32)))
    
    # SEÇÃO 4: Torre Final (2400-3200)
    # Chão da área final com tiles de rocha
    for i in range(2400, 3200, 64):
        platforms.append(Platform('rock_tiles_00', (i, HEIGHT - 32), (64, 32)))
    
    # Torre gigante no final com variação de tiles
    for j in range(12):
        tile_left = 'rock_tiles_30' if j % 3 == 0 else 'rock_tiles_15'
        tile_right = 'rock_tiles_45' if j % 2 == 0 else 'rock_tiles_00'
        platforms.append(Platform(tile_left, (2800, HEIGHT - 80 - j*50), (64, 32)))
        platforms.append(Platform(tile_right, (2900, HEIGHT - 100 - j*50), (64, 32)))
    
    # Plataforma final no topo
    platforms.append(Platform('rock_tiles_45', (2850, HEIGHT - 650), (100, 32)))
    
    # --- INIMIGOS DA FASE 2 (Mais Desafiadores) ---
    
    # BlueBirds voadores (mais rápidos)
    enemies.append(BlueBird(pos=(600, HEIGHT - 200)))
    enemies.append(BlueBird(pos=(1200, HEIGHT - 300)))
    enemies.append(BlueBird(pos=(1800, HEIGHT - 250)))
    enemies.append(BlueBird(pos=(2600, HEIGHT - 200)))
    
    # FireBall nas torres
    enemies.append(FireBall(pos=(150, HEIGHT - 200), size=28))
    enemies.append(FireBall(pos=(750, HEIGHT - 200), size=28))
    enemies.append(FireBall(pos=(2850, HEIGHT - 300), size=32))
    
    # Ghost perseguidores (mais agressivos)
    green1 = Ghost(pos=(1000, HEIGHT - 100), size=30)
    green1.set_player_reference(player)
    enemies.append(green1)
    
    green2 = Ghost(pos=(2000, HEIGHT - 200), size=30)
    green2.set_player_reference(player)
    enemies.append(green2)
    
    green3 = Ghost(pos=(2900, HEIGHT - 400), size=32)
    green3.set_player_reference(player)
    enemies.append(green3)
    
    # --- COLETÁVEIS DA FASE 2 ---
    
    # Corações estrategicamente posicionados
    hearts.append(Heart(pos=(200, HEIGHT - 450)))    # Torre de entrada
    hearts.append(Heart(pos=(1200, HEIGHT - 350)))   # Plataformas flutuantes
    hearts.append(Heart(pos=(2000, HEIGHT - 500)))   # Grande salto
    hearts.append(Heart(pos=(2850, HEIGHT - 700)))   # Topo da torre final
    
    # Power Fruits da fase 2
    power_fruits.append(PowerFruit(pos=(800, HEIGHT - 200)))    # Início das flutuantes
    power_fruits.append(PowerFruit(pos=(2100, HEIGHT - 350)))   # Grande salto
    power_fruits.append(PowerFruit(pos=(2950, HEIGHT - 500)))   # Torre final


def create_rock_platform(pos, size, tile_type='rock_tile'):
    """Cria uma plataforma usando os novos tiles de rocha."""
    return Platform(tile_type, pos, size)

def create_varied_rock_platforms():
    """Cria plataformas variadas usando diferentes tiles de rocha."""
    rock_platforms = []
    
    # Alguns tiles de rocha interessantes para variar
    rock_tiles = ['rock_tiles_00', 'rock_tiles_15', 'rock_tiles_30', 'rock_tiles_45']
    
    return rock_platforms


def update_camera():
    """Atualiza a posição da câmera para seguir o player."""
    global camera_x, camera_y
    
    if player:
        # Câmera segue o player horizontalmente
        target_camera_x = player.x - WIDTH // 2
        camera_x = target_camera_x
        
        # Câmera segue o player verticalmente (com zona morta)
        target_camera_y = player.y - HEIGHT // 2
        camera_y = max(-400, min(target_camera_y, 100))  # Permite ver mais para cima

def draw_background(screen):
    """Desenha o background simples da fase."""
    if background_image:
        # Calcula quantas cópias da imagem precisamos para cobrir a tela
        # considerando o movimento da câmera
        screen_width = WIDTH
        bg_width = WIDTH  # Assumindo que a imagem tem a largura da tela
        
        # Desenha o background repetido para cobrir toda a área visível
        start_x = int(-camera_x % bg_width) - bg_width
        for x in range(start_x, screen_width + bg_width, bg_width):
            screen.blit(background_image, (x, 0))

def draw(screen):
    """Função para desenhar tudo na tela com câmera."""
    screen.clear()
    
    # Atualiza câmera
    update_camera()
    
    # Desenha o background simples
    draw_background(screen)
    
    # Desenha todas as plataformas (ajustadas pela câmera)
    for p in platforms:
        if (p.x - camera_x > -100 and p.x - camera_x < WIDTH + 100 and
            p.y - camera_y > -100 and p.y - camera_y < HEIGHT + 100):
            original_x, original_y = p.x, p.y
            p.x -= camera_x
            p.y -= camera_y
            p.draw()
            p.x, p.y = original_x, original_y
    
    # Desenha o player (ajustado pela câmera)
    if player:
        original_x, original_y = player.x, player.y
        player.x -= camera_x
        player.y -= camera_y
        player.draw()
        player.x, player.y = original_x, original_y
    
    # Desenha inimigos
    for e in enemies:
        if (e.x - camera_x > -50 and e.x - camera_x < WIDTH + 50 and
            e.y - camera_y > -50 and e.y - camera_y < HEIGHT + 50):
            original_x, original_y = e.x, e.y
            e.x -= camera_x
            e.y -= camera_y
            e.draw()
            e.x, e.y = original_x, original_y
    
    # Desenha coletáveis
    for h in hearts:
        if (h.x - camera_x > -50 and h.x - camera_x < WIDTH + 50 and
            h.y - camera_y > -50 and h.y - camera_y < HEIGHT + 50):
            original_x, original_y = h.x, h.y
            h.x -= camera_x
            h.y -= camera_y
            h.draw()
            h.x, h.y = original_x, original_y
    
    for pf in power_fruits:
        if (pf.x - camera_x > -50 and pf.x - camera_x < WIDTH + 50 and
            pf.y - camera_y > -50 and pf.y - camera_y < HEIGHT + 50):
            original_x, original_y = pf.x, pf.y
            pf.x -= camera_x
            pf.y -= camera_y
            pf.draw()
            pf.x, pf.y = original_x, original_y
    
    # UI da Fase 2
    if player:
        draw_health_ui(screen)
        
        phase_text = "FASE 2: CASTELO FLUTUANTE"
        screen.draw.text(phase_text, (10, 10), color="white", fontsize=24)
        
        controls_text = "Meta: Chegue ao topo da torre final!"
        screen.draw.text(controls_text, (10, HEIGHT - 30), color="yellow")
    
    # Mensagens temporárias
    if message_timer > 0:
        msg_x = WIDTH - 20
        msg_y = HEIGHT - 20
        # Texto menor, alinhado no canto inferior direito
        screen.draw.text(
            message_text,
            topright=(msg_x, msg_y),
            color="black",
            fontsize=28
        )


def draw_health_ui(screen):
    """Desenha a interface de vida do player"""
    if not player:
        return
    
    heart_start_x = 10
    heart_start_y = 60
    heart_spacing = 36
    
    for i in range(player.max_health):
        heart_x = heart_start_x + (i * heart_spacing)
        heart_y = heart_start_y
        
        if i < player.health:
            screen.draw.filled_circle((heart_x + 16, heart_y + 16), 12, (255, 50, 50))
        else:
            screen.draw.circle((heart_x + 16, heart_y + 16), 12, (100, 100, 100))
    
    health_text = f"Vida: {player.health}/{player.max_health}"
    screen.draw.text(health_text, (heart_start_x, heart_start_y + 40), color="white")
    
    # Indicador de invencibilidade
    if player.invincible:
        invincible_text = f"INVENCÍVEL: {player.invincible_timer:.1f}s"
        screen.draw.text(invincible_text, (heart_start_x + 25, heart_start_y + 100), color="yellow")
    
    # Indicador de power-up
    if player.has_power:
        power_text = f"PODER ATIVO: {player.power_timer:.1f}s"
        screen.draw.text(power_text, (heart_start_x + 200, heart_start_y + 80), color="gold")
        screen.draw.text("Inimigos vulneráveis!", (heart_start_x + 200, heart_start_y + 100), color="white")

def update(dt, keyboard):
    global message_timer
    
    # Atualiza timer das mensagens
    if message_timer > 0:
        message_timer -= dt
    
    if player and player.is_alive():
        # Movimento e animação do player
        update_player_movement(player, keyboard, dt, platforms)
        player.update_animation(dt)
        
        # Verifica colisão com plataformas perigosas
        for p in platforms:
            if isinstance(p, DangerPlatform) and player.colliderect(p):
                if player.take_damage():
                    show_message("ESPINHOS DO CASTELO!")
                break
        
        # Verifica colisão com inimigos
        enemies_to_remove = []
        for e in enemies:
            if player.collides_with(e):
                player_rect = player.get_collision_rect()
                enemy_rect = e.get_collision_rect()
                
                if (player.vy > 0 and player_rect.centery < enemy_rect.centery and 
                    abs(player_rect.centerx - enemy_rect.centerx) < enemy_rect.width * 0.8):
                    e.start_death()
                    player.vy = -200
                    show_message(f"{e.__class__.__name__} eliminado!")
                    sound_manager.play_sound('enemy_die')
                    enemies_to_remove.append(e)
                    break
                elif player.has_power and e.is_vulnerable:
                    e.start_death()
                    show_message(f"{e.__class__.__name__} eliminado pelo poder!")
                    sound_manager.play_sound('enemy_die')
                    enemies_to_remove.append(e)
                    break
                elif not e.is_vulnerable:
                    if player.take_damage():
                        show_message(f"Atingido por {e.__class__.__name__}!")
                        sound_manager.play_sound('player_hurt')
                        if e.x < player.x:
                            player.x += 20
                        else:
                            player.x -= 20
                    break
        
        # Remove inimigos mortos
        for e in enemies_to_remove:
            if e in enemies:
                enemies.remove(e)
        
        # Verifica coleta de corações
        for h in hearts[:]:
            if player.colliderect(h):
                if player.heal():
                    show_message("Vida recuperada!")
                    sound_manager.play_sound('collect_heart')
                    hearts.remove(h)
                elif player.health == player.max_health:
                    show_message("Vida no máximo!")
                    sound_manager.play_sound('collect_heart')
                    hearts.remove(h)
        
        # Verifica coleta de power fruits
        for pf in power_fruits[:]:
            if player.colliderect(pf):
                player.activate_power()
                show_message("PODER ATIVADO!")
                sound_manager.play_sound('collect_power')
                power_fruits.remove(pf)
                
                for e in enemies:
                    e.make_vulnerable()
        
        # Verifica se chegou ao final da fase (topo da torre)
        if player.x > 2850 and player.y < HEIGHT - 700:
            show_message("PARABÉNS! VOCÊ CONCLUIU A DEMO")
            sound_manager.play_sound('level_complete')
            # Não retorna nada - permanece na tela mostrando a vitória
            
    
    elif player and not player.is_alive():
        # Game Over - Redireciona diretamente para o início da fase 1
        sound_manager.play_sound('player_die')
        return "scene1"

    # Atualiza inimigos
    enemies_to_remove = []
    for e in enemies:
        should_remove = e.update(dt)
        if should_remove:
            enemies_to_remove.append(e)
    
    for e in enemies_to_remove:
        if e in enemies:
            enemies.remove(e)
    
    # Remove vulnerabilidade quando power-up acaba
    if player and not player.has_power:
        for e in enemies:
            if e.is_vulnerable:
                e.make_invulnerable()
    
    # Atualiza coletáveis
    for h in hearts:
        h.update(dt)
    for pf in power_fruits:
        pf.update(dt)
    
    # Atualiza câmera
    if player and player.is_alive():
        update_camera()

    # Verifica tecla para voltar à Scene1 (para teste)
    if keyboard.K_1:
        return "scene1"
    
    # Verifica tecla para voltar ao menu
    if keyboard.escape:
        return "menu"  # Sinal para voltar à Scene1
    
    return None  # Continua na Scene2
