from os import path
from threading import Event
from io import BytesIO
from cf_scheduler import CFScheduler
from cf_utils import CFUtils
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

STOP_FLAG = Event()
INITIAL_X = 20
INITIAL_Y = 20
CAT_EMOJI = "\U0001F431"
GLOBE_EMOJI_NA = "\U0001F30E"
GLOBE_EMOJI_AS = "\U0001F30F"
HOURGLASS_EMOJI = "\U000023F3"
EMOJI_COLOR = (255, 165, 0)
ORIGIN_COLOR = (137, 207, 240)
DESCRIPTION_COLOR = (65, 65, 65)
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
        self.utils = CFUtils(INITIAL_X, INITIAL_Y)
        # post fetch event to the loop
        self.utils.fetch(pygEvent, self.eventIds["fetch"])
        self.fonts = {
            "small": font.SysFont("segoeuisymbol", 20),
            "med": font.SysFont("segoeuisymbol", 25),
            "emoji": font.Font(EMOJI_PATH, 30),
        }
        self.screen = display.set_mode(
            self.utils.size(display),
            RESIZABLE,
            SCALED,
        )

    def origin(self, origin):
        screenContent = [
            (self.fonts["emoji"], CAT_EMOJI, EMOJI_COLOR),
            (self.fonts["med"], origin, ORIGIN_COLOR),
            (self.fonts["emoji"], CAT_EMOJI, EMOJI_COLOR),
        ]
        rendered = self.utils.renderList(screenContent)
        self.utils.blit(self.screen, {"type": "origin", "content": rendered})

    def details(self, details):
        brokenLines = self.utils.breakLine(self.fonts["small"], details)
        screenContent = [
            (self.fonts["small"], x, DESCRIPTION_COLOR) for x in brokenLines
        ]
        rendered = self.utils.renderList(screenContent)
        self.utils.blit(self.screen, {"type": "details", "content": rendered})

    def image(self, image):
        transformed = self.utils.transformImage(pygImage, transform, image, display)
        self.utils.blit(
            self.screen, {"type": "image", "content": [transformed, (0, 0)]}
        )

    def showCat(self, breed, details, origin, image):
        display.set_caption(breed)
        self.image(image)
        self.origin(origin)
        self.details(details)
        display.flip()
        self.utils.log(
            breed, details, origin, CAT_EMOJI, GLOBE_EMOJI_NA, GLOBE_EMOJI_AS
        )

    def loading(self, image):
        display.set_caption("Loading...")
        self.image(image)
        display.flip()
        print(f"Loading data {HOURGLASS_EMOJI}")

    def spawn(self, cats):
        child = CFScheduler(STOP_FLAG, cats, self.eventIds["cat"], pygEvent)
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
                # load and show loading image
                with open(LOADING_PATH, "rb") as image:
                    self.loading(BytesIO(image.read()))
                """
                invoke fetch
                when it returns, spawn
                daemon process to invoke
                cat events without blocking
                main thread
                """
                fetch = event.__dict__["callback"]
                cats = fetch()
                self.spawn(cats)
            elif event.type == catId:
                self.showCat(*event.__dict__["data"].values())
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    program.main()
