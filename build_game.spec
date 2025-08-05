# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('images', 'images'),
        ('music', 'music'),
        ('sound', 'sound'),
        ('Scripts', 'Scripts'),
    ],
    hiddenimports=[
        'pygame',
        'pgzero',
        'pgzero.game',
        'pgzero.runner',
        'pgzero.constants',
        'pgzero.loaders',
        'pgzero.actor',
        'pgzero.animation',
        'pgzero.clock',
        'pgzero.keyboard',
        'pgzero.mouse',
        'pgzero.music',
        'pgzero.tone',
        'pgzero.transform',
        'pgzero.rect',
        'pgzero.screen',
        'pgzero.sounds',
        'pgzero.storage',
        'pgzrun',
        'Scripts.Actors.Player',
        'Scripts.Actors.Enemies',
        'Scripts.Components',
        'Scripts.Scenes.Menu',
        'Scripts.Scenes.Scene1',
        'Scripts.Scenes.Scene2',
        'Scripts.Utils.InputManager',
        'Scripts.Utils.Movement',
        'Scripts.Utils.SoundManager',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyExamGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para não mostrar console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Você pode adicionar um ícone aqui depois
)
