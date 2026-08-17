# tests/test_rwlock.py

import threading
import time
import unittest

from rw_lock import RWLock


class TestRWLock(unittest.TestCase):

    def test_multiple_readers_can_run_together(self):
        lock = RWLock()

        active_readers = 0
        max_readers = 0

        mutex = threading.Lock()

        def reader():
            nonlocal active_readers, max_readers

            lock.acquire_read()

            with mutex:
                active_readers += 1
                max_readers = max(max_readers, active_readers)

            time.sleep(0.2)

            with mutex:
                active_readers -= 1

            lock.release_read()

        threads = [
            threading.Thread(target=reader)
            for _ in range(5)
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(max_readers, 5)


if __name__ == "__main__":
    unittest.main()