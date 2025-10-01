# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for GalaxyWizard tactical RPG.
Bundles all dependencies, data files, and resources into a standalone executable.
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files from src/data directory
data_files = []

# Add all data files (abilities, classes, items, maps, scenarios, units)
data_files += [
    ('src/data', 'data'),  # Include entire data directory
]

# Collect hidden imports for dynamic modules
hiddenimports = [
    # Main dependencies
    'pygame',
    'OpenGL',
    'OpenGL.GL',
    'OpenGL.GLU',
    'OpenGL.GLUT',
    'OpenGL.arrays',
    'OpenGL.arrays.arraydatatype',
    'numpy',
    'numpy.core._methods',
    'numpy.lib.format',
    'twisted',
    'twisted.internet',
    'twisted.internet.reactor',
    'twisted.internet.protocol',
    'twisted.internet.selectreactor',
    'twisted.spread',
    'twisted.spread.pb',
    'twisted.python',
    'twisted.python.log',
    'zope.interface',
    # Root src modules
    'translate',
    'resources',
    'sound',
    'util',
    'constants',
    'fsm',
    'log',
    'twistedmain',
]

# Collect all submodules from engine, gui, ai packages
hiddenimports += collect_submodules('engine')
hiddenimports += collect_submodules('gui')
hiddenimports += collect_submodules('ai')
hiddenimports += collect_submodules('test')

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],  # Add src to the Python path
    binaries=[],
    datas=data_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'pandas',
        'scipy',
        'IPython',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GalaxyWizard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed mode (no console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if you have one: 'src/data/core/images/icon-32.png'
)
