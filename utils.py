import logging
from hashlib import sha1
from time import perf_counter


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_hostname():
    import platform
    return platform.node()


def calculate_hash(path):
    """Returns sha1 secure hash / message digest for the file at `path`"""
    t1 = perf_counter()
    s = sha1()
    with open(path, "rb") as f:
        s.update(f.read())
    t2 = perf_counter()
    elapsed_in_ms = (t2 - t1) * 1000
    logger.debug(f"Hashed {path} in {elapsed_in_ms:.3f} ms")
    return s.hexdigest()

