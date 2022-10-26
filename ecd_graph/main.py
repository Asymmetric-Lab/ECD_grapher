from const import *
from classes import *

def main():
    args = parser()
    check_parser(args)

    if args.save: create_folder(args.graph_directory)

    # generating graphs and convulate them
    graphs = [ECD(
            fname=i,
            FWHM=args.fwhm,
            is_xy=args.compare,
            invert=args.invert,
            initial_lambda = args.initial_lambda,
            final_lambda = args.final_lambda,
            definition = args.definition,
            sigma = args.sigma,
            level = args.level,
            norm = args.normalisation,
            ) for i in args.file]

    
    # get reference
    refs = None
    if args.reference:
        refs = [Ref(i) for i in args.reference]

        
    # weighted graph
    weighted = None
    if not args.no_weighted:
        weighted = Weighted_Plot(x=graphs[0].x, norm = args.normalisation)

    
    # population
    pff = None
    if args.pop_from_file:
        with open(args.pop_from_file) as f:
            pff = {File.get_filename(i.split()[0].strip()):float(i.strip().split()[1]) for i in f.readlines() if i.strip()}

    for idx, i in enumerate(graphs):
        i.get_pop(idx=idx, p=args.pop, pff=pff)
    
    if args.save: create_report(0, weighted, args.sigma, args.graph_directory , args.fwhm)



if __name__ == '__main__':
    main()