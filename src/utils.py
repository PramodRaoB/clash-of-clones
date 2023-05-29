import errno
import os
import subprocess
import time


def wait(curr, target):
    if time.time() - curr < target:
        return True
    return False


def numbers(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    for filename in os.listdir(path):
        name, _ = os.path.splitext(filename)
        yield int(name[6:])


def play_audio(file):
    pass
    # with open(os.devnull, 'wb') as devnull:
    #     subprocess.Popen(["mpg123", file], stdout=devnull, stderr=devnull)
