# How translations works in GalaxyWizard

## About Gettext framework

GalaxyWizard uses the gettext framework. This framework is easy to use for a developper point of view and powerfull for the translator. If you want to know more about gettext, go to [gettext site](http://www.gnu.org/software/gettext/)

## Developper point of view

For a developper, the translations task aims to translate text string or redifine filename for a specific language.

### Translate string

If you want to translate a string, simply call _ method with the string. No more things to do!

This is the dummy example:

```python
print _("Hello world")
```

if "Hello world" is found in the french dictionnary, the print will ouput *Salut le monde* else the string is return by _(...) so *Hello world* will be printed

### Filename

If a filename must be specific for a language, for example for a voice sound file, we use the same method as string!

Since a filename is a string, we use the same method, this is the code use in Name.py to load specific name:

```python
__maleNames = Resources.text(_("names-male"))
```

So if a language provides a specific names-male, the dictionnary will contais the specific name and it will be return by _(...).

In this example, in french language the key names-male is link to *noms-homme*

## Translator point of view

FIXME: to be define !
