# Scripts/Scenes/Scene1.py

# --- Importações Essenciais ---
from Scripts.Actors.Player import Player
from Scripts.Actors.Enemies import BlueBird, FireBall, Ghost
from Scripts.Components import Platform, DangerPlatform, Heart, PowerFruit  
from Scripts.Utils.Movement import update_player_movement
from Scripts.Utils.SoundManager import sound_manager

# --- Constantes (copiadas do Main.py) ---
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

# Portal no final da fase
portal = None

# --- Sistema de Mensagens ---
message_text = ""
message_timer = 0.0
message_duration = 3.0  # Mensagem fica 3 segundos na tela

def show_message(text):
    """Exibe uma mensagem na tela por alguns segundos."""
    global message_text, message_timer
    message_text = text
    message_timer = message_duration

def init_game():
    """
    Prepara o jogo - Primeira fase
    """
    global player, platforms, enemies, hearts, power_fruits, portal, camera_x, camera_y, background_image

    # Define o background simples da fase 1
    background_image = 'bg_fase1_orig_big'

    # Cria o jogador numa posição inicial
    player = Player(pos=(100, HEIGHT - 100))

    # Reseta câmera
    camera_x = 0
    camera_y = 0

    # Limpa as listas
    platforms = []
    enemies = []
    hearts = []
    power_fruits = []
    
    # Cria o portal no final da fase 
    try:
        from pgzero.actor import Actor
        portal = Actor('portal', pos=(3050, HEIGHT - 100))
    except ImportError:
        # Fallback - cria um objeto simples se não conseguir importar
        class SimplePortal:
            def __init__(self, pos):
                self.x, self.y = pos
                self.width, self.height = 64, 64
            def colliderect(self, other):
                return (abs(self.x - other.x) < 32 and abs(self.y - other.y) < 32)
            def draw(self):
                pass  # Será implementado no draw principal
        portal = SimplePortal((3050, HEIGHT - 100))
    
    # --- Criação do Mapa Extenso ---
    
    # SEÇÃO 1: Área inicial (0-1200) 
    # Chão principal da área inicial
    for i in range(0, 1200, 64):
        platforms.append(Platform('normal', (i, HEIGHT - 32), (64, 32)))
    
    # Primeira plataforma flutuante com buraco
    platforms.append(Platform('normal', (200, HEIGHT - 250), (64, 32)))
    platforms.append(Platform('normal', (400, HEIGHT - 300), (64, 32)))
    platforms.append(Platform('normal', (600, HEIGHT - 200), (64, 32)))
    
    # SEÇÃO 2: Desafio com buracos (1200-1800)
    # Chão com buracos
    platforms.append(Platform('normal', (1200, HEIGHT - 32), (64, 32)))
    platforms.append(Platform('normal', (1264, HEIGHT - 32), (64, 32)))
    # BURACO de 192px aqui (maior)
    platforms.append(Platform('normal', (1520, HEIGHT - 32), (64, 32)))
    platforms.append(Platform('normal', (1584, HEIGHT - 32), (64, 32)))
    
    # Plataformas para atravessar o buraco
    platforms.append(Platform('normal', (1350, HEIGHT - 150), (48, 24)))
    platforms.append(Platform('normal', (1420, HEIGHT - 200), (48, 24)))
    
    # SEÇÃO 3: Área com espinhos (1800-2400)
    for i in range(1800, 2400, 64):
        platforms.append(Platform('normal', (i, HEIGHT - 32), (64, 32)))
    
    # Plataformas perigosas (espinhos)
    platforms.append(DangerPlatform((1900, HEIGHT - 64), (64, 32)))
    platforms.append(DangerPlatform((2100, HEIGHT - 64), (64, 32)))
    platforms.append(DangerPlatform((2300, HEIGHT - 64), (64, 32)))
    
    # Plataformas altas para evitar espinhos
    platforms.append(Platform('normal', (1850, HEIGHT - 250), (64, 32)))
    platforms.append(Platform('normal', (2000, HEIGHT - 300), (64, 32)))
    platforms.append(Platform('normal', (2150, HEIGHT - 250), (64, 32)))
    platforms.append(Platform('normal', (2350, HEIGHT - 200), (64, 32)))
    
    # SEÇÃO 4: Área alta para testar câmera (2400-3000)
    for i in range(2400, 3000, 64):
        platforms.append(Platform('normal', (i, HEIGHT - 32), (64, 32)))
    
    # Torre de plataformas (mais alta para tela maior)
    for j in range(8):
        platforms.append(Platform('normal', (2500, HEIGHT - 100 - j*80), (64, 32)))
        platforms.append(Platform('normal', (2650, HEIGHT - 130 - j*80), (64, 32)))
    
    # Plataformas bem altas
    platforms.append(Platform('normal', (2800, HEIGHT - 500), (64, 32)))
    platforms.append(Platform('normal', (2950, HEIGHT - 600), (64, 32)))
    
    # --- Criação dos Inimigos ---
    # BlueBird (triângulos azuis) em diferentes seções
    enemies.append(BlueBird(pos=(500, HEIGHT - 200)))
    enemies.append(BlueBird(pos=(800, HEIGHT - 150)))
    enemies.append(BlueBird(pos=(1400, HEIGHT - 250)))
    enemies.append(BlueBird(pos=(2000, HEIGHT - 200)))
    enemies.append(BlueBird(pos=(2600, HEIGHT - 300)))
    
    # FireBall (bolas de fogo) espalhadas
    enemies.append(FireBall(pos=(700, HEIGHT - 200), size=24))
    enemies.append(FireBall(pos=(1600, HEIGHT - 300), size=20))
    enemies.append(FireBall(pos=(2200, HEIGHT - 250), size=28))
    enemies.append(FireBall(pos=(2800, HEIGHT - 400), size=26))
    
    # Ghost (fantasmas perseguidores)
    green1 = Ghost(pos=(400, HEIGHT - 250), size=22)
    green1.set_player_reference(player)
    enemies.append(green1)
    
    green2 = Ghost(pos=(1300, HEIGHT - 200), size=24)
    green2.set_player_reference(player)
    enemies.append(green2)
    
    green3 = Ghost(pos=(2100, HEIGHT - 300), size=26)
    green3.set_player_reference(player)
    enemies.append(green3)
    
    green4 = Ghost(pos=(2700, HEIGHT - 350), size=28)
    green4.set_player_reference(player)
    enemies.append(green4)
    
    # --- Criação dos Corações Coletáveis ---
    # Corações espalhados pelo mapa para o player coletar
    hearts.append(Heart(pos=(300, HEIGHT - 350)))    # Seção 1
    hearts.append(Heart(pos=(650, HEIGHT - 250)))    # Seção 1
    hearts.append(Heart(pos=(1450, HEIGHT - 250)))   # Seção 2 (perto do buraco)
    hearts.append(Heart(pos=(1950, HEIGHT - 400)))   # Seção 3 (área alta, longe dos espinhos)
    hearts.append(Heart(pos=(2250, HEIGHT - 350)))   # Seção 3
    hearts.append(Heart(pos=(2550, HEIGHT - 400)))   # Seção 4 (na torre)
    hearts.append(Heart(pos=(2850, HEIGHT - 550)))   # Seção 4 (bem alto)
    
    # --- Criação das Power Fruits ---
    # Power fruits espalhadas estrategicamente pelo mapa
    power_fruits.append(PowerFruit(pos=(900, HEIGHT - 300)))    # Seção 1
    power_fruits.append(PowerFruit(pos=(1700, HEIGHT - 200)))   # Seção 2
    power_fruits.append(PowerFruit(pos=(2400, HEIGHT - 350)))   # Seção 3/4


