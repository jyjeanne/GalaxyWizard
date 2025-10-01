import gettext
import os
import builtins


class Translate:

    @staticmethod
    def getLanguageDict(lang):
        locale_path = os.path.join(os.getcwd(), 'locale')
        try:
            gettext.bindtextdomain('GalaxyWizard', locale_path)
            gettext.textdomain('GalaxyWizard')
            return gettext.translation('GalaxyWizard', locale_path, languages=[lang])
        except FileNotFoundError:
            # Return a null translation that just passes through strings
            return gettext.NullTranslations()

    def __init__(self):
        # fill our language dictionary with each language
        self.langDict = {}
        for lang in ['fr', 'en']:
            self.langDict[lang] = self.getLanguageDict(lang)

        # Install a default translation function if none exists
        if not hasattr(builtins, '_'):
            builtins._ = lambda x: x

    def setLanguage(self, lang=None):
        # look if we have this language
        if lang != None and lang in self.langDict:
            self.langDict[lang].install()
        else:  # install default language
            self.langDict['en'].install()