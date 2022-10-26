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

    @staticmethod
    def shift(w, rif, user_shift):
        if not user_shift: x_shift = rif.x[rif.x_indx_peak] - w.x[w.x_indx_peak]
        if user_shift: x_shift = user_shift
        w.shift_ev = x_shift