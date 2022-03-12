import time


def wait(curr, target):
    if time.time() - curr < target:
        return True
    return False
