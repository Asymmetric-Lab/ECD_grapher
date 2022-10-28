# ECD graphs

Script to generate ECD graphs from ORCA TD-DFT calculation. \
Can be used to create various graphs from the same output with multiple references graph. 



```bash 
usage: ecd.py [-h] -r REFERENCE [REFERENCE ...] [--ref_eV] [--compare] [-l LEVEL] [-i] 
              [-il INITIAL_LAMBDA] [-fl FINAL_LAMBDA] [-fwhm FWHM] [-si SIGMA] 
              [-sh SHIFT [SHIFT ...]] [-def DEFINITION] [-n NORMALISATION] [-sc] [-sR] [-nw] 
              [-t TITLE] [--save] [-gd GRAPH_DIRECTORY] [-p POP [POP ...]] [-pff POP_FROM_FILE]
              file [file ...]

positional arguments:
  file                  Log file(s) of the TD-SCF calculation

options:
  -h, --help            show this help message and exit
  -r REFERENCE [REFERENCE ...], --reference REFERENCE [REFERENCE ...]
                        File xy of the ECD plot sperimental
  --ref_eV              If the reference graph is ∆ε against eV, use this flag.
  --compare             Input file are already convoluted ECD spectra
  -l LEVEL, --level LEVEL
                        Define the computational level of the simulated graph
  -i, --invert          Invert the y sign, in order to obtain the enantiomer's ECD
  -il INITIAL_LAMBDA, --initial_lambda INITIAL_LAMBDA
                        Inital wavelenght. Default: 200 nm
  -fl FINAL_LAMBDA, --final_lambda FINAL_LAMBDA
                        Final wavelenght. Default: 450 nm
  -fwhm FWHM            Full width at half maximum. Defaul 0.333 eV
  -si SIGMA, --sigma SIGMA
                        Peak width, considered as dispertion σ for a gaussian curve
  -sh SHIFT [SHIFT ...], --shift SHIFT [SHIFT ...]
                        Define a default shift in eV. If multiple references, specify shift for each reference
  -def DEFINITION, --definition DEFINITION
                        Definition of the spectra of eV spanned spectra. Add more points on which calculate the absortion. 
                        (MAX-MIN)*10^d. Default: 4
  -n NORMALISATION, --normalisation NORMALISATION
                        Set the normalisation range. Default: [-1, 1]
  -sc, --show_conformers
                        Show all the plots of all conformers passed
  -sR, --show_R         Show Rstrenght bar in the plot (only for weightered plot)
  -nw, --no_weighted    Do not show weighted plot on the graph. Use this for benchmarks or comparison.
  -t TITLE, --title TITLE
                        Title of the graph
  --save                Save pickle and csvs of the graph
  -gd GRAPH_DIRECTORY, --graph_directory GRAPH_DIRECTORY
                        Define the directory in which you want to save the files of the graph. Default: scan_graph
  -p POP [POP ...], --pop POP [POP ...]
                        Define the population of the conformers indicated. Use with caution and be sure of the order. MAX population = 1
  -pff POP_FROM_FILE, --pop_from_file POP_FROM_FILE
                        File containg population of conformes. Names must be the same of the TDDFT files
```
