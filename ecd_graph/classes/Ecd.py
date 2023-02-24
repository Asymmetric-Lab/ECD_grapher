from ecd_graph.const.const import FACTOR_EV_NM, c, h, electron_volt, plotted
from .File import File
import numpy as np


class ECD:
    o_patterns_s = ['CD SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS', 'CD SPECTRUM']
    # g_patterns_s = '<0|del|b> * <b|rxdel|0> + <0|del|b> * <b|delr+rdel|0>'
    o_p_final = 'Total run time'
    o_stddft_p_f = 'sTD-DFT done'


    ecds = []

    def __init__(self, fname:str, FWHM:float, is_xy:bool, invert:bool, initial_lambda:float, final_lambda:float, definition:int, sigma:float, level:str, norm:float) -> None:
        
        self.x = np.linspace(
            FACTOR_EV_NM/(initial_lambda-100) if FACTOR_EV_NM/(initial_lambda-100) > 0 else 0.00000000000001,
            FACTOR_EV_NM/(final_lambda+100),
            10**definition)
        self.ecds.append(self)

        self.fname = File.get_filename(fname)
        self.file = File.readinput(fname)
        self.orca = 'O   R   C   A' in self.file
        self.fl = self.filter_input_data()
        if is_xy:
            self.x, self.y = File.obtain_xy(self.file)
        else:
            self.eV = self.collect_energies()
            self.R = self.collect_R()
            if invert:
                self.R *= -1
            self.y = self.convolution(FWHM=FWHM, sigma=sigma, norm=norm)

        self.pop = 1.0
        self.shift_ev = 0.0
        self.level = level

        self.x_indx_peak = self.find_peak()

    def __str__(self):
        return self.fname

    def filter_input_data(self):
        if self.orca:
            return self.split_orca()

    def split_orca(self):
        fl = self.file
        for i in self.o_patterns_s:
            fl = fl.split(i)[-1]
        fl = fl.split(self.o_p_final)[0].split(self.o_stddft_p_f)[0]
        return fl.strip().splitlines()[4:]

    def collect_energies(self):
        return h*c/(np.array([float(i.split()[2]) for i in self.fl])*10**-9*electron_volt)

    def collect_R(self):
        return np.array([float(i.split()[3]) for i in self.fl])

    def create_gaussian(self, x, sigma, r, ev):
        return r/(sigma*np.sqrt(2*np.pi)) * np.exp(-0.5*((x-ev)/sigma)**2)

    def convolution(self, FWHM, sigma=None, norm=1):
        s = sigma if sigma != float(0) else FWHM/(np.sqrt(2*np.log(2))*2)
        y = np.zeros(self.x.shape)
        for i, e in zip(self.R, self.eV):
            y += self.create_gaussian(self.x, s, i, e)
        y = File.normalise(y, norm)
        return y

    def weight_plot(self):
        self.R *= self.pop
        self.y *= self.pop

    def find_peak(self):
        max_ = np.argmax(self.y)
        min_ = np.argmin(self.y)
        return max_ if self.y[max_] > -self.y[min_] else min_

    def data(self):
        return FACTOR_EV_NM/(self.x+self.shift_ev), self.y

    def generate_report(self):
    
        return ' | '.join([self.fname, str(np.round(self.pop, 4)), f'{self.shift_ev:.9f}', ', '.join(np.array(self.eV, dtype=str)), ', '.join(np.array(self.R/self.pop, dtype=str))]) + ' | '

    def plot(self, ax, alph):
        x, y = FACTOR_EV_NM/(self.x+self.shift_ev), self.y
        plot = ax.plot(x, y, label=self.fname.replace('_', ' '), alpha=alph)
        plotted[self.fname] = plot

    def get_pop(self, idx, p, pff:dict=None):
        if pff: 
            self.pop = pff[self.fname] 
            return
        self.pop = p[idx]