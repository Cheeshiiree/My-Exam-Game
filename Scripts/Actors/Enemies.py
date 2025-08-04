# Scripts/Actors/Enemies.py

from pgzero.actor import Actor
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

        from pygame import Rect
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
    Inimigo voador triangular azul que patrulha horizontalmente.
    """
    def __init__(self, pos=(0, 0)):
        # Usa a forma triangular azul
        super().__init__('blue_triangle', 'blue_triangle_white', pos=pos)
        
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

    def update_movement(self, dt):
        """Move o pássaro de um lado para o outro."""
        self.x += self.patrol_speed * self.direction * dt

        # Verifica limites da patrulha
        if self.x > self.start_x + self.patrol_range:
            self.direction = -1
        elif self.x < self.start_x - self.patrol_range:
            self.direction = 1
        
        self.bob_timer += dt * self.bob_speed
        self.y = self.base_y + math.sin(self.bob_timer) * self.bob_range

    def update(self, dt):
        """Função de atualização principal."""
        # Verifica se deve morrer
        if self.update_death(dt):
            return True  # Sinaliza para ser removido
            
        if not self.is_dying:
            self.update_movement(dt)
        return False

    def draw(self):
        """Desenha o triângulo azul."""
        super().draw()


class RedSquare(BaseEnemy):
    """
    Inimigo quadrado vermelho que se move verticalmente.
    """
    def __init__(self, pos=(0, 0), size=32):
        # Usa a forma quadrada vermelha
        super().__init__('red_square', 'red_square_white', pos=pos)
        
       
        self.hitbox_scale = 0.75  
        
        # Movimento Vertical
        self.patrol_speed = 80
        self.patrol_range = 100
        self.start_y = pos[1]
        self.direction = 1  # 1 = para baixo, -1 = para cima
        
    def update_movement(self, dt):
        """Move o quadrado para cima e para baixo."""
        self.y += self.patrol_speed * self.direction * dt
        
        # Se chegou ao limite inferior da patrulha
        if self.y > self.start_y + self.patrol_range:
            self.direction = -1  # Muda direção para cima
        # Se chegou ao limite superior da patrulha
        elif self.y < self.start_y - self.patrol_range:
            self.direction = 1   # Muda direção para baixo
        
    def update(self, dt):
        """Função de atualização principal."""
        # Verifica se deve morrer
        if self.update_death(dt):
            return True  # Sinaliza para ser removido
            
        if not self.is_dying:
            self.update_movement(dt)
        return False

    def draw(self):
        """Desenha o quadrado vermelho."""
        super().draw()


class GreenCircle(BaseEnemy):
    """
    Inimigo circular verde que persegue o player.
    """
    def __init__(self, pos=(0, 0), size=28):
        # Usa a forma circular verde
        super().__init__('green_circle', 'green_circle_white', pos=pos)
        
        
        self.hitbox_scale = 0.8 
        
        # Comportamento de Perseguição
        self.chase_speed = 50
        self.detection_range = 200
        self.player_ref = None
        
    def set_player_reference(self, player):
        """Define a referência ao player para perseguição."""
        self.player_ref = player
        
    def update_movement(self, dt):
        """Move o círculo em direção ao player se estiver próximo."""
        if not self.player_ref:
            return
            
        # Calcula a distância até o player
        dx = self.player_ref.x - self.x
        dy = self.player_ref.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Se o player estiver dentro do alcance de detecção
        if distance < self.detection_range and distance > 5:
            # Normaliza o vetor direção
            dx = dx / distance
            dy = dy / distance
            
            # Move em direção ao player
            self.x += dx * self.chase_speed * dt
            self.y += dy * self.chase_speed * dt
    
    def update(self, dt):
        """Função de atualização principal."""
        # Verifica se deve morrer
        if self.update_death(dt):
            return True  # Sinaliza para ser removido
            
        if not self.is_dying:
            self.update_movement(dt)
        return False

    def draw(self):
        """Desenha o círculo verde."""
        super().draw()