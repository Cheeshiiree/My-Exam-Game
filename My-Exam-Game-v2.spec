# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('images', 'images'), ('sounds', 'sounds'), ('music', 'music')]
datas += collect_data_files('pgzero')


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pgzero', 'pgzero.actor', 'pgzero.animation', 'pgzero.builtins', 'pgzero.clock', 'pgzero.game', 'pgzero.keyboard', 'pgzero.loaders', 'pgzero.music', 'pgzero.rect', 'pgzero.screen', 'pgzero.sounds', 'pgzero.tone', 'pygame', 'pygame.mixer', 'pygame.time', 'pygame.key', 'pygame.constants', 'pygame.locals', 'pygame.font', 'pygame.image', 'pygame.surface', 'pygame.rect', 'pygame.color', 'pygame.math'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='My-Exam-Game-v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
