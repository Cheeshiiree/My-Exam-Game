# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('images', 'images'), ('music', 'music'), ('sound', 'sound'), ('Scripts', 'Scripts')]
datas += collect_data_files('pgzero')


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pgzero', 'pgzero.game', 'pgzero.runner', 'pgzrun'],
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
    name='MyExamGame',
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
