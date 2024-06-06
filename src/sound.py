import resources
import pygame

_quiet = False
_mixerInit = pygame.mixer.get_init() is not None

if _mixerInit:
    _cursorChannel = pygame.mixer.Channel(0)
    _actionChannel = pygame.mixer.Channel(1)
else:
    _quiet = True
    _cursorChannel = None
    _actionChannel = None


def _play(channel, sound):
    if not _mixerInit:
        return
    if not _quiet and sound is not None:
        channel.play(sound)


def setQuiet(quiet):
    global _quiet

    if not _mixerInit:
        return

    _quiet = quiet

    if _quiet:
        pygame.mixer.pause()
        pygame.mixer.music.pause()
    else:
        pygame.mixer.unpause()
        pygame.mixer.music.unpause()


def toggleQuiet():
    setQuiet(not _quiet)


def playMusic(musicName):
    """Changes background music."""
    if not _mixerInit:
        return
    if not _quiet:
        resources.music(musicName)


def playTune(tuneName):
    """Plays a short tune. Returns whether it was actually played."""
    if _mixerInit and not _quiet:
        resources.music(tuneName, loop=False)
        return True
    else:
        return False


def cursorClick():
    s = resources.sound("cursor-click")
    _play(_cursorChannel, s)


def cursorCancel():
    s = resources.sound("cursor-cancel")
    _play(_cursorChannel, s)


def cursorMove():
    s = resources.sound("cursor-move")
    _play(_cursorChannel, s)


def cursorInvalid():
    s = resources.sound("cursor-invalid")
    _play(_cursorChannel, s)


def action(sound):
    s = resources.sound(sound)
    _play(_actionChannel, s)
