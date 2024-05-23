import traceback
import logging


def sign(n):
    return (n > 0) - (n < 0)


def delay(f, *args):
    return lambda: f(*args)


class Lock:
    def __init__(self, lock):
        self._lock = lock

    def release(self):
        tb = traceback.extract_stack(limit=2)
        line = f"rel {tb[0][0]}:{tb[0][1]} {tb[0][2]}"
        logging.debug(line)
        self._lock.release()
        logging.debug("rel done")

    def acquire(self):
        tb = traceback.extract_stack(limit=2)
        line = f"acq {tb[0][0]}:{tb[0][1]} {tb[0][2]}"
        logging.debug(line)
        self._lock.acquire()
        logging.debug("acq done")
