import time
from cf_utils import CFUtils
from io import BytesIO
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


INITIAL_X = 20
INITIAL_Y = 20
CAT_EMOJI = "\U0001F431"
GLOBE_EMOJI_NA = "\U0001F30E"
GLOBE_EMOJI_AS = "\U0001F30F"
EMOJI_COLOR = (255, 165, 0)
ORIGIN_COLOR = (137, 207, 240)
DESCRIPTION_COLOR = (65, 65, 65)


class CatFacts:
    def __init__(self):
        init()
        self.running = True
        self.eventIds = {
            "fetch": pygEvent.custom_type(),
            "cat": pygEvent.custom_type(),
            "wait": pygEvent.custom_type(),
        }
        self.utils = CFUtils(INITIAL_X, INITIAL_Y)
        self.utils.fetch(pygEvent, self.eventIds["fetch"])
        self.fonts = {
            "small": font.SysFont("segoeuisymbol", 20),
            "med": font.SysFont("segoeuisymbol", 25),
            "emoji": font.Font("../fonts/NotoEmoji-Medium.ttf", 30),
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
        print("Loading data.")

    def main(self):
        print("\n \U0001F389 Welcome to the show! Let's get this party started... \n")
        fetchId, catId, waitId = self.eventIds.values()
        while self.running and pygEvent.peek(fetchId) or pygEvent.peek(catId):
            for event in pygEvent.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == fetchId:
                    with open("../images/inked_loading_cat.jpg", "rb") as image:
                        self.loading(BytesIO(image.read()))
                    fetchCats = event.__dict__["callback"]
                    fetchCats(catId, waitId, pygEvent)
                elif event.type == catId:
                    self.showCat(*event.__dict__.values())
                elif event.type == waitId:
                    time.sleep(10)
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    program = CatFacts()
    program.main()
