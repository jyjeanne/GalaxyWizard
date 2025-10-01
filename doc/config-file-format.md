# Config File Format

Each data file is actually written in the Python language. This is just done for convenience, as it makes loading the data files a snap. So it might help to get a text editor that supports Python syntax highlighting, as it will be easier to notice if you make some sort of error. Don't think that the data files will be difficult to write just because we use Python to write them -- all the file formats have been designed to be easy to edit, even if you have no knowledge of programming.

If you are familiar with Python, the format of the data files is probably immediately obvious to you, and you can skip most of the details that are here.

## Config file types

There are a wide variety of things that can be specified in config files: scenarios, units, classes, abilities, and so on. All the config files share the same basic format, but when you want to create a specific type of thing (such as an ability) you'll need to look at the specific reference for that type of thing to find out the full details -- such as what sorts of things you need to specify. References for each type of config file can be found at the bottom of this page.

## Sample config file

Here's a sample config file. It defines the "Dart" ability. (You can find the latest version of this file in `data/core/abilities/dart.py`.)

---

```
# "Dart" action ability.

VERSION = 1

NAME = "Dart"
DESCRIPTION = "Throw a dart."
COST = 5

ABILITY_TYPE = ACTION
TARGET_TYPE = HOSTILE

RANGE = Circle(1, 4)
AOE = Single()

EFFECTS = [Damage(power=1.25, damageType=PHYSICAL)]

SOUND = 'sword-hit-large'
```

---

Every type of data file has some number of *keys* that have to be given *values*. Some of these keys are required, and some are optional. For more information on which keys you need to fill in, you need to look at the reference for that particular type of data file. For an ability file, we must specify values for the most of these keys (such as `COST` and `TARGET_TYPE`), but the `SOUND` key is optional.

The basic syntax is `SOME_KEY = some_value`. The `SOME_KEY` needs to start in the first column (all the way to the left).

Blank lines are ignored. Any line can contain a comment. Comments start with a pound sign (`#`) and continue to the end of the line. Any text inside a comment is ignored.

All config files have a `VERSION` key. This is the version of the *config file format*, not the version of the specific thing you are working on. For now, `VERSION` should always be set to `1`. If we come up with a new file format in the future, GalaxyWizard can use the `VERSION` numbers to know the correct way of loading both the old and new files.

Each value needs to be a specific type. For instance, `COST` has to be an integer. Again, the reference for the specific file type will tell you what kind of value each key requires. Here's a summary of the various types, and how you write them:

- **Integer**: a whole number. You specify an integer in the obvious way, like this: `2`, `13`, `42`, etc. In the example above, the value assigned to `COST` is an integer.

- **Float**: a floating-point number (number with a decimal point.) You specify a float in the obvious way: `1.25`, `3.0`, etc. A float is used in part of the value of the `EFFECTS` key.

- **String**: a sequence of characters enclosed in quotes. You can use either single-quotes or double-quotes; there is no difference between the two. Examples: `"Dart"`, `'sword-hit-large'`. Strings are often used to specify file names. For instance, the `SOUND` key is used to specify which sound file to play when the "dart" action occurs.

- **List**: a list of values, enclosed in square brackets and separated by commas. Often, the values in the list need to have a certain type. For instance, a list of integers would look like this: `[2, 5, 3, 4]`; a list of strings would look like this: `['this', 'is', 'a', 'list']`. You can also use parentheses instead of square brackets: `(1, 2, 3, 4)`. Like with strings, there is no difference between using brackets or parentheses.

- **Enumerations**: sometimes, there are only a couple possible choices for a value. For instance, there are only 3 valid values for `TARGET_TYPE`: `HOSTILE`, `FRIENDLY`, and `FRIENDLY_AND_HOSTILE`. If a key requires an enumeration, the reference for the type of data file you are working on will tell you what values are allowed.

- **Object**: some specific Python object. Objects are similar to enumerations in that the valid values will be explained in the reference for the type of data file you are working on. The difference is that objects can take *parameters* -- extra values that provide additional configuration flexibility. This is what `Circle(1, 4)` and `Single()` are -- specific Python objects that represent a circle with radius 4 and a single square, respectively.

# Data File References

[Map file format](maps/index.md)

[All other file formats](file-formats.md)
