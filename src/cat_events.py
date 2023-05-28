from threading import Thread


class CatEventEmitter(Thread):
    def __init__(self, event_signal):
        Thread.__init__(self)
        self.stopped = event_signal
        self.cats_list = []
        self.current_cat = 0
        self.total_count = 0
        self.waiting = True
        self.post_function = None

    def start_thread(self):
        self.start()

    def kill_thread(self):
        self.stopped.set()

    def set_post_function(self, callback):
        self.post_function = callback

    def set_total_count(self, count):
        self.total_count = count

    def add_cat(self, cat):
        self.cats_list.append(cat)
        print(cat["breed"])

    def can_continue(self):
        can_continue = self.current_cat < len(self.cats_list)
        if can_continue:
            self.waiting = False
        return can_continue

    def update_current_cat(self):
        if self.total_count and self.current_cat == self.total_count - 1:
            self.current_cat = 0
        else:
            self.current_cat += 1

    def post_cat(self):
        if not self.can_continue():
            self.waiting = True
            return

        current_cat_data = self.cats_list[self.current_cat]
        self.post_function("show_cat", current_cat_data)
        self.update_current_cat()

    def run(self):
        while not self.stopped.is_set():
            if self.waiting:
                while self.waiting and not self.stopped.wait(0.5):
                    self.can_continue()
            else:
                while not self.waiting and not self.stopped.wait(10.0):
                    self.post_cat()
