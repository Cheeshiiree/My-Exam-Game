# Scripts/Actors/Enemies.py

from pgzero.actor import Actor
from pygame import Rect
import random
import math

class BaseEnemy(Actor):
    """Classe base para todos os inimigos com funcionalidades comuns."""
    def __init__(self, image, white_image, **kwargs):
        super().__init__(image, **kwargs)
        
        # Estado do inimigo
        self.is_vulnerable = False  # Se está vulnerável (branco) pelo power-up
        self.is_dying = False  # Se está morrendo
        self.death_timer = 0.0
        self.death_duration = 1.0  # Tempo para morrer completamente
        self.blink_timer = 0.0
        self.blink_speed = 0.1  # Velocidade do piscar
        self.original_image = image  # Guarda imagem original
        self.white_image = white_image  # Imagem branca para vulnerabilidade
        self.hitbox_scale = 0.7  
        
    def get_collision_rect(self):
        reduced_width = self.width * self.hitbox_scale
        reduced_height = self.height * self.hitbox_scale
        offset_x = (self.width - reduced_width) / 2
        offset_y = (self.height - reduced_height) / 2

        return Rect(
            self.x - reduced_width/2,
            self.y - reduced_height/2, 
            reduced_width, 
            reduced_height
        )
    
    def collides_with(self, other):
        """Verifica colisão."""
        if hasattr(other, 'get_collision_rect'):
            return self.get_collision_rect().colliderect(other.get_collision_rect())
        else:
            # Se o outro objeto não tem hitbox personalizado, usa o padrão
            return self.get_collision_rect().colliderect(other)
        
    def make_vulnerable(self):
        """Torna o inimigo vulnerável."""
        self.is_vulnerable = True
        self.image = self.white_image
        
    def make_invulnerable(self):
        """Remove vulnerabilidade do inimigo."""
        self.is_vulnerable = False
        self.image = self.original_image
        
    def start_death(self):
        """Inicia o processo de morte do inimigo."""
        if not self.is_dying:
            self.is_dying = True
            self.death_timer = self.death_duration
            
    def update_death(self, dt):
        """Atualiza o efeito de morte (piscar)."""
        if self.is_dying:
            self.death_timer -= dt
            self.blink_timer += dt
            
            # Efeito de piscar
            if self.blink_timer >= self.blink_speed:
                self.blink_timer = 0.0
                # Alterna entre visível e invisível
                if hasattr(self, '_visible'):
                    self._visible = not self._visible
                else:
                    self._visible = False
                    
            return self.death_timer <= 0  # Retorna True quando deve ser removido
        return False
        
    def draw(self):
        """Desenha o inimigo com efeitos visuais."""
        if self.is_dying and hasattr(self, '_visible') and not self._visible:
            return  # Não desenha durante o piscar
            
        super().draw()

