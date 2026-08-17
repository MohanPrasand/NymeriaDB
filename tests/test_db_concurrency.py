import threading
import unittest

from database import Database


class TestDatabaseConcurrency(unittest.TestCase):

    def test_concurrent_inserts(self):
        db = Database("concurrency_test")

        def writer(start):
            for i in range(start, start + 100):
                db.insert(f"key-{i}", str(i))

        threads = [
            threading.Thread(
                target=writer,
                args=(i * 100,)
            )
            for i in range(5)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        for i in range(500):
            self.assertEqual(
                db.get(f"key-{i}"),
                str(i)
            )


if __name__ == "__main__":
    unittest.main()