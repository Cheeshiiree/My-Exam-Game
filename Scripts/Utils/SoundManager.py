# Scripts/Utils/SoundManager.py

import random

class SoundManager:
    """Gerenciador centralizado de efeitos sonoros."""
    
    def __init__(self):
        """Inicializa o gerenciador de sons."""
        self.sounds_enabled = True
        self.sound_volume = 0.7
        self.sounds_ref = None  # Referência para o objeto sounds do PgZero
        
        # Mapeamento direto para os arquivos copiados na pasta sound/
        self.sound_mapping = {
            'menu_navigate': 'menu_navigate',
            'menu_select': 'menu_select',
            'player_jump': 'player_jump',
            # 'player_land': 'player_land', 
            'player_hurt': 'player_hurt',
            'player_die': 'player_die',
            'collect_heart': 'collect_heart',
            'collect_power': 'collect_power',
            'enemy_die': 'enemy_die',
            'portal_enter': 'portal_enter',
            'level_complete': 'level_complete',
            'menu_toggle': 'menu_select', 
        }
    
    def set_sounds_reference(self, sounds):
        """Define a referência para o objeto sounds do PgZero."""
        self.sounds_ref = sounds
    
    def play_sound(self, action, volume=None):
        if not self.sounds_enabled:
            return
            
        if action not in self.sound_mapping:
            return
        
        try:
            # Obtém o nome do arquivo de som
            sound_name = self.sound_mapping[action]
            
            # Tenta tocar o som usando a referência do PgZero
            if hasattr(self, '_pgzero_sounds'):
                try:
                    sound_obj = self._pgzero_sounds.load(sound_name)
                    if sound_obj:
                        sound_obj.play()
                        
                        return
                except Exception as e:
                    try:
                        # Tenta carregar com .ogg explicitamente
                        sound_obj = self._pgzero_sounds.load(f"{sound_name}.ogg")
                        if sound_obj:
                            sound_obj.play()
                            
                            return
                    except Exception as e2:
                        print(f"Erro ao carregar {sound_name}: {e} / {e2}")
            
            # Fallback: indica tentativa de som
            print(f"🔊 📢 {action.upper()}: {sound_name}")
                
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
