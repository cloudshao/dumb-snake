import curses
import sys
import traceback
import logging
from renderer import Renderer
from gameloop import GameLoop

def onexception(exctype, value, tb):
    traceback.print_exception(exctype, value, tb)


def main(window):
    sys.excepthook = onexception
    logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    renderer = Renderer()
    gameloop = GameLoop(renderer)
    gameloop.start()


if __name__ == "__main__":
    curses.wrapper(main)

