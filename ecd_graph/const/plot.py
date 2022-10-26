import matplotlib.pyplot as plt
import os
import pickle
import numpy as np

from classes.File import File
from .report import create_report
from .const import FACTOR_EV_NM



def save_graph(graphs:list, fig, graph_directory:str):
    with open(os.path.join(graph_directory, 'ecd.pickle'), 'wb') as f:
        pickle.dump(fig, f)

    for ecd in graphs:
        np.save(os.path.join(graph_directory, f"{ecd.fname}-graph.npy"), np.array([(x, y) for x, y in zip(FACTOR_EV_NM/ecd.x, ecd.y)]))

    plt.savefig(os.path.join(graph_directory, 'ecd.png'), dpi=700)



def label_plot(ax, ax2, norm:float, initial_lambda:float, final_lambda:float):
    ax.set_ylim((-norm-0.1, norm+0.1))
    if ax2: ax2.set_ylim((-norm-0.1, norm+0.1))
    if ax2: ax2.set_ylabel('Rotary Strenght')
    ax.set_xlim((initial_lambda, final_lambda))
    ax.hlines(0, 0, 30000, 'grey', linewidth=.95)
    ax.set_ylabel(r'$\Delta \varepsilon$ (a.u.)')
    ax.set_xlabel('Wavelenght (nm)')
    


def plot(graphs:list, refs:list, shift:list, title:str, show_R:bool, norm:float, initial_lambda:float, final_lambda:float, save:bool, graph_directory:str, weighted=None, show_conformers:bool=False, no_weighted:bool=False):

    try:
        fig, axs = plt.subplots(ncols=1, nrows=len(refs), sharex=True)
    except TypeError:
        fig, axs = plt.subplots()
        axs = [axs]

    for idx, ax in enumerate(axs):

        # shift graphs
        if refs:
            if weighted:
                File.shift(weighted, refs[idx], shift[idx] if shift else None)
            if show_conformers or no_weighted:
                for i in graphs:
                    if refs[idx]: File.shift(i, refs[idx], shift[idx] if shift else weighted.shift_ev)

        # show graphs
        if weighted:
            weighted.plot(ax)
        if refs: 
            refs[idx].plot(ax, title)

        if show_conformers or no_weighted:
            alp = 0.3 if weighted else 1
            for i in graphs:
                i.plot(ax, alp)

        ax2 = None
        if show_R:
            ax2 = ax.twinx()
            weighted.plot_R(ax2, norm)
                
        label_plot(ax=ax, ax2=ax2, norm=norm, initial_lambda=initial_lambda, final_lambda=final_lambda)

        if refs:
            y_legend = -.35 if len(refs) > 1 else -0.125
        else:
            y_legend = -0.25

        legend = plt.legend(
            loc='upper center', bbox_to_anchor=(0.5, y_legend), fancybox=True, shadow=True, ncol=3
        )
        

        plt.tight_layout()

        if save: save_graph(graphs=graphs, fig=fig, graph_directory=graph_directory)

        plt.show()
