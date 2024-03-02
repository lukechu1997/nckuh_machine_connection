# -*- mode: python ; coding: utf-8 -*-

pyFiles = [
    'app.py',
    'libs\\view\\ui.py',
    'libs\\view\\option.py',
    'libs\\controllers\\mainController.py',
    'libs\\controllers\\optionController.py',
    'libs\\helpers\\serialHelper.py',
    'libs\\model\\mdbModel.py',
    'libs\\model\\sqliteModel.py',
    'libs\\threads\\fetchTestsThread.py'
]

a = Analysis(
    pyFiles,
    pathex=[],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='G1200工具程式',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
