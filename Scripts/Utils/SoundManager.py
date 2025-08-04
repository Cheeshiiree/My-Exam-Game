# Scripts/Utils/SoundManager.py

import random

class SoundManager:
    """Gerenciador centralizado de efeitos sonoros."""
    
    def __init__(self):
        """Inicializa o gerenciador de sons."""
        self.sounds_enabled = True
        self.sound_volume = 0.7
        
        # Mapeamento direto para os arquivos copiados na pasta sound/
        self.sound_mapping = {
            'menu_navigate': 'menu_navigate',
            'menu_select': 'menu_select',
            'player_jump': 'player_jump',
            # 'player_land': 'player_land',  # Removido - som muito repetitivo
            'player_hurt': 'player_hurt',
            'player_die': 'player_die',
            'collect_heart': 'collect_heart',
            'collect_power': 'collect_power',
            'enemy_die': 'enemy_die',
            'portal_enter': 'portal_enter',
            'level_complete': 'level_complete',
            'menu_toggle': 'menu_select',  # Reutiliza o som de seleção
        }
    
    def play_sound(self, action, volume=None):
        """
        Toca um efeito sonoro baseado na ação.
        
        Args:
            action (str): Nome da ação (ex: 'player_jump', 'menu_select')
            volume (float, optional): Volume específico para este som (0.0 a 1.0)
        """
        if not self.sounds_enabled:
            return
            
        if action not in self.sound_mapping:
            return
        
        try:
            # Obtém o nome do arquivo de som
            sound_name = self.sound_mapping[action]
            
            # Usa pygame diretamente (método que funciona)
            import pygame
            sound_path = f"sound/{sound_name}.ogg"
            sound_obj = pygame.mixer.Sound(sound_path)
            
            # Define o volume se especificado
            if volume is not None:
                sound_obj.set_volume(volume)
            else:
                sound_obj.set_volume(self.sound_volume)
            
            sound_obj.play()
                
        except Exception as e:
            # Ignora erros silenciosamente para não quebrar o jogo
            pass
    
    def set_volume(self, volume):
        """Define o volume geral dos efeitos sonoros (0.0 a 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def enable_sounds(self, enabled=True):
        """Habilita ou desabilita os efeitos sonoros."""
        self.sounds_enabled = enabled
    
    def toggle_sounds(self):
        """Alterna entre sons ligados/desligados."""
        self.sounds_enabled = not self.sounds_enabled
        return self.sounds_enabled

# Instância global do gerenciador de sons
sound_manager = SoundManager()
