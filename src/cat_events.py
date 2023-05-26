from threading import Thread
from json import loads
from operator import itemgetter
from urllib.request import Request, urlopen
from os import getenv
from io import BytesIO


class CatEventEmitter(Thread):
    def __init__(self, event, cats, cats_id, event_loop):
        Thread.__init__(self)
        self.started = False
        self.event = event
        self.cats = cats
        self.cats_id = cats_id
        self.event_loop = event_loop

    def fetch_cats(self):
        req = Request("https://api.thecatapi.com/v1/breeds")
        req.add_header("x-api-key", getenv("API_KEY"))
        res = urlopen(req)
        json = loads(res.read().decode("utf-8"))
        for ele in json:
            if not "image" in ele:
                continue
            image, name, details, origin = itemgetter(
                "image", "name", "description", "origin"
            )(ele)
            imageContent = self.fetch_image(image["url"])
            cat = (
                {
                    "breed": name,
                    "details": details,
                    "origin": origin,
                    "image": BytesIO(imageContent.read()),
                },
            )
            self.add_cat(cat)

    def fetch_image(self, url):
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urlopen(req)
        return res

    def kill_thread(self):
        self.stopped.set()

    def add_cat(self, cat):
        self.cats.append(cat)

    def immediately_show_first_cat(self):
        if len(self.cats) == 0:
            self.run()
        else:
            self.started = True
            self.main()
            self.run()

    def main(self):
        cat = self.cats.popleft()
        event = self.event_loop.Event(self.cats_id, {"data": cat})
        self.event_loop.post(event)

    def run(self):
        if not self.started:
            while not self.event.wait(1):
                self.immediately_show_first_cat()
        else:
            while not self.event.wait(10.0):
                self.main()
