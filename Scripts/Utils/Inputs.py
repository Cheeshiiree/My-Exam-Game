# Código para reconhecer os inputs

import pgzero

# Combinar inputs de teclado
def get_input():
    keys = pgzero.keyboard.get_pressed()
    inputs = {
        'left': keys[pgzero.keys.LEFT] or keys[pgzero.keys.A],
        'right': keys[pgzero.keys.RIGHT] or keys[pgzero.keys.D],
        'up': keys[pgzero.keys.UP] or keys[pgzero.keys.W],
        'down': keys[pgzero.keys.DOWN] or keys[pgzero.keys.S],
        'jump': keys[pgzero.keys.SPACE],
        'attack': keys[pgzero.keys.Z],
        'interact': keys[pgzero.keys.X]
    }
    return inputs