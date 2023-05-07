import os
from collections import deque
from io import BytesIO
from json import loads
from operator import itemgetter
from urllib.request import Request, urlopen


class CFUtils:
    def __init__(self, x, y):
        self.initial_x = x
        self.initial_y = y
        self.X = x
        self.Y = y

    def size(self, display):
        return (display.Info().current_w, display.Info().current_h)

    def fetch(self, pygEvent, fetchId):
        fetchEvent = pygEvent.Event(fetchId, {"callback": self.cats})
        pygEvent.post(fetchEvent)

    def cats(self):
        req = Request("https://api.thecatapi.com/v1/breeds")
        req.add_header("x-api-key", os.getenv("API_KEY"))
        res = urlopen(req)
        json = loads(res.read().decode("utf-8"))
        q = deque()
        for ele in json:
            if not "image" in ele:
                continue
            image, name, details, origin = itemgetter(
                "image", "name", "description", "origin"
            )(ele)
            imageContent = self.image(image["url"])
            q.append(
                {
                    "breed": name,
                    "details": details,
                    "origin": origin,
                    "image": BytesIO(imageContent.read()),
                },
            )
        return q

    def image(self, url):
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urlopen(req)
        return res

    def log(self, breed, details, origin, catEmoji, globeNA, globeAS):
        print(
            " ".join(
                [
                    f"{catEmoji} {breed} {catEmoji}",
                    f"{globeNA} {origin} {globeAS}:",
                    f"{details}\n",
                ]
            )
        )

    def breakLine(self, font, line):
        currentLine = ""
        brokenLines = []
        for ele in line.split():
            if font.size(currentLine + ele)[0] < 400:
                currentLine += f"{ele} "
            else:
                brokenLines.append(currentLine)
                currentLine = f"{ele} "
        brokenLines.append(currentLine)
        return brokenLines

    def transformImage(self, pygImage, transform, image, display):
        converted = pygImage.load(image).convert()
        dw, dh = display.Info().current_w, display.Info().current_h
        rw, rh = converted.get_rect().width, converted.get_rect().height
        if rw > dw or rh > dh:
            scaled = transform.scale(converted, converted.get_rect().center)
            return scaled
        return converted

    def renderList(self, list):
        return [self.render(*x) for x in list]

    def render(self, font, text, color):
        return font.render(text, True, color)

    def position(self, coord, ele):
        if coord == "X":
            return self.X + ele.get_width() + 5
        return self.Y + ele.get_height() + 5

    """
    screen is reset after each image
    always start at same X
    increase X for each origin element
    last origin also increase Y since
    details will come next
    increase Y for each element of details
    reset Y after last detail
    """

    def blit(self, screen, request):
        content = request["content"]
        section = request["type"]
        if section == "origin" or section == "details":
            for idx in range(len(content)):
                ele = content[idx]
                screen.blit(ele, (self.X, self.Y))
                if section == "origin":
                    self.X = self.position("X", ele)
                if section == "details" or idx == len(content) - 1:
                    self.Y = self.position("Y", ele)
            self.X = self.initial_x
            self.Y = self.Y if section == "origin" else self.initial_y
        else:
            screen.blit(*content)
