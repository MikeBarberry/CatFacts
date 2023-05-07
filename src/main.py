from os import path, getenv
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
from json import loads
from operator import itemgetter
from urllib.request import Request, urlopen

from cat_scheduler import CatScheduler
from pyg_utils import PygUtils


STOP_FLAG = Event()
INITIAL_X = 20
INITIAL_Y = 20
EMOJI_PATH = path.join(path.abspath("."), "fonts", "NotoEmoji-Medium.ttf")
LOADING_PATH = path.join(path.abspath("."), "images", "inked_loading_cat.jpg")


class CatFacts:
    def __init__(self):
        init()
        self.running = True
        self.eventIds = {
            "fetch": pygEvent.custom_type(),
            "cat": pygEvent.custom_type(),
        }
        self.fonts = {
            "small": font.SysFont("segoeuisymbol", 20),
            "med": font.SysFont("segoeuisymbol", 25),
            "emoji": font.Font(EMOJI_PATH, 30),
        }
        self.screen = display.set_mode(
            (display.Info().current_w, display.Info().current_h),
            RESIZABLE,
            SCALED,
        )
        self.pyg_utils = PygUtils(
            INITIAL_X,
            INITIAL_Y,
            self.screen,
            display,
            pygImage,
            transform,
            *self.fonts.values()
        )
        fetch_event = pygEvent.Event(
            self.eventIds["fetch"], {"callback": self.fetch_cats}
        )
        pygEvent.post(fetch_event)

    def fetch_cats(self):
        req = Request("https://api.thecatapi.com/v1/breeds")
        req.add_header("x-api-key", getenv("API_KEY"))
        res = urlopen(req)
        json = loads(res.read().decode("utf-8"))
        q = deque()
        for ele in json:
            if not "image" in ele:
                continue
            image, name, details, origin = itemgetter(
                "image", "name", "description", "origin"
            )(ele)
            imageContent = self.fetch_image(image["url"])
            q.append(
                {
                    "breed": name,
                    "details": details,
                    "origin": origin,
                    "image": BytesIO(imageContent.read()),
                },
            )
        return q

    def fetch_image(self, url):
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urlopen(req)
        return res

    def spawn_child(self, cats):
        child = CatScheduler(STOP_FLAG, cats, self.eventIds["cat"], pygEvent)
        child.daemon = True
        child.start()

    def main(self):
        print("\n \U0001F389 Welcome to the show! Let's get this party started... \n")
        fetchId, catId = self.eventIds.values()
        while self.running:
            event = pygEvent.wait()
            if event.type == QUIT:
                self.running = False
            elif event.type == fetchId:
                with open(LOADING_PATH, "rb") as image:
                    self.pyg_utils.show_loading(BytesIO(image.read()))
                # self.fetch_cats
                callback = event.__dict__["callback"]
                self.spawn_child(callback())
            elif event.type == catId:
                self.pyg_utils.show_cat(*event.__dict__["data"].values())
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    program.main()
