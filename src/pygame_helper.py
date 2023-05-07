CAT_EMOJI = "\U0001F431"
GLOBE_EMOJI_NA = "\U0001F30E"
GLOBE_EMOJI_AS = "\U0001F30F"
HOURGLASS_EMOJI = "\U000023F3"
EMOJI_COLOR = (255, 165, 0)
ORIGIN_COLOR = (137, 207, 240)
DESCRIPTION_COLOR = (65, 65, 65)


class PygHelper:
    def __init__(
        self, x, y, screen, display, pygImage, transform, smallFont, medFont, emojiFont
    ):
        self.screen = screen
        self.display = display
        self.pygImage = pygImage
        self.transform = transform
        self.initial_x = x
        self.initial_y = y
        self.X = x
        self.Y = y
        self.emojiFont = emojiFont
        self.smallFont = smallFont
        self.medFont = medFont

    def show_origin(self, origin):
        screenContent = [
            (self.emojiFont, CAT_EMOJI, EMOJI_COLOR),
            (self.medFont, origin, ORIGIN_COLOR),
            (self.emojiFont, CAT_EMOJI, EMOJI_COLOR),
        ]
        self.render_and_blit(screenContent, "origin")

    def show_details(self, details):
        brokenLines = self.break_line(self.smallFont, details)
        screenContent = [(self.smallFont, x, DESCRIPTION_COLOR) for x in brokenLines]
        self.render_and_blit(screenContent, "details")

    def show_image(self, image):
        transformed = self.transform_image(image)
        self.blit({"type": "image", "content": [transformed, (0, 0)]})

    def show_cat(self, breed, details, origin, image):
        self.display.set_caption(breed)
        self.show_image(image)
        self.show_origin(origin)
        self.show_details(details)
        self.display.flip()
        self.console_log(breed, details, origin)

    def show_loading(self, image):
        self.display.set_caption("Loading...")
        self.show_image(image)
        self.display.flip()
        print(f"Loading data {HOURGLASS_EMOJI}")

    def console_log(self, breed, details, origin):
        print(
            " ".join(
                [
                    f"{CAT_EMOJI} {breed} {CAT_EMOJI}",
                    f"{GLOBE_EMOJI_NA} {origin} {GLOBE_EMOJI_AS}:",
                    f"{details}\n",
                ]
            )
        )

    def break_line(self, font, line):
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

    def transform_image(self, image):
        converted = self.pygImage.load(image).convert()
        dw, dh = self.display.Info().current_w, self.display.Info().current_h
        rw, rh = converted.get_rect().width, converted.get_rect().height
        if rw > dw or rh > dh:
            scaled = self.transform.scale(converted, converted.get_rect().center)
            return scaled
        return converted

    def render_and_blit(self, content, type):
        rendered = self.render_list(content)
        self.blit({"type": type, "content": rendered})

    def render_list(self, list):
        return [self.render(*x) for x in list]

    def render(self, font, text, color):
        return font.render(text, True, color)

    def update_position(self, coord, ele):
        if coord == "X":
            return self.X + ele.get_width() + 5
        return self.Y + ele.get_height() + 5

    """
    each image starts from initial coords
    increase curr X after each origin ele
    also increase Y after last origin ele
    increase Y after each details ele
    reset Y after details but not origin
    since details will come next
    if type is other just blit content
    """

    def blit(self, request):
        content = request["content"]
        section = request["type"]
        if section == "origin" or section == "details":
            for idx in range(len(content)):
                ele = content[idx]
                self.screen.blit(ele, (self.X, self.Y))
                if section == "origin":
                    self.X = self.update_position("X", ele)
                if section == "details" or idx == len(content) - 1:
                    self.Y = self.update_position("Y", ele)
            self.X = self.initial_x
            self.Y = self.Y if section == "origin" else self.initial_y
        else:
            self.screen.blit(*content)
