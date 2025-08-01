# Classe responsável pelo movimento do Player

import pgzero
import math
from Scripts.Utils.Inputs import get_input

# Função que controla o pulo
isJumping = False
jumpHeight = 0

# Verifica se o player está em contato com o chão
def is_on_ground(player):
    return player.y >= player.ground_level

# O Jogador só pode pular se estiver em contato com o chão ou dar um unico pulo duplo
# Isso garante que o jogador não possa pular infinitamente no ar
def can_jump(player):
    return is_on_ground(player) or (player.double_jump_available and not isJumping)

def jump(player): # Inicia o pulo do player
    global isJumping, jumpHeight
    if can_jump(player):
        isJumping = True
        jumpHeight = 0
        player.velocity_y = -player.jump_speed
        player.double_jump_available = True
        player.is_jumping = True

def update_jump(player, dt):
    global isJumping, jumpHeight
    if isJumping: # Se o player estiver pulando
        jumpHeight += player.jump_speed * dt # Aumenta a altura do pulo
        player.y += player.velocity_y * dt # Atualiza a posição do player com base na velocidade vertical
        player.velocity_y += player.gravity * dt # Aplica a gravidade na velocidade vertical

        if jumpHeight >= player.max_jump_height or is_on_ground(player): # Se a altura do pulo for maior que a altura máxima ou se o player estiver no chão
            isJumping = False # Para o pulo
            jumpHeight = 0
            player.is_jumping = False
            player.double_jump_available = False
            player.velocity_y = 0
            player.y = max(player.y, player.ground_level)  # Garante que o player permaneça no nível do chão

# Função que controla o movimento horizontal do player
def move_player(player, dt):
    inputs = get_input()  # Obtém os inputs do jogador

    if inputs['left']:  # Se o jogador pressionar a tecla esquerda
        player.x -= player.speed * dt  # Move o player para a esquerda
        player.direction = 'left'  # Define a direção do player como esquerda

    if inputs['right']:  # Se o jogador pressionar a tecla direita
        player.x += player.speed * dt  # Move o player para a direita
        player.direction = 'right'  # Define a direção do player como direita

    if inputs['jump']:  # Se o jogador pressionar a tecla de pulo
        jump(player)  # Chama a função de pulo

    update_jump(player, dt)  # Atualiza o estado do pulo

# Função que atualiza a posição do player
def update_player(player, dt):
    move_player(player, dt)  # Move o player com base nos inputs
    player.x = max(0, min(player.x, player.screen_width))  # Garante que o player não saia da tela
    player.y = max(player.ground_level, player.y)  # Garante que o player não saia do chão
    player.rect.topleft = (player.x, player.y)  # Atualiza o retângulo de colisão do player

# Função que desenha o player na tela e atualiza sua animação
