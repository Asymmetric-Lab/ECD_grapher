from .Ecd import ECD
from .File import File
import numpy as np
from const.const import FACTOR_EV_NM, plotted


class Weighted_Plot:

    def __init__(self, x, norm:float):
        self.filename = 'Weighted Plot'
        self.x = x
        self.y = np.zeros(self.x.shape)

        self.R, self.eV = [], []

        for i in ECD.ecds:
            self.y += i.y*i.pop
            self.R += list(i.R)
            self.eV += list(i.eV)
        self.R, self.eV = np.array(self.R), np.array(self.eV)

        self.y = File.normalise(self.y, norm=norm)
        
        self.x_indx_peak = self.find_peak()
        self.shift_ev = 0

    def find_peak(self):
        max_ = np.argmax(self.y)
        min_ = np.argmin(self.y)
        return max_ if self.y[max_] > -self.y[min_] else min_

    def data(self):
        return FACTOR_EV_NM/(self.x+self.shift_ev), self.y

    def generate_report(self):
        return ' | '.join([ self.filename, ' ', str(np.round(self.shift_ev, 4)), ', '.join(np.array(self.eV, dtype=str)), ', '.join(np.array(self.R, dtype=str))]) + ' | '

    def plot(self, ax):
        x, y = FACTOR_EV_NM/(self.x+self.shift_ev), self.y
        plot = ax.plot(x, y, label=self.filename)
        plotted[self.filename] = plot

    def plot_R(self, ax, norm):
        for _, i in enumerate(zip(self.R/np.max(np.abs(self.R))*norm/2, self.eV+self.shift_ev)):
            R, eV = i
            lb = None
            ax.vlines(FACTOR_EV_NM/eV, 0, R, color='red', label=lb)