class BlueBird(BaseEnemy):
    """
    Inimigo voador blue bird que patrulha horizontalmente com animação de voo.
    """
    def __init__(self, pos=(0, 0)):
        # Usa os sprites do blue bird
        super().__init__('0_bb_fly', 'hit_32x32', pos=pos)
        
        self.hitbox_scale = 0.6
        
        # Movimento horizontal
        self.patrol_speed = 60
        self.patrol_range = 80
        self.start_x = pos[0]
        self.direction = random.choice([-1, 1])
        
        # Movimento vertical 
        self.bob_timer = 0.0
        self.bob_speed = 3.0
        self.bob_range = 8
        self.base_y = pos[1]
        
        # Animação de voo
        self.animation_timer = 0.0
        self.animation_speed = 8.0  # Frames por segundo
        self.current_frame = 0
        
        # Frames para direita (originais)
        self.fly_frames_right = [
            '0_bb_fly', '1_bb_fly', '2_bb_fly', '3_bb_fly', 
            '4_bb_fly', '5_bb_fly', '6_bb_fly', '7_bb_fly', '8_bb_fly'
        ]
        
        # Frames para esquerda (flipados)
        self.fly_frames_left = [
            '0_bb_fly_left', '1_bb_fly_left', '2_bb_fly_left', '3_bb_fly_left', 
            '4_bb_fly_left', '5_bb_fly_left', '6_bb_fly_left', '7_bb_fly_left', '8_bb_fly_left'
        ]
        self.hurt_frames = [
            '00_bluebird_hurt', '01_bluebird_hurt', '02_bluebird_hurt', 
            '03_bluebird_hurt', '04_bluebird_hurt'
        ]
        
        # Frames hurt para esquerda (flipados)
        self.hurt_frames_left = [
            '00_bluebird_hurt_left', '01_bluebird_hurt_left', '02_bluebird_hurt_left', 
            '03_bluebird_hurt_left', '04_bluebird_hurt_left'
        ]
        
        # Timer para efeito de piscar quando vulnerável
        self.blink_timer = 0.0

    def update_movement(self, dt):
        """Move o pássaro de um lado para o outro com animação."""
        self.x += self.patrol_speed * self.direction * dt

        # Verifica limites da patrulha
        if self.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.x < self.start_x - self.patrol_range:
            self.direction = 1
        
        # Movimento vertical (bob)
        self.bob_timer += dt * self.bob_speed
        self.y = self.base_y + math.sin(self.bob_timer) * self.bob_range
        
        # Atualiza animação baseada no estado
        if self.is_dying:
            # Animação de morte com direção
            hurt_frame = int((self.death_timer / self.death_duration) * len(self.hurt_frames))
            if hurt_frame < len(self.hurt_frames):
                # Escolhe sprite hurt baseado na direção
                if self.direction == 1:  # Indo para direita
                    self.image = self.hurt_frames_left[hurt_frame]  # Usa hurt flipado
                else:  # Indo para esquerda
                    self.image = self.hurt_frames[hurt_frame]  # Usa hurt original
        elif self.is_vulnerable:
            # Quando vulnerável, usa sprite branco com direção
            if self.direction == 1:  # Indo para direita
                self.image = '00_bluebird_hurt_left'  # Sprite branco flipado
            else:  # Indo para esquerda
                self.image = '00_bluebird_hurt'  # Sprite branco original
        else:
            # Animação normal de voo com direção
            self.animation_timer += dt * self.animation_speed
            self.current_frame = int(self.animation_timer) % len(self.fly_frames_right)
            
            # Escolhe sprites baseado na direção (corrigindo inversão)
            if self.direction == 1:  # Indo para direita
                self.image = self.fly_frames_left[self.current_frame]  # Trocado
            else:  # Indo para esquerda (direction == -1)
                self.image = self.fly_frames_right[self.current_frame]  # Trocado

    def update(self, dt):
        """Função de atualização principal."""
        # Verifica se deve morrer
        if self.update_death(dt):
            return True  # Sinaliza para ser removido
            
        if not self.is_dying:
            self.update_movement(dt)
            
        return False

    def make_vulnerable(self):
        """Torna o BlueBird vulnerável mantendo a animação."""
        self.is_vulnerable = True
        # Não define imagem fixa aqui - deixa a animação continuar
        
    def make_invulnerable(self):
        """Remove vulnerabilidade do BlueBird."""
        self.is_vulnerable = False
        # A animação normal continuará no update_movement

    def draw(self):
        """Desenha o blue bird."""
        super().draw()


class FireBall(BaseEnemy):
    """
    Inimigo bola de fogo que flutua verticalmente com animação.
    """
    def __init__(self, pos=(0, 0), size=32):
        # Usa o sprite do fogo
        super().__init__('fire', 'fire_white', pos=pos)
        
        # Movimento Vertical (fogo flutua)
        self.patrol_speed = 80  # Fogo é mais dinâmico
        self.patrol_range = 100  # Movimento vertical
        self.start_y = pos[1]
        self.direction = 1  # 1 = para baixo, -1 = para cima
        
        # Fogo tem hitbox menor
        self.hitbox_scale = 0.6
        
        # Animação de fogo
        self.animation_timer = 0.0
        self.animation_speed = 12.0  # Frames por segundo (mais rápido)
        self.current_frame = 0
        
        # Frames de animação do fogo
        self.fire_frames = [
            'fire_anim_0', 'fire_anim_1', 'fire_anim_2', 'fire_anim_3', 'fire_anim_4'
        ]
        
    def update_movement(self, dt):
        """Move a bola de fogo para cima e para baixo com animação."""
        self.y += self.patrol_speed * self.direction * dt
        
        # Se chegou ao limite inferior da patrulha
        if self.y > self.start_y + self.patrol_range:
            self.direction = -1  # Muda direção para cima
        # Se chegou ao limite superior da patrulha
        elif self.y < self.start_y - self.patrol_range:
            self.direction = 1   # Muda direção para baixo
        
        # Atualiza animação de fogo
        self.animation_timer += dt * self.animation_speed
        self.current_frame = int(self.animation_timer) % len(self.fire_frames)
        
        # Atualiza sprite baseado no estado
        if self.is_vulnerable:
            # Quando vulnerável, usa sprite branco
            self.image = 'fire_white'
        elif not self.is_dying:
            # Animação normal de fogo
            self.image = self.fire_frames[self.current_frame]
        
    def update(self, dt):
        """Função de atualização principal."""
        # Verifica se deve morrer
        if self.update_death(dt):
            return True  # Sinaliza para ser removido
            
        if not self.is_dying:
            self.update_movement(dt)
        return False

    def make_vulnerable(self):
        """Torna a bola de fogo vulnerável."""
        self.is_vulnerable = True
        
    def make_invulnerable(self):
        """Remove vulnerabilidade da bola de fogo."""
        self.is_vulnerable = False
        

    def draw(self):
        """Desenha a bola de fogo."""
        super().draw()


