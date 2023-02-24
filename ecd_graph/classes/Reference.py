from .File import File 
from ecd_graph.const.const import FACTOR_EV_NM, plotted

import numpy as np 

class Ref:

    def __init__(self, filename, col_ref, is_nm=True, norm=1):
        self.col_ref = col_ref
        self.title = File.get_filename(filename).replace('_', ' ').title()
        self.filename = 'Exp. Graph'
        self.fl = File.readinput(filename)
        self.x, self.y = File.obtain_xy(self.fl)
        if is_nm: self.x = self.convert_to_eV()
        self.y = File.normalise(self.y, norm)
        self.x_indx_peak = self.find_peak()

    def __str__(self):
        return self.filena


    def convert_to_eV(self):
        x = self.x[:]
        return FACTOR_EV_NM/x

    def find_peak(self):
        max_ = np.argmax(self.y)
        min_ = np.argmin(self.y)
        return max_ if self.y[max_] > -self.y[min_] else min_

    def data(self):
        return FACTOR_EV_NM/self.x, self.y
        
    def plot(self, ax, level, t):
        plot = ax.plot(FACTOR_EV_NM/self.x, self.y, label=self.filename, color=self.col_ref)
        plotted[self.filename] = plot
        ax.set_title(f'{self.title} experimental peak comparison. {level}' if not t else t)