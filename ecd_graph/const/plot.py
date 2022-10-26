import matplotlib.pyplot as plt
import os
import pickle



def save_graph(fig):
    with open(os.path.join(args.graph_directory, 'ecd.pickle'), 'wb') as f:
        pickle.dump(fig, f)

    for ecd in ECD.ecds:
        np.savetxt(os.path.join(args.graph_directory, f"{ecd.filename}-graph.txt"), np.array([(x, y) for x, y in zip(FACTOR_EV_NM/ecd.x, ecd.y)]), newline='\n')

    plt.savefig(os.path.join(args.graph_directory, 'ecd.png'), dpi=700)



def label_plot(ax, ax2):
    ax.set_ylim((-args.normalisation-0.1, args.normalisation+0.1))
    if ax2: ax2.set_ylim((-args.normalisation-0.1, args.normalisation+0.1))
    ax.set_xlim((args.initial_lambda, args.final_lambda))
    if args.save: create_report(0, weighted)
    ax.hlines(0, 0, 30000, 'grey', linewidth=.95)
    ax.set_ylabel(r'$\Delta \varepsilon$ (a.u.)')
    ax.set_xlabel('Wavelenght (nm)')


def plot():
    fig, axs = plt.subplots(ncols=1, nrows=len(args.reference), sharex=True)

    for idx, ax in enumerate(list(axs)):

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