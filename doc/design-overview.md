# Design Overview

This page gives a high-level overview of all the major components of a GalaxyWizard campaign. By the time you're done reading this page, you should have a good understanding of how all the pieces fit together. After continuing on to learn about the GalaxyWizard [directory structure](directory-structure.md) and [config file format](config-file-format.md), you'll know all you need to know to start on your own GalaxyWizard campaign!

## Campaigns

A *campaign* is basically a complete game that uses the GalaxyWizard engine. Right now, GalaxyWizard ships with one campaign, called "demo", that simply has a few demonstration scenarios. In future releases, we will start to distribute one or more official campaigns along with GalaxyWizard. Right now, true campaigns aren't implemented yet -- you can't actually string sequences of battles together in the engine. But that doesn't mean you can't design the different scenarios now, and use them later.

## Scenarios

A campaign mostly consists of a group of related *scenarios*. Each scenario defines a single battle. Right now, a scenario file specifies:

- The *map* that the battle will take place on.
- The *units* possessed by each *faction* of the battle.
- The *ending conditions* for the battle.
- The *lighting* and *music* to use for the battle.

Soon, we will add the ability to specify what happens when each ending condition is satisfied -- that is, you'll be able to actually string scenarios together into a true campaign. For now, the player's units and their positions on the field are specified in the scenario file. Eventually, the player will be able to choose which units he/she would like to fight with, and place them in an initial region of the battlefield.

## Maps

A *map* is the environment in which a battle occurs. A map can be used by multiple scenarios, if you would like multiple battles to take place on the same battlefield. A map file specifies:

- The width and height of the map.
- The height of each map square.
- Other attributes for each map square, such as a color, a texture, and so on.

## Units

*Units* are the actual characters that participate in a battle. We call them "units" instead of "characters" because the word "character" is used for many different things in computer programming, and it's slightly less confusing for developers that way. :) Each unit includes:

- A bunch of different *stats*, which determine the unit's performance in battle.

- A *class*, which determines (among other things) how the unit's stats grow when it gains a level, and the abilities available to the unit. We plan on eventually adding *multiclassing*, which will allow a unit to advance in different classes to learn different sorts of abilities.

- *Abilities*, which are different skills that can be used in combat. The only abilities implemented so far are *action abilities*, which are chosen by the player (or AI) as an action during battle. These abilities are listed under the "Special" menu option.

- A set of sprites, which determine how the unit looks when displayed on screen.

- A gender, which is used to determine what the unit looks like and to choose a name for the unit. (This is all that gender will ever affect.)

- A name, which is chosen randomly based on the unit's gender.

- If the unit is computer-controlled, it contains an *AI*, which will choose actions for the unit during battle. Each unit has its own AI because eventually we will have the ability to create units with different "personalities" -- some units might be foolhardy, some might be timid, others might be concerned about keeping their friends alive, and so on.

Eventually, units will have even more things, such as equipment and weaknesses/strengths to different types of damage, but none of that is implemented yet.

## Classes

As mentioned before, every unit has a *class*. When a unit is first created, it has an *initial class*, which determines the *base values* of the unit's stats. Every time the unit gains a level, it chooses a class to level up in -- and its stats grow based on the *growth values* specified by the class. Classes also define a *multiplier value* for each stat. This will be used once multiclassing is implemented. For now, you don't have to worry about it.

Each class also contains a list of *abilities*, and how many levels a unit has to take in that class in order to learn each ability. So as a unit gains levels in a class, it will learn new abilities.

Each class also defines a set of sprites that will be used to display units that are of that class. These sprites can be overridden on a per-unit basis, but for most units you'll simply want to use the default class sprites.

## Abilities

Right now, the only abilities implemented are *action abilities* -- abilities that the player (or AI) can choose as an action during battle. Eventually there may be other types of abilities. The basic "Attack" command is also implemented as an action ability. The specific ability depends on which type of weapon the unit is wielding, so if the unit is wielding a sword, the "sword" ability will be used. (Since equipment isn't implemented yet, all "Attack" actions currently use the "sword" ability.) An ability contains:

- A name and description, which are displayed to the player.

- A *cost*: the amount of SP required to use the ability. Some abilities (such as the basic attack abilities) have a cost of 0.

- A *target type*: which targets are affected by the ability. This can be either FRIENDLY, HOSTILE, or FRIENDLY_AND_HOSTILE.

- A *range*: an area that says where the ability can be targeted, relative to the unit's current position. There are many different types of ranges available, including circles, squares, and crosses.

- An *area of effect*, or *AOE*: the area around the targeted area that is also affected by the ability. A simple attack will usually have an AOE of just the single square that is targeted, but special attacks can have AOEs or arbitrary shape, including circles, squares, and crosses.

- A list of *effects*, which determine what happens to each target that is affected by the ability. Right now, the only types of effects are damage and healing; later, we will implement various sorts of status effects.

- A sound that is played when the action is initiated.

Later, we will add more user-interface fields to the actions, such as the sound to make when the ability hits a target, some graphics/animations to use to display the ability as it's used, and so on.

# Conclusion

Now you know all about the various components of a GalaxyWizard campaign. Before going further, you might want to read about the GalaxyWizard [directory structure](directory-structure.md), especially about the contents of the `data/` directory. Then you can read about the basic GalaxyWizard [config file format](config-file-format.md) and get started writing your own scenarios, maps, abilities, and so on!
