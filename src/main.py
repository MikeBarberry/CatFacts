import os, io
from threading import Event, Thread

import pygame

from utils import init_custom_events, fetch_cat_data
from pygame_helper import PygHelper
from cat_events import CatEventEmitter

pyg_helper = PygHelper(pygame)

# Declare thread that will post to
# pygame event loop.
emitter = CatEventEmitter(Event())
# Pass it to data-fetching thread as
# an argument, and run both in the
# background.
fetch_data = Thread(
    target=fetch_cat_data,
    args=[emitter],
    daemon=True,
)


class CatFacts:
    def __init__(self):
        self.running = True
        self.custom_events = init_custom_events()
        self.helper = pyg_helper
        # Set loading screen.
        self.post_event("loading")
        # Give event emitter thread function
        # to post to this main loop.
        emitter.post_to_pygame = self.post_event
        # Start fetching data.
        fetch_data.start()

    def post_event(self, event_name, data={}):
        event_id = self.custom_events[event_name]
        event = pygame.event.Event(event_id, {"data": data})
        pygame.event.post(event)

    def loading_image(self):
        root_dir = os.path.abspath(".")
        image_path = os.path.join(root_dir, "images", "inked_loading_cat.jpg")

        with open(image_path, "rb") as image:
            self.helper.show_loading(io.BytesIO(image.read()))

    def main(self):
        print("\n \U0001F389 Welcome to the show! Let's get this party started... \n")
        while self.running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.running = False
                # Kill daemon thread.
                emitter.stopped.set()
            elif event.type == self.custom_events["loading"]:
                self.loading_image()
            elif event.type == self.custom_events["show_cat"]:
                self.helper.show_cat(*event.__dict__["data"].values())
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    try:
        program.main()
    except KeyboardInterrupt:
        # Kill daemon thread.
        emitter.stopped.set()
        exit(0)
