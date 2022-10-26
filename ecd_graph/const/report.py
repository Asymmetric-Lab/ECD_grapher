import numpy as np
from classes.Ecd import ECD



def create_report(idx, w, sigma, graph_directory , fwhm):

    head = ['Filename', 'Pop', 'Shift (eV)', 'Transition Energy (eV)', 'R']

    t = '|' + ' | '.join(head) + '|\n' 

    t += '|'.join([':--:' for _ in head])+ '|\n'

    t += '|\n'.join([i.generate_report() for i in ECD.ecds])+ '|'

    if w: t += '|\n'+w.generate_report() + '|\n'

    s = sigma if sigma != float(0) else fwhm/(np.sqrt(2*np.log(2))*2)

    t += '|\n'
    t += '' + f'| Sigma (eV) | {np.round(s, 4)} | FWHM (eV) | {fwhm if sigma != float(0) else np.round(2*s*np.sqrt(2*np.log(2)), 4)} | |'

    with open(f'{graph_directory}/report_{idx}.md', 'w') as f:
        f.write(t)
