# Scripts/Components/platform.py

from pgzero.actor import Actor

class Platform(Actor):
    """Classe que representa uma plataforma no jogo usando PgZero Actor."""
    def __init__(self, platform_type='normal', position=(0, 0), size=(64, 32)):
        
        if platform_type == 'normal':
            # Usa uma imagem verde (vamos criar um arquivo de 1px verde)
            super().__init__('platform_green', pos=position)
        elif platform_type == 'danger':
            # Usa uma imagem vermelha (vamos criar um arquivo de 1px vermelho)
            super().__init__('platform_red', pos=position)
        else:
            # Padrão
            super().__init__('platform_green', pos=position)
        
        # Define o tipo da plataforma
        self.platform_type = platform_type
        self.platform_size = size
        
        # Ajusta o tamanho do ator
        self.width = size[0]
        self.height = size[1]

class DangerPlatform(Platform):
    """Plataforma perigosa que machuca o player."""
    def __init__(self, position=(0, 0), size=(64, 32)):
        super().__init__('danger', position, size)
        self.damage = True  # Indica que esta plataforma causa dano


class Heart(Actor):
    """Coletável de vida."""
    def __init__(self, **kwargs):
        super().__init__('heart', **kwargs)
        self.bob_timer = 0.0
        self.bob_offset = 0.0
        self.original_y = self.y
        
    def update(self, dt):
        """Atualização do coração com animação de flutuação."""
        # Animação de flutuação (bob)
        self.bob_timer += dt * 3  # Velocidade da flutuação
        self.bob_offset = 5 * (0.5 + 0.5 * (self.bob_timer % 6.28))  # Movimento senoidal
        self.y = self.original_y - self.bob_offset


class PowerFruit(Actor):
    """Coletável de power-up."""
    def __init__(self, **kwargs):
        # Usar a power fruit como power-up
        super().__init__('power_fruit', **kwargs)
        self.bob_timer = 0.0
        self.bob_offset = 0.0
        self.original_y = self.y
        self.rotation_timer = 0.0
        
    def update(self, dt):
        """Atualização da power fruit com animação de flutuação e rotação."""
        # # Animação de flutuação (bob)
        # self.bob_timer += dt * 4  # Velocidade da flutuação
        # self.bob_offset = 8 * (0.5 + 0.5 * (self.bob_timer % 6.28))  # Movimento senoidal
        # self.y = self.original_y - self.bob_offset
        
        # Rotação suave
        self.rotation_timer += dt * 2
        self.angle = self.rotation_timer * 180 / 3.14159  # Conversão para graus
