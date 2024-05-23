import os
import sys
import logging
import platform
import optparse
import numpy as np

__version__ = "0.1.0"


def dependencycheck():
    logging.debug('Platform: ' + platform.platform())
    logging.debug('Python version ' + sys.version)
    try:
        logging.debug('Numpy version ' + np.__version__)
    except ImportError as err:
        logging.error('Loading dependency "Numpy" failed: ' + str(err))
        sys.exit(1)

    try:
        import pygame
        logging.debug('pygame version ' + pygame.ver)
    except ImportError as err:
        logging.error('Loading dependency "pygame" failed: ' + str(err))
        sys.exit(1)

    try:
        import OpenGL.GL
        logging.debug('PyOpenGL version ' + OpenGL.__version__)
    except ImportError as err:
        logging.error('Loading dependency "OpenGL.GL" failed: ' + str(err))
        sys.exit(1)

    try:
        import OpenGL.GLU
    except ImportError as err:
        logging.error('Loading dependency "OpenGL.GLU" failed: ' + str(err))
        sys.exit(1)

    try:
        import twisted
        logging.debug('Twisted version ' + twisted.__version__)
    except ImportError as err:
        logging.error('Loading dependency "twisted" failed: ' + str(err))
        sys.exit(1)


def main():
    print('GalaxyWizard', __version__)

    # init translate
    from translate import Translate
    translateConfig = Translate()

    parser = optparse.OptionParser(description="Cross-platform, open-source tactical RPG.")
    parser.add_option("--fullscreen", "-f", action="store_true", default=False)
    parser.add_option("--quiet", "-q", action="store_true", default=False)
    parser.add_option("--verbose", "-v", action="count", default=0)
    parser.add_option("-w", dest="width", type=int, default=800, metavar="WIDTH")
    parser.add_option("--edit-map", "-e", action="store", default=None, metavar="MAPNAME")
    parser.add_option("--port", "-P", type=int, default=22222)
    parser.add_option("--lang", "-l", default="en")
    parser.add_option("--user", default=os.environ.get('USER', 'Player'))
    (options, args) = parser.parse_args()

    logging.basicConfig(level=logging.INFO - options.verbose * 10)

    translateConfig.setLanguage(options.lang)

    dependencycheck()

    import pygame
    pygame.display.init()
    pygame.font.init()
    pygame.joystick.init()

    try:
        pygame.mixer.init(48000, -16, True, 4096)
    except pygame.error as e:
        options.quiet = True
        logging.warning("Couldn't initialize sound: " + str(e))

    import resources
    # TODO finish to convert
    # import Sound
    # import twistedmain

    resources.texture.setTextureSize(64)
    # TODO finish to convert
    # Sound.setQuiet(options.quiet)


# TODO finish to convert
# twistedmain.run(options)


if __name__ == "__main__":
    main()
