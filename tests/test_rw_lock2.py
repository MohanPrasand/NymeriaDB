import threading
import time
import unittest

from rw_lock import RWLock


class TestRWLock(unittest.TestCase):

    def test_writer_waits_for_readers(self):
        lock = RWLock()

        reader_started = threading.Event()
        release_reader = threading.Event()
        writer_entered = threading.Event()

        def reader():
            lock.acquire_read()
            reader_started.set()

            release_reader.wait()

            lock.release_read()

        def writer():
            reader_started.wait()

            lock.acquire_write()
            writer_entered.set()
            lock.release_write()

        reader_thread = threading.Thread(target=reader)
        writer_thread = threading.Thread(target=writer)

        reader_thread.start()
        writer_thread.start()

        # Make sure the reader has acquired the lock.
        self.assertTrue(reader_started.wait(timeout=1))

        # Writer must still be waiting because reader is active.
        self.assertFalse(writer_entered.is_set())

        # Let the reader leave.
        release_reader.set()

        # Now the writer should be able to enter.
        writer_thread.join(timeout=1)

        self.assertTrue(writer_entered.is_set())

        reader_thread.join()


    def test_new_reader_waits_when_writer_is_waiting(self):
        lock = RWLock()

        reader_started = threading.Event()
        release_reader = threading.Event()

        writer_started_waiting = threading.Event()
        release_writer = threading.Event()
        writer_entered = threading.Event()

        second_reader_entered = threading.Event()

        def reader1():
            lock.acquire_read()
            reader_started.set()

            release_reader.wait()

            lock.release_read()

        def writer():
            reader_started.wait()

            lock.acquire_write()
            writer_entered.set()

            release_writer.wait()

            lock.release_write()

        def reader2():
            # Wait until the writer has entered before attempting to read.
            writer_entered.wait()

            lock.acquire_read()
            second_reader_entered.set()
            lock.release_read()

        r1 = threading.Thread(target=reader1)
        w = threading.Thread(target=writer)
        r2 = threading.Thread(target=reader2)

        r1.start()
        w.start()

        # Wait for reader 1 to acquire the lock.
        self.assertTrue(reader_started.wait(timeout=1))

        # Give the writer a chance to start waiting.
        time.sleep(0.05)

        # Reader 1 is still holding the lock, so writer cannot enter.
        self.assertFalse(writer_entered.is_set())

        # Release reader 1.
        release_reader.set()

        # Writer should now acquire the lock.
        self.assertTrue(writer_entered.wait(timeout=1))

        # Start reader 2 while writer is active.
        r2.start()

        # Reader 2 must wait for writer.
        self.assertFalse(second_reader_entered.is_set())

        # Release writer.
        release_writer.set()

        # Reader 2 should now enter.
        self.assertTrue(second_reader_entered.wait(timeout=1))

        r1.join()
        w.join()
        r2.join()


if __name__ == "__main__":
    unittest.main()