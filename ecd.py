import argparse
import os
import numpy as np
from scipy.constants import c, h, electron_volt
import matplotlib.pyplot as plt
import shutil
import sys
import pickle

#### GAUSSIAN NOT IMPLEMENTED YET

FACTOR_EV_NM = h*c/(10**-9*electron_volt)
np.seterr(divide='ignore', invalid='ignore')

parser = argparse.ArgumentParser()

# files
parser.add_argument('file', help='Log file(s) of the TD-SCF calculation', nargs='+')
parser.add_argument('-r', '--reference', help='File xy of the ECD plot sperimental', nargs='+', required=True)
parser.add_argument('--ref_eV', action='store_false', help='If the reference graph is ∆ε against eV, use this flag.')
parser.add_argument('--compare', action='store_true', help='Iput file are already convoluted ECD spectra')
parser.add_argument('-l', '--level', help='Define the computational level of the simulated graph')


# convolution details
parser.add_argument('-i','--invert', action='store_true', help='Invert the y sign, in order to obtain the enantiomer\'s ECD')
parser.add_argument('-il', '--initial_lambda', help='Inital wavelenght. Default: %(default)s nm', default=200, type=int)
parser.add_argument('-fl', '--final_lambda', help='Final wavelenght. Default: %(default)s nm', default=450, type=int)
parser.add_argument('-fwhm', help='Full width at half maximum. Defaul %(default)s eV', default=1/3, type=float)
parser.add_argument('-si', '--sigma', help='Peak width, considered as dispertion σ for a gaussian curve', default=0, type=float)
parser.add_argument('-sh', '--shift', type=float, help='Define a default shift in eV. If multiple references, specify shift for each reference', nargs='+')



# graph details
parser.add_argument('-def', '--definition', help='Definition of the spectra of eV spanned spectra. Add more points on which calculate the absortion. (MAX-MIN)*10^d. Default: %(default)s', default=4, type=float)
parser.add_argument('-n', '--normalisation', help='Set the normalisation range. Default: [-%(default)s, %(default)s]', default=1)
parser.add_argument('-sc','--show_conformers', help='Show all the plots of all conformers passed', action='store_true')
parser.add_argument('-sR', '--show_R', help='Show Rstrenght bar in the plot (only for weightered plot)', action='store_true')
parser.add_argument('-nw','--no_weighted', help='Do not show weighted plot on the graph. Use this for benchmarks or comparison.', action='store_true')
parser.add_argument('-t','--title', help='Title of the graph')

parser.add_argument('--save', help='Save pickle and csvs of the graph', action='store_true')
parser.add_argument('-gd','--graph_directory', help='Define the directory in which you want to save the files of the graph. Default: %(default)s', default='scan_graph')




# define popuation of the ensemble
parser.add_argument('-p', '--pop', help='Define the population of the conformers indicated. Use with caution and be sure of the order. MAX population = 1', nargs='+', type=float)
parser.add_argument('-pff', '--pop_from_file',help='File containg population of conformes. Names must be the same of the TDDFT files')


args = parser.parse_args()

if args.shift: 
    if len(args.shift)==1: 
        args.shift*=len(args.file)
    elif len(args.shift) != len(args.file):
        Exception('Number of shifts defined is not the same number of files parsed')

class File:

    def __init__(self):
        pass

    @staticmethod
    def readinput(filename):
        with open(filename) as f:
            return f.read()

    @staticmethod
    def get_filename(filename):
        head, tail = os.path.split(filename)
        return tail.split('.')[0] if tail else filename.split('.')[0]

    @staticmethod
    def obtain_xy(file):
        x = np.array([float(i.split()[0].strip()) for i in file.splitlines() if i])
        y = np.array([float(i.split()[1].strip()) for i in file.splitlines() if i])
        return x, y



class Ref:

    def __init__(self, filename, is_nm=args.ref_eV):
        self.title = File.get_filename(filename).replace('_', ' ').title()
        self.filename = 'Exp. Graph'
        self.fl = File.readinput(filename)
        self.x, self.y = File.obtain_xy(self.fl)
        if is_nm: self.x = self.convert_to_eV()
        self.y = ECD.normalise(self.y)
        self.x_indx_peak = self.find_peak()

    def __str__(self):
        return self.filename


    def convert_to_eV(self):
        x = self.x[:]
        return FACTOR_EV_NM/x

    def find_peak(self):
        max_ = np.argmax(self.y)
        min_ = np.argmin(self.y)
        return max_ if self.y[max_] > -self.y[min_] else min_

    def data(self):
        return FACTOR_EV_NM/self.x, self.y
        
    def plot(self, ax):
        plot = ax.plot(FACTOR_EV_NM/self.x, self.y, label=self.filename, color='brown')
        plotted[self.filename] = plot
        ax.set_title(f'{self.title} experimental peak comparison' if not args.title else args.title)


