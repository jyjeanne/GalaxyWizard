# Changelog

## Version 0.2.0

### Content

The "adept", "squire", and "scout" classes have been replaced with six new classes that will be considered our core classes: "fighter", "defender", "rogue", "archer", "healer", and "mage". Stats of all these classes have been tweaked. A few new abilities have been added for the new classes.

A random map generator and random scenario generator have been added.

New "win" and "loss" music.

### Battle Engine

Units can now wear weapons and armor. Some basic weapons and armor have been added to the data/core/items directory. The sounds played when attacking with a weapon now depend on the type of weapon (so bows make an arrow noise, swords make a clangy noise, and so on.)

Ranged attacks can now be targeted up to 16 height-units up/down from the unit's position. (The previous value was 8.)

### User Interface

Scenarios can now be chosen from the GUI instead of only from the command-line. After a battle is complete, GalaxyWizard returns to the GUI scenario chooser so that the player can pick another scenario to play.

You can now cancel a unit's move if it has not yet acted. (Just press the escape key until the unit returns to its old position.)

Preliminary joystick support added.

The camera behavior is now a bit better on maps with significant height differences (units stay centered without the need to zoom in and out).

The camera can now be rotated smoothly by right-clicking and draggins left/right.

The highlights showing unit movement ranges have been changed from green to cyan. This makes it a bit easier to see the movement ranges on green grassy areas.

We now use linear filtering to smooth unit sprites when they are viewed close-up.

Fix for a bug where the camera would oscillate wildly for players with very low FPS.

### AI

The AI has been improved significantly. It actually makes use of special attacks, healing, and so on. It's currently a bit unoptimized, so might take a bit of time in some circumstances. The AI now runs in a separate thread. The battle engine is currently responsible for displaying the actions taken by the AI. Previous scenarios have been rebalanced to account for the stronger AI.

### Translation

Infrastructure for translation has been added. A translation of GalaxyWizard into French is underway.

## Version 0.1.2

### Content

Added a new map and a scenario for that map. The map includes a hill, ravine, and river.

### Battle Engine

Dead units now disappear from the battlefield.

### User Interface

The main window is now resizable.

After an action is complete, the camera focus remains on the unit for a short period of time, to ensure that the player can see the effects of the action.

Added keybinding: Home/End now rotate the map (in addition to brackets), for users who do not have bracket keys on their keyboards.

Added mouse binding: the map can also be rotated by right-clicking and dragging to the left or right.

Added keybinding: hit F12 to toggle fullscreen during play. Unfortunately, this only works in Linux.

If a scenario isn't specified on the command-line, the scenario will be chosen randomly.

### Design Tools

Implemented a preliminary tool to make map-building easier.

Scenario designers can now set the sky color of their scenarios. If left unset, it defaults to the fog color; if the fog color is also unset, it defaults to a dark blue.

### Documentation

Added a lot more documentation for designers: an overview of all the components of a GalaxyWizard campaign, basic config file format information, and a detailed tutorial on creating maps by hand.

### Miscellaneous

New "GM" icon.

Started using Python's built-in logging module. The old "-d" command-line option has been replaced by "-v". A lot more system information is now logged to the debug steam.

Fixed some graphics issues -- surface normals for the tops of map squares now seem to be working properly for squares with non-zero corner heights. Some mild performance improvements.

## Version 0.1.1

Bug fix for crash that occurs on machines without sound cards (pygame.mixer unable to initialize).

## Version 0.1.0

Initial release.
