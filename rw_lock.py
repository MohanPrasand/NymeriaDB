import threading


class RWLock:

    def __init__(self):
        self.condition = threading.Condition(threading.Lock())
        self.readers = 0
        self.writer = False
        self.waiting_writers = 0

    def acquire_read(self):
        with self.condition:
            while self.writer or self.waiting_writers > 0:
                self.condition.wait()

            self.readers += 1

    def release_read(self):
        with self.condition:
            self.readers -= 1

            if self.readers == 0:
                self.condition.notify_all()

    def acquire_write(self):
        with self.condition:
            self.waiting_writers += 1

            try:
                while self.readers > 0 or self.writer:
                    self.condition.wait()

                self.writer = True
            finally:
                self.waiting_writers -= 1

    def release_write(self):
        with self.condition:
            self.writer = False
            self.condition.notify_all()