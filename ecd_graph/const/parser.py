import argparse


def parser():
    parser = argparse.ArgumentParser()

    # files
    parser.add_argument('file', help='Log file(s) of the TD-SCF calculation', nargs='+')
    parser.add_argument('-r', '--reference', help='File xy of the ECD plot sperimental', nargs='+') #, required=True)
    parser.add_argument('--ref_eV', action='store_false', help='If the reference graph is ∆ε against eV, use this flag.')
    parser.add_argument('--compare', action='store_true', help='Input file are already convoluted ECD spectra')
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
    parser.add_argument('-gd','--graph_directory', help='Define the directory in which you want to save the files of the graph. Default: %(default)s', default='ecd_report')




    # define popuation of the ensemble
    parser.add_argument('-p', '--pop', help='Define the population of the conformers indicated. Use with caution and be sure of the order. MAX population = 1', nargs='+', type=float)
    parser.add_argument('-pff', '--pop_from_file',help='File containg population of conformes. Names must be the same of the TDDFT files')

    return parser.parse_args()


def check_parser(args):
    if args.shift: 
        if len(args.shift)==1: 
            args.shift*=len(args.file)
            return args
        elif len(args.shift) != len(args.file):
            Exception('Number of shifts defined is not the same number of files parsed')
