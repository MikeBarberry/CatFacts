import os
import time
from pygame import font, init, display, mixer, image, transform, RESIZABLE
from io import BytesIO
from json import loads
from operator import itemgetter
from threading import Thread, Event
from urllib.request import Request, urlopen


class CatFacts(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.event = event
        self.catEmoji = "\U0001F431"
        self.audoFile = "./appandbanan.mp3"

    def killThread(self):
        self.event.set()

    def fetchCatFacts(self):
        req = Request("https://api.thecatapi.com/v1/breeds")
        req.add_header("x-api-key", os.getenv("API_KEY"))
        res = urlopen(req)
        json = loads(res.read().decode("utf-8"))
        pertinentFacts = []
        for ele in json:
            if not "image" in ele:
                continue
            image, name, description, origin = itemgetter(
                "image", "name", "description", "origin"
            )(ele)
            imgB = self.fetchCatImg(image["url"])
            pertinentFacts.append(
                {
                    "breed": name,
                    "description": description,
                    "origin": origin,
                    "image": {
                        "b": imgB,
                    },
                }
            )
        self.catFacts = pertinentFacts
        return

    def fetchCatImg(self, url):
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urlopen(req)
        imgB = BytesIO(res.read())
        return imgB

    def flipDisplay(self, breed, desc, origin, img):
        imgB = img["b"]
        self.display.set_caption(breed)
        imgSurf = image.load(imgB).convert()
        imgSurfT = transform.scale(imgSurf, imgSurf.get_rect().center)
        self.screen.fill((0, 0, 0))
        self.screen.blit(imgSurfT, (0, 0))
        self.prepareTextBlit(origin, desc)
        self.display.flip()

    def prepareTextBlit(self, origin, desc):
        emojiSurf = self.emojiFont.render(self.catEmoji, True, (251, 206, 177))
        originSurf = self.textFont.render(origin, True, (137, 207, 240))
        self.blitText(emojiSurf, originSurf, desc)

    def blitText(self, emoji, origin, desc):
        startX, startY = 20, 20
        *_, emojiW, emojiH = emoji.get_rect()
        *_, originW, _ = origin.get_rect()
        self.screen.blits(
            [
                (emoji, (startX, startY)),
                (origin, (startX + emojiW, startY)),
                (emoji, (startX + emojiW + originW, startY)),
            ]
        )
        self.utilBreakLines(desc, sum([emojiH + startY]))

    def utilBreakLines(self, desc, prevH):
        lines = []
        line = ""
        for word in desc.split():
            if self.textFont.size(line + word)[0] < 400:
                line += f"{word} "
            else:
                lines.append(line)
                line = f"{word} "
        lines.append(line)
        self.utilBlitLines(lines, prevH)

    def utilBlitLines(self, lines, prevH):
        currH = prevH + 5
        for line in lines:
            lineToRender = self.textFont.render(line, True, (255, 165, 0))
            self.screen.blit(lineToRender, (20, currH))
            currH += sum([lineToRender.get_height(), 5])

    def logToConsole(self, breed, desc, origin, _):
        breedLog = f"\U0001F431 {breed} \U0001F431"
        originLog = f"\U0001F30E {origin} \U0001F30F:"
        descLog = f"{desc}\n"
        print(" ".join([breedLog, originLog, descLog]))

    def initSoundTrack(self):
        mixer.init()
        mixer.music.load(self.audoFile)
        mixer.music.set_volume(0.7)
        mixer.music.play()

    def initPygame(self):
        init()
        self.display = display
        self.screen = self.display.set_mode(
            (display.Info().current_w, display.Info().current_h), RESIZABLE
        )
        self.emojiFont = font.Font("./NotoEmoji-Medium.ttf", 30)
        self.textFont = font.SysFont("segoeuisymbol", 25)

    def main(self):
        while len(self.catFacts):
            fact = [v for (k, v) in self.catFacts.pop(0).items()]
            self.flipDisplay(*fact)
            self.logToConsole(*fact)
            self.event.wait(10)
        print("Bye!")
        self.killThread()

    def run(self):
        self.initPygame()
        self.fetchCatFacts()
        self.main()


try:
    print("Starting program.")
    event = Event()
    catFacts = CatFacts(event)
    catFacts.daemon = True
    catFacts.start()
    while catFacts.event:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    print("Received close signal. Stopping...")