def update_camera():
    """Atualiza a posição da câmera para seguir o player."""
    global camera_x, camera_y
    
    if player:
        # Câmera segue o player horizontalmente
        target_camera_x = player.x - WIDTH // 2
        camera_x = target_camera_x
        
        # Câmera segue o player verticalmente (com zona morta)
        target_camera_y = player.y - HEIGHT // 2
        camera_y = max(-200, min(target_camera_y, 50))

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
        # Só desenha se estiver visível na tela
        if (p.x - camera_x > -100 and p.x - camera_x < WIDTH + 100 and
            p.y - camera_y > -100 and p.y - camera_y < HEIGHT + 100):
            # Salva posição original
            original_x, original_y = p.x, p.y
            # Move para posição da câmera
            p.x -= camera_x
            p.y -= camera_y
            p.draw()
            # Restaura posição original
            p.x, p.y = original_x, original_y
    
    # Desenha o player (ajustado pela câmera)
    if player:
        original_x, original_y = player.x, player.y
        player.x -= camera_x
        player.y -= camera_y
        player.draw()
        player.x, player.y = original_x, original_y
    
    # Desenha cada inimigo (ajustado pela câmara)
    for e in enemies:
        # Só desenha se estiver visível
        if (e.x - camera_x > -50 and e.x - camera_x < WIDTH + 50 and
            e.y - camera_y > -50 and e.y - camera_y < HEIGHT + 50):
            original_x, original_y = e.x, e.y
            e.x -= camera_x
            e.y -= camera_y
            e.draw()
            e.x, e.y = original_x, original_y
    
    # Desenha corações coletáveis (ajustado pela câmera)
    for h in hearts:
        # Só desenha se estiver visível
        if (h.x - camera_x > -50 and h.x - camera_x < WIDTH + 50 and
            h.y - camera_y > -50 and h.y - camera_y < HEIGHT + 50):
            original_x, original_y = h.x, h.y
            h.x -= camera_x
            h.y -= camera_y
            h.draw()
            h.x, h.y = original_x, original_y
    
    # Desenha power fruits (ajustado pela câmera)
    for pf in power_fruits:
        # Só desenha se estiver visível
        if (pf.x - camera_x > -50 and pf.x - camera_x < WIDTH + 50 and
            pf.y - camera_y > -50 and pf.y - camera_y < HEIGHT + 50):
            original_x, original_y = pf.x, pf.y
            pf.x -= camera_x
            pf.y -= camera_y
            pf.draw()
            pf.x, pf.y = original_x, original_y
    
    # Desenha portal (ajustado pela câmera)
    if portal and (portal.x - camera_x > -50 and portal.x - camera_x < WIDTH + 50):
        original_x, original_y = portal.x, portal.y
        portal.x -= camera_x
        portal.y -= camera_y
        portal.draw()
        portal.x, portal.y = original_x, original_y
    
    # HUD de vida (não afetado pela câmera)
    if player:
        draw_health_ui(screen)
    
    # UI/Debug (não afetado pela câmera)
    if player:
        # controls_text = "Controles: SETAS/WASD = mover, ESPAÇO/SETA CIMA = pular, ESC = menu"
        # screen.draw.text(controls_text, (10, HEIGHT - 30), color="white")
        
        phase_text = "FASE 1"
        screen.draw.text(phase_text, (10, 10), color="white", fontsize=24)
    
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
    """Desenha a interface de vida do player."""
    if not player:
        return
    
    # Posição inicial dos corações na HUD
    heart_start_x = 10
    heart_start_y = 60
    heart_size = 32
    heart_spacing = 36
    
    # Desenha corações para mostrar a vida atual
    for i in range(player.max_health):
        heart_x = heart_start_x + (i * heart_spacing)
        heart_y = heart_start_y
        
        if i < player.health:
            # Coração cheio (vermelho)
            screen.draw.filled_circle((heart_x + 16, heart_y + 16), 12, (255, 50, 50))
        else:
            # Coração vazio (contorno cinza)
            screen.draw.circle((heart_x + 16, heart_y + 16), 12, (100, 100, 100))
    
    # Texto da vida
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
    """Função para atualizar a lógica do jogo."""
    global message_timer
            # if player.x > 2950:
                # # Efeito piscante
                # import math
                # alpha = int(128 + 127 * math.sin(message_timer * 10))
                # portal_instruction = "ENTRE NO PORTAL DOURADO!"
                # screen.draw.text(portal_instruction, center=(WIDTH // 2, HEIGHT // 2 + 50), color="gold", fontsize=24)
                
                # # Indicador visual de direção
                # arrow_text = "→ → →"
                # screen.draw.text(arrow_text, (player.x - camera_x + 50, player.y - camera_y - 50), color="yellow", fontsize=30)

