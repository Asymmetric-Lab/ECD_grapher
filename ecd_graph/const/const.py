
import numpy as np
from scipy.constants import c, h, electron_volt

FACTOR_EV_NM = h*c/(10**-9*electron_volt)
np.seterr(divide='ignore', invalid='ignore')