import pandas as pd
import os

class FuelTank:

    def __init__(self):
        RF_tanks = pd.read_csv(os.path.join('..', 'data', 'RFTanks.csv'))
        LF_tanks = pd.read_csv(os.path.join('..', 'data', 'LFTanks.csv'))
        Xenon_tanks = pd.read_csv(os.path.join('..', 'data', 'LFTanks.csv'))

