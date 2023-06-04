from threading import Thread

# Main idea: only wait for enough
# data to show next cat.
# Load everything else in the
# background.


class CatEventEmitter(Thread):
    def __init__(self, event_signal):
        Thread.__init__(self)
        # self.stopped.wait returns False
        # while event_signal is not set
        self.stopped = event_signal
        self.waiting = True
        self.finished_fetching = False
        self.post_to_pygame = None
        self.current_cat = 0
        self.cats_list = []

    def post_cat(self):
        if self.current_cat >= len(self.cats_list):
            if self.finished_fetching:
                # restart from beginning
                self.current_cat = 0
            else:
                # wait for more data to load
                self.waiting = True
                return

        self.post_to_pygame("show_cat", self.cats_list[self.current_cat])
        self.current_cat += 1

    # Python threads automatically call
    # run method and exit when it returns
    def run(self):
        # loop while thread is alive
        while not self.stopped.is_set():
            if self.waiting:
                # check every 100ms for new data
                # post as soon as it's ready
                # and break this loop
                while self.waiting and not self.stopped.wait(0.1):
                    if self.current_cat < len(self.cats_list):
                        self.post_cat()
                        self.waiting = False
            else:
                # when not waiting for data
                # pause for 10 seconds between consecutive posts
                while not self.waiting and not self.stopped.wait(10.0):
                    self.post_cat()
