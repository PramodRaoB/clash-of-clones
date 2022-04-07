import pickle
import sys
import time


class Replay:
    def __init__(self, f):
        self._all_frames = None
        self._previous_frame = time.time()
        self.frame_rate = 1/30
        try:
            self._all_frames = pickle.load(open(f, "rb"))
            for frame in self._all_frames:
                sys.stdout.write(frame)
                while time.time() - self._previous_frame < self.frame_rate:
                    pass
                self._previous_frame = time.time()
        except (OSError, IOError) as e:
            print("File does not exist")


args = sys.argv
if len(args) <= 1:
    print("Error: Enter a filename (example: replay.py replay1) to be replayed")
    sys.exit(1)

if len(args) > 2:
    print("Error: Too many arguments")
    sys.exit(1)

rep = Replay(args[1])
