import numpy as np
import os

class File:

    def __init__(self):
        pass

    @staticmethod
    def readinput(filename):
        with open(filename) as f:
            return f.read()

    @staticmethod
    def get_filename(filename):
        _, tail = os.path.split(filename)
        return tail.split('.')[0] if tail else filename.split('.')[0]

    @staticmethod
    def obtain_xy(file):
        x = np.array([float(i.split()[0].strip()) for i in file.splitlines() if i])
        y = np.array([float(i.split()[1].strip()) for i in file.splitlines() if i])
        return x, y

    @staticmethod
    def normalise(array, norm):
        return array/(np.max(np.abs(array))) * norm