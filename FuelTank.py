import pandas as pd
import os
from Fuels import Fuels

class FuelTank:

    def __init__(self):
        RF_tanks_df = pd.read_csv(os.path.join('data', 'RFTanks.csv'), encoding = "ISO-8859-1")
        LF_tanks_df = pd.read_csv(os.path.join('data', 'LFTanks.csv'), encoding = "ISO-8859-1")
        Xenon_tanks_df = pd.read_csv(os.path.join('data', 'LFTanks.csv'), encoding = "ISO-8859-1")

        cost_LFOX_fuel = RF_tanks_df['Liquid Fuel'] * Fuels.liquidFuel['Cost'] + RF_tanks_df['Oxidizer'] * Fuels.oxidizer[
            'Cost']
        self.LFOX = {'percentStructure': (RF_tanks_df['Mass Empty'] / RF_tanks_df['Mass Full']).min(),
                     'costPerTonStructure': ((RF_tanks_df['Cost Full'] - cost_LFOX_fuel) / RF_tanks_df['Mass Empty'])}

        self.RF_tanks = makeDominantTanks(RF_tanks_df)


        print(1)
    @staticmethod
    def makeDominantTanks(df):


