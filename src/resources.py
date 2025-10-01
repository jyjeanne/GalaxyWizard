import logging
import pygame
import os
import sys
from gui import GLUtil
import re
import random

logger = logging.getLogger('reso')

# Cache for file lookups to avoid repeated filesystem checks and log spam
_filename_cache = {}


# Determine the base path for data files
# When running as PyInstaller executable, use sys._MEIPASS
# When running normally, use the directory containing this file
def _get_base_path():
    """Get the base path for the application (handles PyInstaller)."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller executable
        return sys._MEIPASS
    else:
        # Running normally
        return os.path.dirname(os.path.abspath(__file__))


# getFilename("images", "arch-mage.png") ->
# "campaigns/common/images/arch-mage.png"
def _getFilename(base, name):
    # Check cache first to avoid repeated filesystem checks and log spam
    cache_key = (campaign, base, name)
    if cache_key in _filename_cache:
        return _filename_cache[cache_key]

    logger.debug('finding file for (%s, %s)' % (str(base), str(name)))
    sep = os.path.sep
    if sep == '\\':
        sep = r'\\'
    base = re.sub(r'/', sep, base)
    name = re.sub(r'/', sep, name)

    base_path = _get_base_path()

    result = os.path.join(base_path, "data", campaign, base, name)
    if os.path.exists(result):
        logger.debug('found ' + result)
        _filename_cache[cache_key] = result
        return result
    result = os.path.join(base_path, "data", "extra", base, name)
    if os.path.exists(result):
        logger.debug('found ' + result)
        _filename_cache[cache_key] = result
        return result
    result = os.path.join(base_path, "data", "core", base, name)
    if os.path.exists(result):
        logger.debug('found ' + result)
        _filename_cache[cache_key] = result
        return result

    # Cache the negative result to avoid repeated lookups
    # Only log once per missing file to reduce spam
    logger.debug('no suitable file found')
    _filename_cache[cache_key] = None
    return None


class FontLoader(object):
    def __init__(self):
        self.fonts = {}
        self.files = {"sans": {False: "vera/Vera.ttf",
                               True: "vera/VeraBd.ttf"},
                      "serif": {False: "vera/VeraSe.ttf",
                                True: "vera/VeraSeBd.ttf"},
                      "mono": {False: "vera/VeraMono.ttf",
                               True: "vera/VeraMoBd.ttf"}}

    def __call__(self, family="sans", size=16, bold=True):
        key = (family, size, bold)
        if key not in self.fonts:
            if family not in self.files:
                raise Exception('Font family should be "sans", "serif"' +
                                ', or "mono"')
            filename = self.files[family][bold]
            fontFile = _getFilename("fonts", filename)
            if fontFile == None:
                raise Exception('Font file "%s" not found' % filename)
            f = pygame.font.Font(fontFile, size)
            self.fonts[key] = f
        return self.fonts[key]


class MapLoader(object):
    def __call__(self, mapName):
        import engine.Map as Map
        if mapName == 'random':
            import engine.MapGenerator as MapGenerator
            return MapGenerator.generateRandom()
        if (not '/' in mapName) and (not '.' in mapName):
            filename = mapName + ".py"
            mapName = _getFilename("maps", filename)
        if mapName == None:
            raise Exception('Map file "%s" not found' % filename)
        return Map.MapIO.load(mapName)


class ImageLoader(object):
    def __init__(self):
        self.cache = {}

    def __call__(self, imageName, dirName="images"):
        if imageName not in self.cache:
            filename = imageName + ".png"
            fileName = _getFilename(dirName, filename)
            if fileName == None:
                raise Exception('Image file "%s/%s" not found' % (dirName,
                                                                  filename))
            self.cache[imageName] = pygame.image.load(fileName)
            if pygame.display.get_surface() != None:
                self.cache[imageName] = self.cache[imageName].convert_alpha()
        return self.cache[imageName]


class TextureLoader(object):
    def __init__(self):
        self.cache = {}
        self._textureSize = 64

    def setTextureSize(self, textureSize):
        """Set texture size and clear cache."""
        self.clear()  # Properly clear old textures before resizing
        self._textureSize = textureSize

    def __call__(self, textureName):
        if textureName not in self.cache:
            i = image(textureName, "textures")
            i = pygame.transform.scale(i, (self._textureSize,
                                           self._textureSize))
            textureID = GLUtil.makeTexture(i)[0]
            self.cache[textureName] = textureID
        return self.cache[textureName]

    def clear(self):
        """Clear texture cache and free OpenGL resources."""
        if not self.cache:
            return

        try:
            from OpenGL.GL import glDeleteTextures, glIsTexture
            for textureName, textureID in list(self.cache.items()):
                try:
                    if glIsTexture(textureID):
                        glDeleteTextures([textureID])
                except Exception as e:
                    import logging
                    logging.warning(f"Failed to delete texture {textureName}: {e}")
            self.cache = {}
        except Exception as e:
            import logging
            logging.error(f"Error clearing texture cache: {e}")
            # Still clear cache dict even if GL cleanup failed
            self.cache = {}

    def __del__(self):
        """Cleanup textures when loader is destroyed."""
        try:
            self.clear()
        except:
            # Ignore errors during shutdown
            pass


class ScenarioLoader(object):
    def __call__(self, scenarioName):
        import engine.Scenario
        if scenarioName == 'random':
            return engine.Scenario.generateRandom(0)
        if scenarioName == 'random-1':
            return engine.Scenario.generateRandom(1)
        if scenarioName == 'random-2':
            return engine.Scenario.generateRandom(2)
        filename = scenarioName + ".py"
        scenarioFilename = _getFilename("scenarios", filename)
        if scenarioFilename == None:
            raise Exception('Scenario file "%s" not found' % filename)
        return engine.Scenario.ScenarioIO.load(scenarioFilename)


class AbilityLoader(object):
    def __init__(self):
        self.cache = {}

    def __call__(self, abilityName):
        if abilityName not in self.cache:
            import engine.Ability as Ability
            filename = abilityName + ".py"
            f = _getFilename("abilities", filename)
            if f == None:
                raise Exception('Ability file "%s" not found' % f)
            with open(f, "r") as abilityFile:
                abilityText = abilityFile.read()

            globalVars = {}
            localVars = {}

            module = compile("from engine.Equipment import Weapon",
                             "Equipment.py", "exec")
            eval(module, globalVars)

            module = compile("from engine.Range import *",
                             "Range.py", "exec")
            eval(module, globalVars)
            module = compile("from engine.Ability import ACTION, FRIENDLY, HOSTILE, " +
                             "FRIENDLY_AND_HOSTILE, WEAPON_SOUND",
                             "Ability.py", "exec")
            eval(module, globalVars)
            module = compile("from engine.Effect import *",
                             "Effect.py", "exec")
            eval(module, globalVars)

            compiled = compile(abilityText, abilityName + ".py", 'exec')
            eval(compiled, globalVars, localVars)
            abilityData = localVars

            if abilityData['VERSION'] != 1:
                raise Exception("Ability version not recognized")

            if abilityData['ABILITY_TYPE'] != Ability.ACTION:
                raise Exception("Only action abilities are supported")

            name = abilityData['NAME']
            targetType = abilityData['TARGET_TYPE']
            range_ = abilityData['RANGE']
            aoe = abilityData['AOE']
            effects = abilityData['EFFECTS']

            requiredWeapons = []
            if 'REQUIRED_WEAPONS' in abilityData:
                requiredWeapons = abilityData['REQUIRED_WEAPONS']

            cost = 0
            if 'COST' in abilityData:
                cost = abilityData['COST']

            sound = None
            if 'SOUND' in abilityData:
                sound = abilityData['SOUND']

            description = abilityData['DESCRIPTION']

            ability = Ability.Ability(name, description, cost, targetType,
                                      requiredWeapons,
                                      range_, aoe, effects, sound)
            self.cache[abilityName] = ability
        return self.cache[abilityName]


class ClassLoader(object):
    def __init__(self):
        self.cache = {}

    def _loadClass(self, className):
        import engine.Class as Class_
        filename = _getFilename("classes", className + ".py")
        if filename == None:
            raise Exception('Class file "%s" not found' % filename)
        with open(filename, "r") as classFile:
            classText = classFile.read()

        globalVars = {}
        localVars = {}

        compiled = compile(classText, className + ".py", 'exec')

        eval(compiled, globalVars, localVars)
        classData = localVars
        if classData['VERSION'] != 1:
            print("Class version not recognized")

        abilities = []
        if 'ABILITIES' in classData:
            abilities = classData['ABILITIES']

        spriteRoot = classData['SPRITE_ROOT']

        self.cache[className] = Class_.Class(classData['NAME'],
                                             abilities,
                                             spriteRoot,
                                             classData['MOVE'],
                                             classData['JUMP'],
                                             classData['HP_BASE'],
                                             classData['HP_GROWTH'],
                                             classData['HP_MULT'],
                                             classData['SP_BASE'],
                                             classData['SP_GROWTH'],
                                             classData['SP_MULT'],
                                             classData['WATK_BASE'],
                                             classData['WATK_GROWTH'],
                                             classData['WATK_MULT'],
                                             classData['WDEF_BASE'],
                                             classData['WDEF_GROWTH'],
                                             classData['WDEF_MULT'],
                                             classData['MATK_BASE'],
                                             classData['MATK_GROWTH'],
                                             classData['MATK_MULT'],
                                             classData['MDEF_BASE'],
                                             classData['MDEF_GROWTH'],
                                             classData['MDEF_MULT'],
                                             classData['SPEED_BASE'],
                                             classData['SPEED_GROWTH'],
                                             classData['SPEED_MULT'])

    def __call__(self, classname):
        if classname not in self.cache:
            self._loadClass(classname)
        return self.cache[classname]


class UnitLoader(object):
    def __call__(self, unitName):
        import engine.Unit as Unit
        import engine.Equipment as Equipment
        filename = unitName + ".py"
        unitFilename = _getFilename("units", filename)
        if unitFilename == None:
            raise Exception('Unit file "%s" not found' % filename)
        with open(unitFilename, "r") as unitFile:
            unitText = unitFile.read()

        globalVars = {}
        localVars = {}

        # Load required modules
        module = compile("from engine.Unit import MALE, FEMALE, NEUTER, FEMALE_OR_MALE",
                         "Unit.py", "exec")
        eval(module, globalVars)

        # Load actual unit
        compiled = compile(unitText, unitFilename, 'exec')
        eval(compiled, globalVars, localVars)
        unitData = localVars

        # Process fields
        if unitData['VERSION'] != 1:
            print("Unit version not recognized")

        # Gender
        gender = Unit.NEUTER
        if 'GENDER' in unitData:
            gender = unitData['GENDER']
            if gender == Unit.FEMALE_OR_MALE:
                if random.random() < 0.5:
                    gender = Unit.FEMALE
                else:
                    gender = Unit.MALE

        # Required field: classes
        classes = unitData['CLASSES']
        (initialClassName, initialClassLevels) = classes[0]
        initialClass = class_(initialClassName)
        unit = initialClass.createUnit(gender)
        latestClass = initialClass
        for i in range(1, initialClassLevels):
            initialClass.levelUp(unit)
        for i in range(1, len(classes)):
            (className, classLevels) = classes[i]
            class__ = class_(className)
            latestClass = class__
            for j in range(0, classLevels):
                class__.levelUp(unit)

        # Weapon (if specified)
        if 'WEAPON' in unitData:
            weapon = equipment(Equipment.WEAPON, unitData['WEAPON'])
            unit.equipWeapon(weapon)
        if 'ARMOR' in unitData:
            armor = equipment(Equipment.ARMOR, unitData['ARMOR'])
            unit.equipArmor(armor)

        # Sprites (if specified)
        spriteRoot = latestClass.spriteRoot()
        if 'SPRITE_ROOT' in unitData:
            spriteRoot = unitData['SPRITE_ROOT']
        unit._spriteRoot = spriteRoot

        return unit


class EquipmentLoader(object):
    def __init__(self):
        self.cache = {}

    def __call__(self, type_, equipmentName):
        if equipmentName not in self.cache:
            import engine.Equipment as Equipment

            if type_ == Equipment.WEAPON:
                subdir = 'weapons'
            elif type_ == Equipment.ARMOR:
                subdir = 'armor'

            filename = equipmentName + ".py"
            equipmentFilename = _getFilename("items/" + subdir, filename)
            if equipmentFilename == None:
                raise Exception('Equipment file "%s" not found' % filename)
            with open(equipmentFilename, "r") as equipmentFile:
                equipmentText = equipmentFile.read()

            globalVars = {}
            localVars = {}

            # Load required modules
            module = compile("from engine.Equipment import Weapon",
                             "Equipment.py", "exec")
            eval(module, globalVars)

            # Load actual equipment
            compiled = compile(equipmentText, equipmentFilename, 'exec')
            eval(compiled, globalVars, localVars)
            equipmentData = localVars

            name = equipmentData['NAME']
            stats = {}
            stats['mhp'] = equipmentData.get('MHP', 0)
            stats['msp'] = equipmentData.get('MSP', 0)
            stats['watk'] = equipmentData.get('WATK', 0)
            stats['wdef'] = equipmentData.get('WDEF', 0)
            stats['matk'] = equipmentData.get('MATK', 0)
            stats['mdef'] = equipmentData.get('MDEF', 0)
            stats['move'] = equipmentData.get('MOVE', 0)
            stats['jump'] = equipmentData.get('JUMP', 0)
            stats['speed'] = equipmentData.get('SPEED', 0)

            if type_ == Equipment.WEAPON:
                weaponType = equipmentData['TYPE']
                self.cache[equipmentName] = Equipment.Weapon(name,
                                                             stats,
                                                             weaponType)
            elif type_ == Equipment.ARMOR:
                self.cache[equipmentName] = Equipment.Armor(name, stats)

            #Sprites (if specified)
            #spriteRoot = latestClass.spriteRoot()
            spriteName = None
            if 'SPRITE_ROOT' in equipmentData:
                spriteRoot = equipmentData['SPRITE_ROOT']
                #spriteName = "%s-%s-%s-%d" % (spriteRoot, genderStr, "standing", 1)
                spriteName = spriteRoot
            if spriteName != None and not _getFilename("images", spriteName + ".png"):
                spriteName = None
                #spriteName = "%s-%s-%s-%d" % (spriteRoot, "unisex", "standing", 1)
            self.cache[equipmentName].setSprites({'standing': [spriteName]})

        return self.cache[equipmentName]


class MusicLoader(object):
    def __call__(self, musicName, loop=True):
        if musicName == None or musicName == '':
            return
        musicFile = _getFilename("music", musicName + ".ogg")
        if musicFile == None:
            return
        try:
            pygame.mixer.music.load(musicFile)
            pygame.mixer.music.set_volume(0.4)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play(0)
        except pygame.error as e:
            return


class TextLoader(object):
    def __call__(self, textName):
        filename = textName + ".txt"
        textFile = _getFilename("text", filename)
        if textFile == None:
            raise Exception('Text file "%s" not found' % filename)
        with open(textFile, "r") as f:
            text = f.readlines()
        return text


class SoundLoader(object):
    def __init__(self):
        self.cache = {}

    def __call__(self, soundName):
        if soundName == None:
            return None
        if soundName not in self.cache:
            soundFile = _getFilename("sounds", soundName + ".ogg")
            if soundFile == None:
                soundFile = _getFilename("sounds", soundName + ".wav")
            try:
                s = pygame.mixer.Sound(soundFile)
            except pygame.error as e:
                return None
            self.cache[soundName] = s
        return self.cache[soundName]


class SpriteConfigLoader(object):
    def __init__(self):
        self._hand = {}
        self._grip = {}
        spriteConfigFilename = _getFilename("images", "spriteconfig.py")
        if spriteConfigFilename != None:
            with open(spriteConfigFilename, "r", newline=None) as spriteConfigFile:
                spriteConfigText = spriteConfigFile.read()

            localVars = {}

            compiled = compile(spriteConfigText, spriteConfigFilename, 'exec')
            eval(compiled, localVars)

            self._hand = {}
            self._grip = {}
            self._spriteTypes = None

            if 'HAND' in localVars:
                self._hand = localVars['HAND']
            if 'GRIP' in localVars:
                self._grip = localVars['GRIP']
            if 'SPRITE_TYPES' in localVars:
                self._spriteTypes = localVars['SPRITE_TYPES']

    def spriteTypes(self):
        return self._spriteTypes

    def hand(self, sprite):
        if sprite in self._hand:
            return self._hand[sprite]
        else:
            return None

    def grip(self, sprite):
        if sprite in self._grip:
            return self._grip[sprite]
        else:
            return None


def setCampaign(c):
    global campaign, font, map, image, texture, scenario, class_, ability, weapon, spriteConfig
    logger.debug('Set campaign to "%s"' % c)
    campaign = c
    # Clear filename cache when campaign changes
    _filename_cache.clear()
    font = FontLoader()
    map = MapLoader()
    image = ImageLoader()
    texture = TextureLoader()
    scenario = ScenarioLoader()
    class_ = ClassLoader()
    ability = AbilityLoader()
    music = MusicLoader()
    text = TextLoader()
    unit = UnitLoader()
    sound = SoundLoader()
    equipment = EquipmentLoader()
    spriteConfig = SpriteConfigLoader()


campaign = 'demo'
font = FontLoader()
map = MapLoader()
image = ImageLoader()
texture = TextureLoader()
scenario = ScenarioLoader()
class_ = ClassLoader()
ability = AbilityLoader()
music = MusicLoader()
text = TextLoader()
unit = UnitLoader()
sound = SoundLoader()
equipment = EquipmentLoader()
spriteConfig = SpriteConfigLoader()
