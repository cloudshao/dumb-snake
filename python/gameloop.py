import time

class GameLoop:

    def __init__(self, renderer):
        self.renderer = renderer

    def update(self):
        self.renderer.update()

    def start(self):
        while True:
            try:
                self.update()
            except KeyboardInterrupt:
                break
