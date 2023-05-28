import pygame
import os
import urllib.request
import json
import os
import io

EMOJI_PATH = os.path.join(os.path.abspath("."), "fonts", "NotoEmoji-Medium.ttf")


def init_custom_events():
    return {
        "loading": pygame.event.custom_type(),
        "show_cat": pygame.event.custom_type(),
    }


def init_fonts():
    return {
        "small": pygame.font.SysFont("segoeuisymbol", 20),
        "med": pygame.font.SysFont("segoeuisymbol", 25),
        "emoji": pygame.font.Font(EMOJI_PATH, 30),
    }


def init_pygame_screen():
    pygame.init()

    screen = pygame.display.set_mode(
        (pygame.display.Info().current_w - 100, pygame.display.Info().current_h - 100),
        pygame.RESIZABLE,
        pygame.SCALED,
    )

    return screen


def fetch_cat_data(add_cat_to_list, report_cats_count, start_posting_cat_events):
    req = urllib.request.Request(
        "https://api.thecatapi.com/v1/breeds",
        headers={"x-api-key": os.getenv("API_KEY")},
    )

    res = urllib.request.urlopen(req)

    json_res = json.loads(res.read().decode("utf-8"))

    count_cats = 0
    for ele in json_res:
        if not "image" in ele:
            continue
        count_cats += 1

        imageContent = fetch_cat_image(ele["image"]["url"])

        cat = {
            "breed": ele["name"],
            "details": ele["description"],
            "origin": ele["origin"],
            "image": imageContent,
        }

        add_cat_to_list(cat)

        if count_cats == 1:
            start_posting_cat_events()

    report_cats_count(count_cats)


def fetch_cat_image(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    image_content = urllib.request.urlopen(req)

    image_bytes = io.BytesIO(image_content.read())

    return image_bytes
