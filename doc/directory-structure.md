# Directory Structure

This page gives an overview of the directory structure of the GalaxyWizard source tree.

If you're interested in designing scenarios, units, abilities, and so on, you probably only need to read all about the files in `data/`.

If you intend to develop GalaxyWizard code, the files in `src/` are probably most important, but you'll probably also want an idea of how the stuff in `data/` works.

## ./

The root directory of the GalaxyWizard source tree. Contents:

`GalaxyWizard.py` - the main GalaxyWizard script. Imports `src/Main.py` and executes the `main()` function defined there.

`*.txt` - top-level documentation files.

## data/

The directory containing all the GalaxyWizard data files. This includes images, sounds, music, and all the configuration files that define classes, abilities, scenarios, maps, and so on.

The `data/` directory has at least three subdirectories:

### data/core

These are the "core" files that can be used by any GalaxyWizard campaign. This includes the base unit classes, the abilities required by these classes, unit sprites, fonts, sound effects, and some plain-text files.

### data/extra

This contains additional data files that would be part of `data/core/`, but are considered "optional". Basically, this directory is for big data files (such as music) that we might eventually want to bundle separately, so that players with slow Internet connections can still download GalaxyWizard reasonably quickly.

### data/some-campaign-name

Every GalaxyWizard campaign lives in a separate subdirectory of `data/`. A campaign's directory contains the maps, scenarios, and unit definitions that are used by that campaign. It may also contain extra class definitions, abilities, sprites, sound effects, music, and so on, that aren't available in the "core" data files. GalaxyWizard is currently distributed with one campaign, in `data/demo/`, that contains a few simple scenarios. If you want to start on your own campaign, you should start by creating a separate directory under `data/`.

### How data files are loaded

All files in the `data/` directory are loaded by the code in the file `src/Resources.py`. Files are referred to by a name that contains no subdirectories and no filename extension, such as "cursor-click". The `Resources` module takes care of looking at all the right places to find the file. First, it looks in the current campaign directory; then, it looks in the `extra` directory; finally, it looks in the `core` directory. `Resources` knows what type of file is being asked for, and uses that to determine which subdirectories to look in and what filename extension to add. For instance, sound files need to be in a subdirectory called `sounds`, and might end in either `.ogg` or `.wav`. So if the current campaign is called "demo", `Resources` will look for the file "cursor-click" in the following locations:

```
data/demo/sounds/cursor-click.ogg
data/demo/sounds/cursor-click.wav
data/extra/sounds/cursor-click.ogg
data/extra/sounds/cursor-click.wav
data/core/sounds/cursor-click.ogg
data/core/sounds/cursor-click.wav
```

The first file found is the one that will be used. If none of these paths contains the desired file, an error will occur. This error will be handled gracefully if it's an optional sort of file, such as a sound or music file, but much less gracefully if it's something important, like a class definition or a map file. :)

I mentioned before that the `Resources` knows to look in the `sounds` subdirectories to find sounds. Here's a list of all the subdirectories for different types of data files.

**`data/*/abilities`**
Files defining abilities that are used by units in battle.

**`data/*/classes`**
Files defining unit classes.

**`data/*/fonts`**
TrueType font files.

**`data/*/images`**
Images. These are mostly unit sprites. All image files are in the PNG format. Alpha values (translucency) are fully supported by GalaxyWizard.

**`data/*/maps`**
Files defining our 3D battle maps.

**`data/*/music`**
Music files, in `.ogg` format.

**`data/*/scenarios`**
Files defining scenarios. A scenario tells GalaxyWizard all it needs to know about setting up a battle, including the map name, the units on each team, the lighting environment, and so on.

**`data/*/sounds`**
Sound effects, in `.ogg` or `.wav` format.

**`data/*/text`**
Miscellaneous text files.

**`data/*/textures`**
Texture files. Like all other images, these are in PNG format.

**`data/*/units`**
Files defining the individual units that are used in scenarios.

## doc/

All the GalaxyWizard documentation is contained here.

## src/

All the GalaxyWizard source code is contained here. Important contents:

`Main.py` - The main script. This is what runs when GalaxyWizard is executed. Parses command-line arguments, detects whether needed libraries are installed, sets up logging, sets up the main window, and starts the desired scenario.

`Resources.py` - This file is the interface for loading all sorts of data files off the disk. For more information, see the "How data files are loaded" section above.

`Sound.py` - Code for setting up pygame's mixer system and playing sound effects on various channels.

### src/ai

This directory contains all code related to opponent AI.

### src/engine

This directory contains all code relating to the game engine itself. Important contents:

`Ability.py, Effect.py, Range.py` - These files all deal with abilities, their ranges, and effects.

`Battle.py` - The battle engine itself. Determines the turn order, notifies the GUI or AI when it's time for the player or opponent to act, applies movement and action commands, and checks victory conditions.

`Class.py` - This file deals with unit classes.

`Faction.py` - Code relating to unit factions -- whether different units are hostile, friendly, or neutral toward one another.

`Light.py` - Defines lights and lighting environments.

`Map.py` - Code relating to the battle map, including the definition of the map itself, breadth-first search on the map, calculation of movement ranges, calculation of nearest units to a given point, and so on.

`Name.py` - Picks random names for units based on their genders.

`Scenario.py` - Defines scenarios.

`Unit.py` - Defines units.

### src/gui

This directory contains all user-interface code. Importnat files here include:

`Camera.py` - Keeps track of the current camera position and has some utility functions for calculating stuff based on the camera position. For instance, it can sort sprites in back-to-front order so that they are alpha-blended properly.

`Clock.py` - Utility code for an FPS clock.

`Cursor.py` - Code for moving around the on-screen cursor -- the blue square on the battle map. This is where the player chooses where his units move and attack.

`Geometry.py` - Utility geometry routines.

`GLUtil.py` - Contains a bunch of OpenGL convenience functions... rendering text to a texture, drawing cubes and sprites on screen, and so on.

`MainWindow.py` - The main window. Contains code for initializing the pygame/PyOpenGL systems, handling window resize events, handling some other events, and counting/limiting FPS. The MainWindow doesn't actually draw anything -- it delegates responsibility for that to another object, such as ScenarioGUI.

`ScenarioGUI.py` - A delegate for displaying an entire scenario. Draws the map, cursor, unit sprites, battle menus, and so on.

`Sprite.py` - Definitions of sprites, including unit sprites, on-screen text displayers, and menus.

## tools/

This directory contains scripts and tools that might be useful to GalaxyWizard developers, but not to players. For example, `tools` contains the scripts used to build the Windows and Macintosh binaries when we do an official release.
