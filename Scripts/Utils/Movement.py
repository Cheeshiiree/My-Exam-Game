# Scripts/Utils/Movement.py

from Scripts.Utils.SoundManager import sound_manager

# --- Constantes de Física ---
GRAVITY = 800
PLAYER_SPEED = 200
JUMP_STRENGTH = 450

def update_player_movement(player, keyboard, dt, platforms):
    
    # --- Movimento Horizontal ---
    if keyboard.left or keyboard.a:
        player.vx = -PLAYER_SPEED
        player.facing_right = False  # Virada para a esquerda
    elif keyboard.right or keyboard.d:
        player.vx = PLAYER_SPEED
        player.facing_right = True   # Virada para a direita
    else:
        player.vx = 0

    player.x += player.vx * dt
    
    # A câmera segue o player
    
    # --- Lógica de Estado da Animação (Simplificada) ---
    if player.is_grounded:
        if player.vx != 0: # Se está a mover-se no chão
            player.state = 'run'
        else: # Se está parado no chão
            player.state = 'idle'
    else: # Se está no ar
        player.state = 'jump'

    # --- Pulo Duplo ---
    jump_key_pressed = keyboard.up or keyboard.space
    
    if jump_key_pressed and not player.jump_pressed:
        # Pulo normal quando no chão
        if player.is_grounded and player.jump_count < player.max_jumps:
            player.vy = -JUMP_STRENGTH
            player.is_grounded = False
            player.jump_count = 1  # Primeiro pulo usado
            sound_manager.play_sound('player_jump')
        # Pulo duplo no ar
        elif not player.is_grounded and player.jump_count < player.max_jumps:
            player.vy = -JUMP_STRENGTH * 0.8  # Pulo duplo é um pouco mais fraco
            player.jump_count = 2  # Segundo pulo usado
            sound_manager.play_sound('player_jump', volume=0.5)  # Som mais baixo para pulo duplo
    
    # Atualiza estado da tecla de pulo
    player.jump_pressed = jump_key_pressed
    
    # --- Gravidade e Colisão ---
    
    # Posição antiga.
    old_y = player.y
    old_bottom = player.bottom

    # Gravidade e o movimento vertical.
    player.vy += GRAVITY * dt
    player.y += player.vy * dt
    
    # Limite inferior do mundo
    if player.y > 700:  
        player.y = 100
        player.vy = 0
        player.is_grounded = False
    
    player.is_grounded = False
    
    # Verificamos a colisão com cada plataforma.
    for p in platforms:
        if player.colliderect(p):
            
            if (player.vy > 0 and  # Player está caindo
                old_bottom <= p.top + 10 and  # Player estava acima da plataforma 
                abs(player.bottom - p.top) < 50):  # Não está muito longe da plataforma
                
                # Posicionamento padrão na plataforma
                player.bottom = p.top
                player.vy = 0
                
                player.is_grounded = True
                player.jump_count = 0  # Reseta contador de pulos quando toca no chão
                break # Sai do loop quando encontra uma plataforma válida