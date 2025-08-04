# # Classe principal de controle do Player

# Scripts/Actors/Player.py

from pgzero.actor import Actor

class Player(Actor):
    def __init__(self, **kwargs):
        # 1. Animações simplificadas usando sprites femininos
        self.idle_frames = [f'player/female_sprites/character1f_1_idle_{i}' for i in range(8)]
        self.run_frames = [f'player/female_sprites/character1f_1_run_{i}' for i in range(8)]
        self.jump_frames = [f'player/female_sprites/character1f_1_jump_{i}' for i in range(2)]
        
        # 2. Dicionário de animações simplificado (igual ao original)
        self.animations = {
            'idle': self.idle_frames,
            'run': self.run_frames,
            'jump': self.jump_frames
        }
        
        # 3. Inicializamos o Actor com o primeiro frame
        super().__init__(self.idle_frames[0], **kwargs)

        # 4. Variáveis de controle simplificadas
        self.state = 'idle'
        self.current_frame = 0
        self.animation_timer = 0.0
        self.facing_right = True  # Direção que a personagem está olhando
        
        # Variáveis de física
        self.vx = 0
        self.vy = 0
        self.is_grounded = False
        
        # Sistema de pulo duplo
        self.jump_count = 0
        self.max_jumps = 2  # Permite pulo duplo
        self.jump_pressed = False  # Para evitar pulos múltiplos com tecla pressionada
        
        # Sistema de vida
        self.health = 5  # Vida inicial: 5 corações
        self.max_health = 10  # Vida máxima: 10 corações
        self.invincible = False  # Sistema de invencibilidade temporária
        self.invincible_timer = 0.0
        self.invincible_duration = 2.0  # 2 segundos de invencibilidade após dano
        
        # Sistema de power-up
        self.has_power = False  # Se tem power fruit ativo
        self.power_timer = 0.0
        self.power_duration = 10.0  # 10 segundos de poder
        
        # Ajuste de hitbox para sprites femininos
        self.hitbox_scale = 0.7  # Reduzindo mais o hitbox  

    def get_collision_rect(self):
        """Retorna um retângulo menor para colisão mais precisa."""
        # Hitbox bem pequeno focado apenas nos pés da personagem
        hitbox_width = self.width * 0.5  # Muito estreito
        hitbox_height = self.height * 0.3  # Muito baixo
        
        # Posiciona o hitbox bem embaixo da sprite
        hitbox_x = self.x - hitbox_width/2
        hitbox_y = self.y + self.height/2 - hitbox_height  # Na base da sprite
        
        # Cria um retângulo com o hitbox reduzido
        from pygame import Rect
        return Rect(
            hitbox_x,
            hitbox_y, 
            hitbox_width, 
            hitbox_height
        )
    
    def collides_with(self, other):
        """Verifica colisão."""
        if hasattr(other, 'get_collision_rect'):
            return self.get_collision_rect().colliderect(other.get_collision_rect())
        else:
            # Se o outro objeto não tem hitbox personalizado, usa o padrão
            return self.get_collision_rect().colliderect(other)

    def update_animation(self, dt):
        """Atualiza a imagem do ator com base no estado atual."""
        # Atualiza invencibilidade
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Atualiza power-up
        if self.has_power:
            self.power_timer -= dt
            if self.power_timer <= 0:
                self.has_power = False
        
        self.animation_timer += dt
        
        # Velocidade de animação similar ao sistema original
        animation_speed = 0.08 if self.state == 'run' else 0.15

        if self.animation_timer > animation_speed:
            self.animation_timer = 0.0
            
            # Pega na lista de frames correta
            current_animation_frames = self.animations[self.state]
            
            # Avança o frame
            self.current_frame = (self.current_frame + 1) % len(current_animation_frames)
            
            # Define a nova imagem
            self.image = current_animation_frames[self.current_frame]
            
            # Espelha a imagem se estiver virada para a esquerda
            if not self.facing_right:
                # Usa o pygame para espelhar a imagem horizontalmente
                import pygame
                # Obtém a surface da imagem atual
                original_surf = self._surf
                # Espelha horizontalmente (flip_x=True, flip_y=False)
                flipped_surf = pygame.transform.flip(original_surf, True, False)
                # Atualiza a surface
                self._surf = flipped_surf
    
    def take_damage(self, damage=1):
        """Player recebe dano se não estiver invencível."""
        if not self.invincible and self.health > 0:
            self.health -= damage
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            return True  # Retorna True se realmente tomou dano
        return False
    
    def heal(self, amount=1):
        """Player recupera vida."""
        if self.health < self.max_health:
            self.health = min(self.health + amount, self.max_health)
            return True  # Retorna True se realmente curou
        return False
    
    def is_alive(self):
        """Verifica se o player ainda está vivo."""
        return self.health > 0
    
    def activate_power(self):
        """Ativa o power-up de matar inimigos."""
        self.has_power = True
        self.power_timer = self.power_duration
        return True