class Ghost(BaseEnemy):
    """
    Inimigo fantasma que persegue o player.
    """
    def __init__(self, pos=(0, 0), size=28):
        # Usa o sprite do fantasma
        super().__init__('ghost', 'ghost_white', pos=pos)
        
        
        # Fantasma tem hitbox um pouco menor
        self.hitbox_scale = 0.7 
        
        # Comportamento de Perseguição (fantasma é mais rápido)
        self.chase_speed = 70  # Fantasma é mais rápido
        self.detection_range = 250  # Fantasma detecta de mais longe
        self.player_ref = None
        
        # Direção do fantasma para sprites direcionais
        self.facing_direction = 1  # 1 = direita, -1 = esquerda
        
        # Animação idle do fantasma
        self.animation_timer = 0.0
        self.animation_speed = 6.0  # Frames por segundo
        self.current_frame = 0
        
        # Frames para direita (originais)
        self.idle_frames_right = [
            'ghost_idle_0', 'ghost_idle_1', 'ghost_idle_2', 'ghost_idle_3'
        ]
        
        # Frames para esquerda (flipados)
        self.idle_frames_left = [
            'ghost_idle_0_left', 'ghost_idle_1_left', 'ghost_idle_2_left', 'ghost_idle_3_left'
        ]
        
    def set_player_reference(self, player):
        """Define a referência ao player para perseguição."""
        self.player_ref = player
        
    def update_movement(self, dt):
        """Move o fantasma em direção ao player se estiver próximo."""
        if not self.player_ref:
            return
            
        # Calcula a distância até o player
        dx = self.player_ref.x - self.x
        dy = self.player_ref.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Se o player estiver dentro do alcance de detecção
        if distance < self.detection_range and distance > 5:
            # Determina direção baseada no movimento horizontal
            if dx > 0:
                self.facing_direction = 1  # Indo para direita
            elif dx < 0:
                self.facing_direction = -1  # Indo para esquerda
            
            # Normaliza o vetor direção
            dx = dx / distance
            dy = dy / distance
            
            # Move em direção ao player (fantasma flutua através de obstáculos)
            self.x += dx * self.chase_speed * dt
            self.y += dy * self.chase_speed * dt
        
        # Atualiza animação idle
        self.animation_timer += dt * self.animation_speed
        self.current_frame = int(self.animation_timer) % len(self.idle_frames_right)
        
        # Atualiza sprite baseado na direção e estado
        if self.is_vulnerable:
            # Quando vulnerável, usa sprite branco
            self.image = 'ghost_white'
        elif not self.is_dying:
            if self.facing_direction == 1:  # Indo para direita
                self.image = self.idle_frames_left[self.current_frame]  # Trocado
            else:  # Indo para esquerda
                self.image = self.idle_frames_right[self.current_frame]  # Trocado
    
    def update(self, dt):
        """Função de atualização principal."""
        # Verifica se deve morrer
        if self.update_death(dt):
            return True  # Sinaliza para ser removido
            
        if not self.is_dying:
            self.update_movement(dt)
        return False

    def make_vulnerable(self):
        """Torna o fantasma vulnerável mantendo a direção."""
        self.is_vulnerable = True
        # Não define imagem fixa aqui - deixa a animação continuar com sprite branco
        
    def make_invulnerable(self):
        """Remove vulnerabilidade do fantasma."""
        self.is_vulnerable = False
        # A animação normal continuará no update_movement

    def draw(self):
        """Desenha o fantasma."""
        super().draw()