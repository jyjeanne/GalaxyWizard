# 🧙‍♂️ GalaxyWizard


[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/jyjeanne/GalaxyWizard)

> An open-source tactical RPG made with Python, featuring 3D graphics, strategic combat, and multiplayer support. It is a cross-platform game , you can run it on Windows, Linux , Macintosh. It is a fork of GalaxyMage originally written by Colin McMillen in 2006 with python 2.7.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Getting Started](#-getting-started)
- [Game Controls](#-game-controls)
- [Gameplay](#-gameplay)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🎮 Overview

GalaxyWizard is a tactical role-playing game inspired by classic strategy RPGs. Command your units across 3D battlefields, engage in strategic combat, and experience rich storytelling in an open-source gaming environment.

**Key Highlights:**
- 🎯 **Strategic Combat**: Turn-based tactical battles on 3D battlefields
- 🌐 **Multiplayer Ready**: Built-in network support for online battles
- 🎨 **3D Graphics**: OpenGL-powered 3D rendering with dynamic camera system
- 🔧 **Modular Design**: Extensible architecture for custom scenarios and units
- 🆓 **Open Source**: GPL v2 licensed, community-driven development

## ✨ Features

### Core Gameplay
- **Turn-based tactical combat** with strategic positioning
- **Character classes** with unique abilities and progression
- **Dynamic 3D battlefields** with height variations and obstacles
- **Scenario system** with both scripted and randomly generated maps

### Technical Features
- **Cross-platform compatibility** (Windows, Linux, macOS)
- **Network multiplayer** using Twisted framework
- **Resource management** with modular asset loading
- **OpenGL rendering** with modern graphics pipeline
- **Poetry dependency management** for easy setup

### Game Systems
- **Unit progression** with experience and leveling
- **Equipment system** with weapons, armor, and items
- **Ability system** with diverse magical and combat skills
- **Map editor** for creating custom scenarios

## 🚀 Installation

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Poetry** - [Install Poetry](https://python-poetry.org/docs/#installation)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jyjeanne/GalaxyWizard.git
   cd GalaxyWizard
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Run the game**
   ```bash
   poetry run python src/main.py
   ```

### Alternative Setup (pip)

If you prefer using pip:

```bash
pip install pygame PyOpenGL Twisted Pillow
python src/main.py
```

### Command Line Options

```bash
# Show help
poetry run python src/main.py -h

# Run in windowed mode
poetry run python src/main.py --windowed

# Run specific scenario
poetry run python src/main.py --scenario demo/castle
```

## 🎯 Getting Started

### First Launch

1. **Start the game** using the installation commands above
2. **Select a scenario** from the main menu using ↑/↓ arrows
3. **Press Enter** to begin your first battle
4. **Follow the tutorial** prompts to learn basic gameplay

### Recommended First Scenario

For new players, we recommend starting with the **"Castle"** scenario, which provides a balanced introduction to the game mechanics.

## 🎮 Game Controls

### Basic Controls

| Action | Key/Mouse | Description |
|--------|-----------|-------------|
| **Move Cursor** | `↑` `↓` `←` `→` | Navigate the battlefield |
| **Select/Confirm** | `Enter` | Select unit or confirm action |
| **Cancel/Back** | `Escape` | Unselect unit or go back |
| **Quit Game** | `Q` | Exit to desktop |
| **Quit Scenario** | `W` | Return to scenario selection |

### Camera Controls

| Action | Key/Mouse | Description |
|--------|-----------|-------------|
| **Pan Camera** | `Left Click + Drag` | Move camera around battlefield |
| **Rotate Camera** | `Right Click + Drag` | Rotate view smoothly |
| **Rotate 45°** | `[` `]` or `Home` `End` | Snap to 8-way directions |
| **Zoom In/Out** | `Mouse Wheel` or `Page Up/Down` | Adjust camera distance |
| **Reset Camera** | `R` | Return to default view |
| **Tilt Camera** | `Right Click + Drag Up/Down` | Adjust camera pitch |

### Utility Controls

| Action | Key | Description |
|--------|-----|-------------|
| **Toggle FPS** | `F` | Show/hide frame rate |
| **Toggle Audio** | `S` | Mute/unmute all sounds |
| **Full Screen** | `F12` | Toggle full-screen mode (Linux) |
| **Debug Map** | `Scroll Lock` | Dump map data to console |

## 🏰 Gameplay

### Basic Gameplay Loop

1. **Unit Selection**: Use arrow keys to move cursor, press Enter to select units
2. **Movement**: Selected units can move within their movement range (highlighted in blue)
3. **Actions**: After moving, units can attack, use abilities, or use items
4. **Turn Management**: Each player takes turns moving all their units
5. **Victory Conditions**: Defeat all enemies or complete scenario objectives

### Unit Classes

- **🗡️ Fighter**: Melee combat specialist with high defense
- **🏹 Archer**: Ranged attacker with bow and arrow abilities
- **🔮 Mage**: Magic user with elemental spells and support abilities
- **🛡️ Healer**: Support class focused on healing and protection
- **🗡️ Rogue**: Fast, agile unit with stealth and critical hit abilities

### Combat Mechanics

- **Range-based Combat**: Different weapons have different attack ranges
- **Height Advantage**: Units on higher ground gain combat bonuses
- **Elemental Damage**: Fire, ice, and other elemental effects
- **Status Effects**: Buffs, debuffs, and temporary conditions
- **Critical Hits**: Chance-based bonus damage

## 🛠 Development

### Project Structure

```
GalaxyWizard/
├── src/                    # Source code
│   ├── engine/            # Core game logic
│   ├── gui/               # User interface and graphics
│   ├── ai/                # AI behavior systems
│   ├── data/              # Game data and configurations
│   └── test/              # Unit tests
├── doc/                   # Documentation
├── pyproject.toml         # Poetry configuration
└── README.md             # This file
```

### Running Tests

```bash
# Run all tests
poetry run python src/test/TestSuite.py

# Run specific test module
poetry run python src/test/TestSuite.py -m enginetests.UnitTest

# Run with verbose output
poetry run python src/test/TestSuite.py -v
```

### Building Executable

```bash
# Using Poetry script
poetry run galaxywizard-build

# Or directly with PyInstaller
poetry run pyinstaller main.spec --clean

# Output: dist/GalaxyWizard.exe
```

**Note:** The `poetry install` step may fail due to missing C++ build tools for PyOpenGL-accelerate. To build the executable, you'll need to either:
- Install [Microsoft Visual C++ 14.0+ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), or
- Remove `PyOpenGL_accelerate` from dependencies (it's optional - only provides performance improvements)

**Technical Details:**
- The executable uses PyInstaller's `sys._MEIPASS` to locate bundled data files
- All game data from `src/data/` is bundled into the executable
- Resource paths are automatically resolved for both normal and executable modes

### Architecture & UML Diagrams

Auto-generated UML diagrams (package dependencies and per-package class
diagrams) are available in [doc/architecture.md](doc/architecture.md) and
render directly on GitHub via Mermaid. They are regenerated automatically
by CI on every push to `main` that touches `src/`, or manually with:

```bash
# Requires dev dependencies (pylint provides pyreverse)
poetry run galaxywizard-uml
```

### AI Knowledge Graph

An AI-ready knowledge graph of the codebase (packages, modules, classes,
functions and the imports / inherits / uses relations between them) is
generated automatically alongside a human-readable architecture report:

- [doc/knowledge-graph.md](doc/knowledge-graph.md) - Architecture report
  with package-dependency and class-inheritance diagrams (Mermaid), key
  module rankings and a full module inventory
- [doc/graph/knowledge_graph.json](doc/graph/knowledge_graph.json) -
  Machine-readable graph for AI assistants, graph databases or
  visualization tools

Both are regenerated automatically by CI on every push to `main` that
touches `src/`, or manually with:

```bash
# Stdlib only - no extra dependencies required
poetry run galaxywizard-graphify
```

### Development Setup

1. **Fork and clone** the repository
2. **Install development dependencies**:
   ```bash
   poetry install --with dev
   ```
3. **Run tests** to ensure everything works
4. **Make your changes** following the coding standards
5. **Submit a pull request** with your improvements

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs**: Use GitHub Issues to report problems
- 💡 **Suggest Features**: Propose new gameplay mechanics or improvements
- 🔧 **Submit Code**: Fix bugs, add features, or improve documentation
- 🎨 **Create Content**: Design new scenarios, units, or artwork
- 📖 **Improve Documentation**: Help make the project more accessible

### Development Guidelines

- **Python 3.11+** compatibility required
- **Follow PEP 8** style guidelines
- **Write tests** for new features
- **Update documentation** for user-facing changes
- **Use meaningful commit messages**

### Quick Start for Contributors

```bash
# Fork the repo and clone your fork
git clone https://github.com/YOUR_USERNAME/GalaxyWizard.git

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
poetry run python src/test/TestSuite.py

# Commit and push
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

## 📄 License

**GalaxyWizard** is free software licensed under the **GNU General Public License v2.0**.

- ✅ **Use** - Run the program for any purpose
- ✅ **Study** - Examine and understand how it works
- ✅ **Share** - Redistribute copies to help others
- ✅ **Improve** - Modify and distribute your changes

```
Copyright (C) 2024 Jeremy Jeanne <jyjeanne@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
```

See the [LICENSE](LICENSE) file for complete details.

---

## 🔗 Links

- **🐛 Report Issues**: [GitHub Issues](https://github.com/jyjeanne/GalaxyWizard/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/jyjeanne/GalaxyWizard/discussions)
- **📖 Documentation**: [Game Documentation](doc/)
- **🎮 Gameplay Guide**: [How to Play](doc/gameplay.html)

---

<div align="center">

**⭐ Star this repository if you find it useful! ⭐**

*Made with ❤️ by the GalaxyWizard community*

</div>