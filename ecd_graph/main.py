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
        refs = [Ref(i, col_ref=args.col_ref, is_nm=args.ref_eV, norm=args.normalisation) for i in args.reference]

        
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
    
        
    plot(graphs=graphs, refs=refs, shift=args.shift, title=args.title, show_R=args.show_R, norm=args.normalisation, initial_lambda=args.initial_lambda, final_lambda=args.final_lambda, save=args.save, level=args.level, graph_directory=args.graph_directory, weighted=weighted, show_conformers=args.show_conformers, no_weighted=args.no_weighted)

    if args.save: create_report(0, weighted, args.sigma, args.graph_directory , args.fwhm)




if __name__ == '__main__':
    main()
