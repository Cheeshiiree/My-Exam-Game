# Scripts/Utils/InputManager.py
# Gerenciador de input com controle de debounce e feedback

class InputManager:
    """Gerencia inputs com controle de debounce para evitar repetições excessivas"""
    
    def __init__(self):
        self.key_states = {}
        self.key_counters = {}
        self.default_delay = 10  # 10 frames de delay padrão
        
    def is_key_pressed(self, key_name, keyboard, delay=None):
        """
        Verifica se uma tecla foi pressionada considerando o delay de debounce
        
        Args:
            key_name: Nome da tecla para rastreamento
            keyboard: Objeto keyboard do PgZero
            delay: Delay customizado em frames (opcional)
        
        Returns:
            bool: True se a tecla pode ser processada
        """
        current_delay = delay if delay is not None else self.default_delay
        
        # Inicializa estado da tecla se não existir
        if key_name not in self.key_states:
            self.key_states[key_name] = False
            self.key_counters[key_name] = 0
        
        # Verifica se a tecla está sendo pressionada
        key_pressed = self._check_key(key_name, keyboard)
        
        if key_pressed:
            # Se a tecla não estava pressionada antes OU se o delay passou
            if (not self.key_states[key_name] or 
                self.key_counters[key_name] >= current_delay):
                
                self.key_states[key_name] = True
                self.key_counters[key_name] = 0
                return True
            else:
                # Incrementa contador se tecla continua pressionada
                self.key_counters[key_name] += 1
        else:
            # Tecla foi solta
            self.key_states[key_name] = False
            self.key_counters[key_name] = 0
            
        return False
    
    def _check_key(self, key_name, keyboard):
        """Verifica diferentes tipos de tecla"""
        if key_name == "up":
            return keyboard.up or keyboard.w
        elif key_name == "down":
            return keyboard.down or keyboard.s
        elif key_name == "space":
            return keyboard.space
        elif key_name == "1":
            return keyboard.K_1
        elif key_name == "m":
            return keyboard.m
        else:
            return False
    
    def reset(self):
        """Reseta todos os estados das teclas"""
        self.key_states.clear()
        self.key_counters.clear()

# Instância global
input_manager = InputManager()