def update(dt, keyboard):
    """Função para atualizar a lógica do jogo."""
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
                    show_message("OUCH! Você tocou nos espinhos!")
                break
        
        # Verifica colisão com inimigos
        enemies_to_remove = []
        for e in enemies:
            if player.collides_with(e):
                # Verifica se o player está pulando em cima do inimigo
                player_rect = player.get_collision_rect()
                enemy_rect = e.get_collision_rect()
                
                if (player.vy > 0 and player_rect.centery < enemy_rect.centery and 
                    abs(player_rect.centerx - enemy_rect.centerx) < enemy_rect.width * 0.8):
                    # Player pulou em cima do inimigo
                    e.start_death()
                    player.vy = -200  # Pequeno pulo após matar
                    show_message(f"{e.__class__.__name__} eliminado!")
                    sound_manager.play_sound('enemy_die')
                    enemies_to_remove.append(e)
                    break
                elif player.has_power and e.is_vulnerable:
                    # Player com power-up tocou inimigo vulnerável
                    e.start_death()
                    show_message(f"{e.__class__.__name__} eliminado pelo poder!")
                    sound_manager.play_sound('enemy_die')
                    enemies_to_remove.append(e)
                    break
                elif not e.is_vulnerable:
                    # Colisão normal - player toma dano
                    if player.take_damage():
                        show_message(f"Você foi atingido por {e.__class__.__name__}!")
                        sound_manager.play_sound('player_hurt')
                        # Pequeno knockback
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
        for h in hearts[:]:  # Copia a lista para poder remover durante iteração
            if player.colliderect(h):
                if player.heal():
                    show_message("Vida recuperada!")
                    sound_manager.play_sound('collect_heart')
                    hearts.remove(h)
                elif player.health == player.max_health:
                    show_message("Vida no máximo!")
                    sound_manager.play_sound('collect_heart')
                    hearts.remove(h)  # Remove mesmo se vida estiver cheia
        
        # Verifica coleta de power fruits
        for pf in power_fruits[:]:  # Copia a lista para poder remover durante iteração
            if player.colliderect(pf):
                player.activate_power()
                show_message("PODER ATIVADO! Inimigos vulneráveis!")
                sound_manager.play_sound('collect_power')
                power_fruits.remove(pf)
                
                # Torna todos os inimigos vulneráveis
                for e in enemies:
                    e.make_vulnerable()
        
        # TRIGGER: Verifica se tocou no portal
        if portal and player.colliderect(portal):
            show_message("PARABÉNS! FASE 1 CONCLUÍDA! ENTRANDO NA FASE 2...")
            sound_manager.play_sound('portal_enter')
            return "scene2"  # Sinal para trocar de cena
        
        # Se o player cair muito, volta ao início
        if player.y > 700: 
            if player.take_damage():
                show_message("Você caiu! Cuidado!")
            player.x = 100
            player.y = HEIGHT - 100
            player.vy = 0
    
    elif player and not player.is_alive():
        # Game Over - Redireciona diretamente para o início da fase 1
        sound_manager.play_sound('player_die')
        init_game()  # Reinicia automaticamente
        return None

    # Atualiza lógica de cada inimigo
    enemies_to_remove = []
    for e in enemies:
        should_remove = e.update(dt)
        if should_remove:
            enemies_to_remove.append(e)
    
    # Remove inimigos que terminaram de morrer
    for e in enemies_to_remove:
        if e in enemies:
            enemies.remove(e)
    
    # Se o power-up acabou, remove vulnerabilidade dos inimigos
    if player and not player.has_power:
        for e in enemies:
            if e.is_vulnerable:
                e.make_invulnerable()
    
    # Atualiza corações (animação de flutuação)
    for h in hearts:
        h.update(dt)
    
    # Atualiza power fruits (animação de rotação)
    for pf in power_fruits:
        pf.update(dt)
    
    # Atualiza câmera apenas se player estiver vivo
    if player and player.is_alive():
        update_camera()
    
    # Verifica tecla para ir direto à Scene2 (para teste)
    if keyboard.K_2:
        return "scene2"
    
    # Verifica tecla para voltar ao menu
    if keyboard.escape:
        return "menu"
    
    return None  # Continua na Scene1

# --- Início do Jogo ---
init_game()