from os import path
from threading import Event
from io import BytesIO
from collections import deque
from pygame import (
    event as pygEvent,
    font,
    init,
    display,
    image as pygImage,
    transform,
    RESIZABLE,
    SCALED,
    QUIT,
)

from cat_events import CatEventEmitter
from pygame_helper import PygHelper

INITIAL_X = 20
INITIAL_Y = 20
EMOJI_PATH = path.join(path.abspath("."), "fonts", "NotoEmoji-Medium.ttf")
LOADING_PATH = path.join(path.abspath("."), "images", "inked_loading_cat.jpg")


class CatFacts:
    def __init__(self):
        init()
        self.running = True
        self.eventIds = self.init_custom_events()
        self.fonts = self.init_fonts()
        self.screen = self.init_screen()
        self.helper = self.init_pygame_helper()
        self.child = self.init_child_thread()
        self.post_event("load")

    def init_custom_events(self):
        return {
            "load": pygEvent.custom_type(),
            "fetch": pygEvent.custom_type(),
            "cat": pygEvent.custom_type(),
        }

    def init_fonts(self):
        return {
            "small": font.SysFont("segoeuisymbol", 20),
            "med": font.SysFont("segoeuisymbol", 25),
            "emoji": font.Font(EMOJI_PATH, 30),
        }

    def init_child_thread(self):
        event = Event()
        child = CatEventEmitter(event, deque(), self.eventIds["cat"], pygEvent)
        child.daemon = True
        child.start()
        return child

    def init_screen(self):
        screen = display.set_mode(
            (display.Info().current_w - 100, display.Info().current_h - 100),
            RESIZABLE,
            SCALED,
        )
        return screen

    def init_pygame_helper(self):
        helper = PygHelper(
            INITIAL_X,
            INITIAL_Y,
            self.screen,
            display,
            pygImage,
            transform,
            *self.fonts.values()
        )
        return helper

    def post_event(self, e):
        event = pygEvent.Event(self.eventIds[e])
        pygEvent.post(event)

    def show_loading_image(self):
        with open(LOADING_PATH, "rb") as image:
            self.helper.show_loading(BytesIO(image.read()))

    def main(self):
        print("\n \U0001F389 Welcome to the show! Let's get this party started... \n")
        loadId, fetchId, catId = self.eventIds.values()
        while self.running:
            event = pygEvent.wait()
            if event.type == QUIT:
                self.running = False
            elif event.type == loadId:
                self.show_loading_image()
                self.post_event("fetch")
            elif event.type == fetchId:
                self.child.fetch_cats()
            elif event.type == catId:
                self.helper.show_cat(*event.__dict__["data"][0].values())
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    program.main()