class ECD:
    o_patterns_s = ['CD SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS', 'CD SPECTRUM']
    # g_patterns_s = '<0|del|b> * <b|rxdel|0> + <0|del|b> * <b|delr+rdel|0>'
    o_p_final = 'Total run time'
    o_stddft_p_f = 'sTD-DFT done'

    x = np.linspace(
        FACTOR_EV_NM/(args.initial_lambda-100) if FACTOR_EV_NM/(args.initial_lambda-100) > 0 else 0.00000000000001,
        FACTOR_EV_NM/(args.final_lambda+100),
        10**args.definition)

    ecds = []

    def __init__(self, filename, FWHM=args.fwhm, is_xy=args.compare, invert=args.invert) -> None:
        self.ecds.append(self)

        self.filename = File.get_filename(filename)
        self.file = File.readinput(filename)
        self.orca = 'O   R   C   A' in self.file
        self.fl = self.filter_input_data()
        if is_xy:
            self.x, self.y = File.obtain_xy(self.file)
        else:
            self.eV = self.collect_energies()
            self.R = self.collect_R()
            if invert:
                self.R *= -1
            self.y = self.convolution(FWHM=args.fwhm, sigma=args.sigma)

        self.pop = 1.0
        self.shift_ev = 0.0
        self.level = args.level

        self.x_indx_peak = self.find_peak()

    def __str__(self):
        return self.filename

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

    def convolution(self, FWHM, sigma=None):
        s = args.sigma if args.sigma != float(0) else args.fwhm/(np.sqrt(2*np.log(2))*2)
        y = np.zeros(self.x.shape)
        for i, e in zip(self.R, self.eV):
            y += self.create_gaussian(self.x, s, i, e)
        y = ECD.normalise(y)
        return y

    @staticmethod
    def normalise(array):
        return array/(np.max(np.abs(array))) * args.normalisation

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
        return ' | '.join([self.filename, str(np.round(self.pop, 4)), str(np.round(self.shift_ev, 4)), ', '.join(np.array(self.eV, dtype=str)), ', '.join(np.array(self.R/self.pop, dtype=str))]) + ' | '

    def plot(self, ax, alph):
        x, y = FACTOR_EV_NM/(self.x+self.shift_ev), self.y
        plot = ax.plot(x, y, label=self.filename.replace('_', ' '), alpha=alph)
        plotted[self.filename] = plot
    
class Weighted_Plot:

    def __init__(self):
        self.filename = 'Weighted Plot'
        self.x = ECD.x
        self.y = np.zeros(self.x.shape)

        self.R, self.eV = [], []

        for i in ECD.ecds:
            self.y += i.y*i.pop
            self.R += list(i.R)
            self.eV += list(i.eV)
        self.R, self.eV = np.array(self.R), np.array(self.eV)

        self.y = ECD.normalise(self.y)
        
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
        plot = ax.plot(x, y, label=self.filename, color='salmon')
        plotted[self.filename] = plot

    def plot_R(self, ax):
        for idx, i in enumerate(zip(self.R/np.max(np.abs(self.R))*args.normalisation/2, self.eV+self.shift_ev)):
            R, eV = i
            lb = None
            ax.vlines(FACTOR_EV_NM/eV, 0, R, color='red', label=lb)


def get_pop(idx, i, pff:dict=None):
    if pff: return pff[i.filename]
    return args.pop[idx]

def shift(self, rif, user_shift=args.shift):
    if not user_shift: x_shift = rif.x[rif.x_indx_peak] - self.x[self.x_indx_peak]
    if user_shift: x_shift = user_shift
    self.shift_ev = x_shift

def create_folder():
    directory = args.graph_directory   

    if os.path.exists(directory):
        if 'y' in input(f'A directory named {directory} already exists. Existing directory  will be deleted, wanna procede? [y/n]').lower():
            shutil.rmtree(directory)   
        else:
            sys.exit()
    os.mkdir(directory)


def save_graph(fig):
    with open(os.path.join(args.graph_directory, 'ecd.pickle'), 'wb') as f:
        pickle.dump(fig, f)

    for ecd in ECD.ecds:
        np.savetxt(os.path.join(args.graph_directory, f"{ecd.filename}-graph.txt"), np.array([(x, y) for x, y in zip(FACTOR_EV_NM/ecd.x, ecd.y)]), newline='\n')

    plt.savefig(os.path.join(args.graph_directory, 'ecd.png'), dpi=700)


