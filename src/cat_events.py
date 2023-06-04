from threading import Thread


class CatEventEmitter(Thread):
    def __init__(self, event_signal):
        Thread.__init__(self)
        # Event.wait returns False when not set
        self.stopped = event_signal
        self.waiting = True
        self.finished_fetching = False
        self.post_to_pygame = None
        self.current_cat = 0
        self.cats_list = []

    def post_cat(self):
        if self.current_cat >= len(self.cats_list):
            self.waiting = True
            return

        if self.finished_fetching and self.current_cat >= len(self.cats_list):
            self.current_cat = 0

        self.post_to_pygame("show_cat", self.cats_list[self.current_cat])

        self.current_cat += 1

    def run(self):
        # Threads automatically call run
        # and exit when it returns
        while not self.stopped.is_set():
            # show first cat as soon as data is ready
            if self.waiting:
                # break this loop if self.waiting is False
                while self.waiting and not self.stopped.wait(0.1):
                    if self.current_cat < len(self.cats_list):
                        self.post_cat()
                        self.waiting = False
            # wait 10 seconds between consecutive posts
            else:
                # break this loop if self.waiting is True
                while not self.waiting and not self.stopped.wait(10.0):
                    self.post_cat()
