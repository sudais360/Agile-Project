# -*- mode: python ; coding: utf-8 -*-
# Enable debugging output

import logging
logging.basicConfig(level=logging.DEBUG)


block_cipher = None

# List all Python files for your project
scripts = [
    'main.py',
    'africa.py',
    'asia.py',
    'australia.py',
    'europe.py',
    'gameplay.py',
    'gameplay2.py',
    'gameplay3.py',
    'geomap.py',
    'highscore.py',
    'imagresize.py',
    'lives.py',
    'main.py',
    'multiplayer.py',
    'northamerica.py',
    'question.py',
    'quiz.py',
    'signuppage.py',
    'slidePanel.py',
    'userlogin.py',
]

# Add asset folders and their contents
datas = [
    ('assets/images', 'assets/images'),  # Include 'images' folder and its contents
    ('assets/sounds', 'assets/sounds'),  # Include 'sounds' folder and its contents
    ('assets/certs', 'assets/certs'),    # Include 'certs' folder and its contents
    ('city-backgrounds-pixel-art', 'city-backgrounds-pixel-art'),  # Include 'city-backgrounds-pixel-art' folder and its contents
    ('fantasy-chibi-female-sprites-pixel-art', 'fantasy-chibi-female-sprites-pixel-art'),  # Include 'fantasy-chibi-female-sprites-pixel-art' folder and its contents
    ('gameassets', 'gameassets'),  # Include 'gameassets' folder and its contents
    ('graphics', 'graphics'),  # Include 'graphics' folder and its contents
    ('login_img', 'login_img'),  # Include 'login_img' folder and its contents
    ('map_img', 'map_img'),  # Include 'map_img' folder and its contents
    ('Red hood free Folder', 'Red hood free Folder'),  # Include 'Red hood free Folder' folder and its contents
    ('audio', 'audio'),  # Include 'audio' folder and its contents
    ('font', 'font'),    # Include 'font' folder and its contents
    ('cacert.pem', '.'),  # Include 'cacert.pem' at the root of the executable
    ('README.md', '.'),   # Include 'README.md' at the root of the executable
]

icon = 'gameassets/icon.png'

a = Analysis(
    ['userlogin.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='WORLD_WANDERER',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
