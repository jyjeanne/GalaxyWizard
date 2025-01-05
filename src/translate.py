import gettext
import os


class Translate:

    @staticmethod
    def getLanguageDict(lang):
        locale_path = os.path.join(os.getcwd(), 'locale')
        gettext.bindtextdomain('GalaxyMage', locale_path)
        gettext.textdomain('GalaxyMage')
        return gettext.translation('GalaxyMage', locale_path, languages=[lang])

    def __init__(self):
        # fill our language dictionary with each language
        self.langDict = {'fr': self.getLanguageDict('fr'),
                         'en': self.getLanguageDict('en')}

        #and install current langauge
        #gettext.install('GalaxyMage', unicode=1)
        pass

    def setLanguage(self, lang=None):
        # look if we have this language
        if lang != None and lang in self.langDict:
            self.langDict[lang].install()
        else:  # install default language
            self.langDict['en'].install()
