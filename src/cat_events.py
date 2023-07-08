from threading import Thread

# Main ideas: (1) Don't wait for
# all of the data to load
# to show the first cat,
# show it as soon as its data
# is available and continue
# to fetch the rest in the background.
# (2) Skip the 10 second delay if coming
# out of a wait period.


class CatEventEmitter(Thread):
    def __init__(self, event_signal):
        Thread.__init__(self)
        # event_signal is an Event object
        self.stopped = event_signal
        self.waiting = True
        self.finished_fetching = False
        # This will become the function
        # to post to the pygame
        # event loop after the main thread
        # starts.
        self.post_to_pygame = None
        self.current_cat = 0
        self.cats_list = []

    def post_cat(self):
        # Potentially not enough data to show.
        if self.current_cat >= len(self.cats_list):
            if self.finished_fetching:
                # It's actually just another loop
                # through the cats, reset to the first.
                self.current_cat = 0
            else:
                # The data hasn't loaded yet, go
                # into waiting state.
                self.waiting = True
                return

        self.post_to_pygame("show_cat", self.cats_list[self.current_cat])
        self.current_cat += 1

    def run(self):
        # Using while loop since Python thread
        # objects exit when their run method
        # exits.
        while not self.stopped.is_set():
            # Not enough data to show next in line.
            if self.waiting:
                # Wait 100ms and recheck the list.
                while self.waiting and not self.stopped.wait(0.1):
                    if self.current_cat < len(self.cats_list):
                        # Post right away and break this loop.
                        self.post_cat()
                        self.waiting = False
            # Data is there, pause 10 seconds between posts.
            else:
                while not self.waiting and not self.stopped.wait(1.0):
                    self.post_cat()
