import os
from threading import Event, Thread
import io
import pygame

from cat_events import CatEventEmitter
from pygame_helper import PygHelper

from utils import init_custom_events, fetch_cat_data

custom_events = init_custom_events()

pyg_helper = PygHelper(
    pygame.display,
    pygame.image,
    pygame.transform,
)

event_signal = Event()
cat_event_emitter = CatEventEmitter(event_signal)

fetch = Thread(
    target=fetch_cat_data,
    args=[
        cat_event_emitter.add_cat,
        cat_event_emitter.set_total_count,
        cat_event_emitter.start_thread,
    ],
    daemon=True,
)
fetch.start()


class CatFacts:
    def __init__(self):
        pygame.init()
        self.running = True
        self.custom_events = init_custom_events()
        self.helper = pyg_helper
        self.post_event("loading")
        cat_event_emitter.set_post_function(self.post_event)

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
        loading, show_cat = self.custom_events.values()
        while self.running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.running = False
                cat_event_emitter.kill_thread()
            elif event.type == loading:
                self.show_loading_image()
            elif event.type == show_cat:
                breed, details, origin, image = event.__dict__["data"].values()
                self.helper.show_cat(breed, details, origin, image)
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    program.main()
