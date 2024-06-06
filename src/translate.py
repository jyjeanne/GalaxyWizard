import gettext
import os


class Translate:

    @staticmethod
    def getLanguageDict(lang):
        return gettext.translation('GalaxyWizard', os.path.join(os.getcwd(), 'locale'), languages=[lang])

    def __init__(self):
        # fill our language dictionary with each language
        self.langDict = {'sp': self.getLanguageDict('sp'),
                         'fr': self.getLanguageDict('fr'),
                         'en': self.getLanguageDict('en'),
                         'nl': self.getLanguageDict('nl')}

        #and install current langauge
        #gettext.install('GalaxyWizard', unicode=1)
        pass

    def setLanguage(self, lang=None):
        # look if we have this language
        if lang != None and lang in self.langDict:
            self.langDict[lang].install(str=1)
        else:  # install default language
            gettext.install('GalaxyWizard', str=1)