def create_report(idx, w):
    head = ['Filename', 'Pop', 'Shift (eV)', 'Transition Energy (eV)', 'R']
    t = '|' + ' | '.join(head) + '|\n' 
    t += '|'.join([':--:' for _ in head])+ '|\n'
    t += '|\n'.join([i.generate_report() for i in ECD.ecds])+ '|'
    if w: t += '|\n'+w.generate_report() + '|\n'
    s = args.sigma if args.sigma != float(0) else args.fwhm/(np.sqrt(2*np.log(2))*2)
    t += '' + f'| Sigma (eV) | {np.round(s, 4)} | FWHM (eV) | {args.fwhm if args.sigma != float(0) else np.round(2*s*np.sqrt(2*np.log(2)), 4)} | |'
    with open(f'{args.graph_directory}/report_{idx}.md', 'w') as f:
        f.write(t)


def multi_plot():
    fig, axs = plt.subplots(ncols=1, nrows=len(args.reference), sharex=True)

    for idx, ax in enumerate(axs):

        # shift graphs
        if weighted:
            shift(weighted, refs[idx], args.shift[idx] if args.shift else None)
        if args.show_conformers or args.no_weighted:
            for i in graphs:
                if refs[idx]: shift(i, refs[idx], args.shift[idx] if args.shift else weighted.shift_ev)

        # show graphs
        if weighted:
            weighted.plot(ax)
        if refs: 
            refs[idx].plot(ax)

        if args.show_conformers or args.no_weighted:
            alp = 0.3 if weighted else 1
            for i in graphs:
                i.plot(ax, alp)

        ax2 = None
        if args.show_R:
            ax2 = ax.twinx()
            weighted.plot_R(ax2)
                
        label_plot(ax, ax2)

def single_plot():
    fig, ax = plt.subplots()

    # shift graphs
    if weighted and refs:
        shift(weighted, refs[0], args.shift[0] if args.shift else None)
    if (args.show_conformers or args.no_weighted) and refs:
        for i in graphs:
            if refs: shift(i, refs[0], args.shift[0] if args.shift else weighted.shift_ev)
            
    # show graphs
    if weighted:
        weighted.plot(ax)
    if refs: 
        refs[0].plot(ax)

    if args.show_conformers or args.no_weighted:
        alp = 0.3 if weighted else 1
        for i in graphs:
            i.plot(ax, alp)

    ax2 = None
    if args.show_R:
        ax2 = ax.twinx()
        weighted.plot_R(ax2)
            
    label_plot(ax, ax2)

def label_plot(ax, ax2):
    ax.set_ylim((-args.normalisation-0.1, args.normalisation+0.1))
    if ax2: ax2.set_ylim((-args.normalisation-0.1, args.normalisation+0.1))
    ax.set_xlim((args.initial_lambda, args.final_lambda))
    if args.save: create_report(0, weighted)
    ax.hlines(0, 0, 30000, 'grey', linewidth=.95)
    ax.set_ylabel(r'$\Delta \varepsilon$ (a.u.)')
    ax.set_xlabel('Wavelenght (nm)')


if __name__ == '__main__':

    if args.save: create_folder()

    # generating graphs and convulate them
    graphs = [ECD(i) for i in args.file]

    # get reference
    refs = None
    if args.reference:
        refs = [Ref(i) for i in args.reference]

    # weighted graph
    weighted = None
    if not args.no_weighted:
        weighted = Weighted_Plot()

    # population
    pff = None
    if args.pop_from_file:
        with open(args.pop_from_file) as f:
            pff = {File.get_filename(i.split()[0].strip()):float(i.strip().split()[1]) for i in f.readlines() if i.strip()}
    
    for idx, i in enumerate(graphs):
        i.pop = get_pop(idx, i, pff)

    plotted = {}
    if args.reference:
        if len(args.reference) > 1:
            multi_plot()
        else:
            single_plot()
    else:
        single_plot()
    
    if args.reference:
        y_legend = -.35 if len(args.reference) > 1 else -0.125
    else:
        y_legend = -0.25

    legend = plt.legend(
        loc='upper center', bbox_to_anchor=(0.5, y_legend), fancybox=True, shadow=True, ncol=3
    )
    

    plt.tight_layout()

    if args.save: save_graph(plt.gcf())

    plt.show()


