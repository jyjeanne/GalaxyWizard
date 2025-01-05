import os
import logging
import optparse
import pygame
from translate import Translate
import numpy as np

__version__ = "0.1.0"

def main():
    print('Start GalaxyWizard', __version__)

    # init translate
    translate_config = Translate()

    # init game config
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

    logging.basicConfig(level=logging.DEBUG - options.verbose * 10)

    translate_config.setLanguage(options.lang)

    # init pygame config
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
    import sound
    import twistedmain

    resources.texture.setTextureSize(64)
    # TODO finish to convert
    sound.setQuiet(options.quiet)


    # TODO finish to convert
    twistedmain.run(options)


if __name__ == "__main__":
    main()
