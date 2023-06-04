import os
from threading import Event, Thread
import io
import pygame
from cat_events import CatEventEmitter
from pygame_helper import PygHelper
from utils import init_custom_events, fetch_cat_data

pyg_helper = PygHelper(
    pygame.display,
    pygame.image,
    pygame.transform,
)
# fetch and post data in sub threads
# to allow main thread to be
# exited at any time
emitter = CatEventEmitter(Event())
fetch_data = Thread(
    target=fetch_cat_data,
    args=[emitter],
    daemon=True,
)


class CatFacts:
    def __init__(self):
        pygame.init()
        self.running = True
        self.custom_events = init_custom_events()
        self.helper = pyg_helper
        self.post_event("loading")
        emitter.post_to_pygame = self.post_event
        fetch_data.start()

    def post_event(self, event_name, data={}):
        event_id = self.custom_events[event_name]
        event = pygame.event.Event(event_id, {"data": data})
        pygame.event.post(event)

    def show_loading_image(self):
        root_dir = os.path.abspath(".")
        loading_image_path = os.path.join(root_dir, "images", "inked_loading_cat.jpg")

        with open(loading_image_path, "rb") as image:
            image_bytes = io.BytesIO(image.read())
            self.helper.show_loading(image_bytes)

    def main(self):
        print("\n \U0001F389 Welcome to the show! Let's get this party started... \n")
        while self.running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.running = False
                emitter.stopped.set()
            elif event.type == self.custom_events["loading"]:
                self.show_loading_image()
            elif event.type == self.custom_events["show_cat"]:
                self.helper.show_cat(*event.__dict__["data"].values())
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    try:
        program.main()
    except KeyboardInterrupt:
        emitter.stopped.set()
        exit(0)
