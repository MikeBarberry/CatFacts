import pygame
import os
import urllib.request
import json as pyjs
from io import BytesIO
import time

pygame.init()
displayInfo = pygame.display.Info()
screen = pygame.display.set_mode(
    (displayInfo.current_w, displayInfo.current_h), pygame.RESIZABLE
)


class CatFacts:
    def __init__(self):
        self.getBreedInfo()

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

    def showPic(self, name, image):
        pygame.display.set_caption(name)
        req = urllib.request.Request(image, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req)
        surface = pygame.image.load(BytesIO(res.read())).convert()
        picture = pygame.transform.scale(surface, surface.get_rect().center)
        screen.blit(picture, (0, 0))
        pygame.display.flip()

    def showAllPics(self):
        print(
            "\n \U0001F389 Welcome to the slideshow! Let's get this party started... \n"
        )
        time.sleep(3)
        for key, value in self.images.items():
            self.showPic(key, value)
            breed = f"\U0001F431 {key} \U0001F431"
            origin = f"\U0001F30E {self.breedInfo[key]['origin']} \U0001F30F:"
            description = f"{self.breedInfo[key]['description']}\n"
            print(" ".join([breed, origin, description]))
            time.sleep(10)


cf = CatFacts()
cf.showAllPics()
