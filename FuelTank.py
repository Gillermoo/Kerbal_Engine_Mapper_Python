import pandas as pd
import os
from Fuels import Fuels
import numpy as np
from utils import pareto
from matplotlib import pyplot as plt

class FuelTank:
    """
    Class for calculating the dominant tanks for different types of fuel in a rocket.

    Attributes:
    -----------
    LF: dict
        Dictionary with the attributes of the dominant tank for liquid fuel.
    LFOX: dict
        Dictionary with the attributes of the dominant tank for liquid fuel and oxidizer.
    xenon: dict
        Dictionary with the attributes of the dominant tank for xenon.

    Methods:
    --------
    makeDominantTanks(costPerTonStructure, totalFuelCapacity):
        Static method that calculates the indices of the dominant tanks for a given fuel type.
    bestCostPerTonStructure(totalFuelCapacity, fuelType):
        Calculates the best cost per ton of structure for a given fuel type and total fuel capacity.
    """

    def __init__(self):
        RF_tanks_df = pd.read_csv(os.path.join('data', 'RFTanks.csv'), encoding="ISO-8859-1")
        LF_tanks_df = pd.read_csv(os.path.join('data', 'LFTanks.csv'), encoding="ISO-8859-1")
        Xenon_tanks_df = pd.read_csv(os.path.join('data', 'XenonTanks.csv'), encoding="ISO-8859-1")

        cost_LFOX_fuel = RF_tanks_df['Liquid Fuel'] * Fuels.liquidFuel['Cost'] + RF_tanks_df['Oxidizer'] * \
                         Fuels.oxidizer['Cost']
        costPerTonStructure = (RF_tanks_df['Cost Full'] - cost_LFOX_fuel) / RF_tanks_df['Mass Empty']
        totalFuelCapacity = RF_tanks_df['Liquid Fuel'] + RF_tanks_df['Oxidizer']
        idx = self.make_dominant_tanks(costPerTonStructure, totalFuelCapacity)
        self.LFOX = {'percentStructure': (RF_tanks_df['Mass Empty'].iloc[idx] / RF_tanks_df['Mass Full'].iloc[idx]).min(),
                     'costPerTonStructure': ((RF_tanks_df['Cost Full'].iloc[idx] - cost_LFOX_fuel.iloc[idx]) /
                                             RF_tanks_df['Mass Empty'].iloc[idx]),
                     'totalFuelCapacity': totalFuelCapacity.iloc[idx]}

        cost_LF_fuel = LF_tanks_df['Liquid Fuel'] * Fuels.liquidFuel['Cost']
        costPerTonStructure = (LF_tanks_df['Cost Full'] - cost_LF_fuel) / LF_tanks_df['Mass Empty']
        totalFuelCapacity = LF_tanks_df['Liquid Fuel']
        idx = self.make_dominant_tanks(costPerTonStructure, totalFuelCapacity)
        self.LF = {
            'percentStructure': (LF_tanks_df['Mass Empty'].iloc[idx] / LF_tanks_df['Mass Full'].iloc[idx]).min(),
            'costPerTonStructure': ((LF_tanks_df['Cost Full'].iloc[idx] - cost_LF_fuel.iloc[idx]) /
                                    LF_tanks_df['Mass Empty'].iloc[idx]),
            'totalFuelCapacity': totalFuelCapacity.iloc[idx]}

        cost_xenon_fuel = Xenon_tanks_df['Xenon'] * Fuels.xenon['Cost']
        costPerTonStructure = (Xenon_tanks_df['Cost Full'] - cost_xenon_fuel) / Xenon_tanks_df['Mass Empty']
        totalFuelCapacity = Xenon_tanks_df['Xenon']
        idx = self.make_dominant_tanks(costPerTonStructure, totalFuelCapacity)
        self.xenon = {
            'percentStructure': (Xenon_tanks_df['Mass Empty'].iloc[idx] / Xenon_tanks_df['Mass Full'].iloc[idx]).min(),
            'costPerTonStructure': ((Xenon_tanks_df['Cost Full'].iloc[idx] - cost_xenon_fuel.iloc[idx]) /
                                    Xenon_tanks_df['Mass Empty'].iloc[idx]),
            'totalFuelCapacity': totalFuelCapacity.iloc[idx]}

    @staticmethod
    def make_dominant_tanks(cost_per_ton_structure, total_fuel_capacity):
        """
        Determines the dominant tanks based on the cost per ton structure and total fuel capacity.

        Args:
        cost_per_ton_structure: A list of costs per ton structure for each tank.
        total_fuel_capacity: A list of total fuel capacities for each tank.

        Returns:
        The indices of the dominant tanks sorted in ascending order by total fuel capacity.
        """
        X = pd.concat((total_fuel_capacity, cost_per_ton_structure), axis=1).to_numpy()
        idx = pareto(X, [1, 1])
        idx_sort = np.argsort(total_fuel_capacity[idx])
        return idx[idx_sort]

    def best_cost_per_ton_structure(self, total_fuel_capacity, fuel_type):
        """
        Determines the best cost per ton structure for a given fuel type and total fuel capacity.

        Args:
        total_fuel_capacity: The total fuel capacity of the tank.
        fuel_type: The type of fuel used in the tank.

        Returns:
        The cost per ton structure for the specified fuel type and total fuel capacity.

        Raises:
        NotImplementedError: If the fuel type requested does not exist.
        """
        if fuel_type == 'LF':
            return self.LF['costPerTonStructure'][np.searchsorted(self.LF['totalFuelCapacity'], total_fuel_capacity)]
        if fuel_type == 'LFOX':
            return self.LFOX['costPerTonStructure'][
                np.searchsorted(self.LFOX['totalFuelCapacity'], total_fuel_capacity)]
        if fuel_type == 'Xenon':
            return self.xenon['costPerTonStructure'][
                np.searchsorted(self.xenon['totalFuelCapacity'], total_fuel_capacity)]
        else:
            raise NotImplementedError('The fuel type you requested does not exist')