import pygame
import os
import urllib.request
import json as pyjs
from io import BytesIO
import time


class CatFacts:
    def __init__(self):
        pygame.init()
        self.getBreedInfo()
        self.displayInfo = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (self.displayInfo.current_w, self.displayInfo.current_h), pygame.RESIZABLE
        )
        self.sysFont = pygame.font.SysFont("segoeuisymbol", 20)
        self.font = pygame.font.Font("./NotoEmoji-Medium.ttf", 20)

    def getBreedInfo(self):
        req = urllib.request.Request("https://api.thecatapi.com/v1/breeds")
        req.add_header("x-api-key", os.getenv("API_KEY"))
        res = urllib.request.urlopen(req)
        json = pyjs.loads(res.read().decode("utf-8"))
        self.breedInfo = {breed["name"]: breed for breed in json}
        self.buildImagesDict()

    def buildImagesDict(self):
        images = {}
        for key, value in self.breedInfo.items():
            if "image" in value:
                images[key] = value["image"]["url"]
        self.images = images

    def showPic(self, name, image, origin, description):
        pygame.display.set_caption(name)
        req = urllib.request.Request(image, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req)
        surface = pygame.image.load(BytesIO(res.read())).convert()
        picture = pygame.transform.scale(surface, surface.get_rect().center)
        self.screen.fill((0, 0, 0))
        self.screen.blit(picture, (0, 0))
        self.writeInfo(origin, description)
        pygame.display.flip()

    def writeInfo(self, origin, description):
        startingX = 20
        startingY = 20
        globe = self.font.render("\U0001F431", True, (255, 165, 0))
        _, _, globeWidth, globeHeight = globe.get_rect()
        originT = self.sysFont.render(origin, True, (255, 165, 0))
        _, _, textWidth, _ = originT.get_rect()
        descriptionT = self.sysFont.render(description, True, (255, 165, 0))
        self.screen.blits(
            [
                (globe, (startingX, startingY)),
                (originT, (startingX + globeWidth, startingY)),
                (globe, (startingX + globeWidth + textWidth, startingY)),
                (descriptionT, (startingX, startingY + globeHeight)),
            ]
        )

    def showAllPics(self):
        print(
            "\n \U0001F389 Welcome to the slideshow! Let's get this party started... \n"
        )
        time.sleep(3)
        for key, value in self.images.items():
            origin = self.breedInfo[key]["origin"]
            description = self.breedInfo[key]["description"]
            breedLog = f"\U0001F431 {key} \U0001F431"
            originLog = f"\U0001F30E {origin} \U0001F30F:"
            descriptionLog = f"{self.breedInfo[key]['description']}\n"
            self.showPic(key, value, origin, description)
            print(" ".join([breedLog, originLog, descriptionLog]))
            time.sleep(10)


cf = CatFacts()
cf.showAllPics()
