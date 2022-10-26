import argparse
import os

import matplotlib.pyplot as plt

#### GAUSSIAN NOT IMPLEMENTED YET


if __name__ == '__main__':

   

    
    
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


