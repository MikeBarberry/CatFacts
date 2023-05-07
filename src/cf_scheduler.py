from threading import Thread


class CFScheduler(Thread):
    def __init__(self, event, cats, catsId, eventLoop):
        Thread.__init__(self)
        self.stopped = event
        self.cats = cats
        self.catsId = catsId
        self.eventLoop = eventLoop

    def killThread(self):
        self.event.set()

    """
    post event to loop 
    that is waiting
    """

    def main(self):
        if not self.cats:
            self.killThread()
        else:
            cat = self.cats.popleft()
            e = self.eventLoop.Event(self.catsId, {"data": cat})
            self.eventLoop.post(e)

    """
    schedule cat events on a delay
    to not block the main loop
    """

    def run(self):
        while not self.stopped.wait(10.0):
            self.main()
