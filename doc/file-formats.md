# File Formats Reference

This document will eventually be a complete reference for all the different GalaxyWizard config file formats. Unfortunately, it's currently incomplete... some options aren't yet documented. We're working on it. :) But some documentation is better than no documentation, and you'll probably do just fine if you look at some examples and work from those.

## Scenario Files

[Sample file](http://svn.gna.org/viewcvs/tactics/trunk/data/demo/scenarios/castle.py?view=markup)

| Key | Req. | Type | Comments |
|-----|------|------|----------|
| MAP | X | string | Name of the map file to load. |
| ENDING_CONDITIONS | X | list of enumerations | For now, this should always be set as follows:<br><pre>ENDING_CONDITIONS = [Battle.PLAYER_DEFEATED,<br>                     Battle.DEFEAT_ALL_ENEMIES]</pre> |
| FACTIONS | X | list of Faction objects | Undocumented |
| LIGHTING | - | Light.Environment object | Undocumented |
| MUSIC | - | string | Filename of a music file to play during the battle. |

## Units

[Sample file](http://svn.gna.org/viewcvs/tactics/trunk/data/demo/units/adept1.py?view=markup)

| Key | Req. | Type | Comments |
|-----|------|------|----------|
| CLASSES | X | list of lists | Undocumented |
| GENDER | X | enumeration | Set to MALE, FEMALE, or NEUTER. |

## Classes

[Sample file](http://svn.gna.org/viewcvs/tactics/trunk/data/core/classes/adept.py?view=markup)

| Key | Req. | Type | Comments |
|-----|------|------|----------|
| NAME | X | string | The class name that is displayed to the player. |
| MOVE | X | integer | Base movement distance for a unit that has this class. |
| JUMP | X | integer | Base jump height for a unit that has this class. |
| *_BASE | X | integer | Base stat value for a unit that starts in this class. |
| *_GROWTH | X | float | The average amount that this stat increases by every time a unit levels in this class. |
| *_MULT | X | float | Will be used for multi-classing; always set to `1.0` for now. |
| SPRITE_ROOT | X | string | Used to determine which sprites to load to display the unit. For example, if SPRITE_ROOT is set to "squire", the default standing pose for the unit will be `squire-male-standing-1.png` (assuming the unit is male). |
| ABILITIES | X | list of lists | Undocumented |

## Abilities

[Sample file](http://svn.gna.org/viewcvs/tactics/trunk/data/core/abilities/dart.py?view=markup)

| Key | Req. | Type | Comments |
|-----|------|------|----------|
| NAME | X | string | The ability name that is displayed to the player. |
| DESCRIPTION | X | string | A description of the ability. Also displayed to the player. |
| COST | X | integer | The cost of the ability, in SP. Can be set to 0 for abilities that don't require SP. |
| ABILITY_TYPE | X | enumeration | Always set this to ACTION for now. |
| TARGET_TYPE | X | enumeration | Set to one of: HOSTILE, FRIENDLY, FRIENDLY_AND_HOSTILE. |
| RANGE | X | Range object | Range of the attack. Valid values are currently undocumented... sorry. |
| AOE | X | Range object | Area-of-effect of the attack. Valid values are currently undocumented... sorry. |
| EFFECTS | X | list of Effect objects | Undocumented |
| SOUND | - | string | Filename of a sound file that should be played when the ability is used. |
