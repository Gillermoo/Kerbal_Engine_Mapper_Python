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
    make_dominant_tanks(costPerTonStructure, totalFuelCapacity):
        Static method that calculates the indices of the dominant tanks for a given fuel type.
    best_cost_per_ton_structure(totalFuelCapacity, fuelType):
        Calculates the best cost per ton of structure for a given fuel type and total fuel capacity.
    """

    def __init__(self):
        rf_tanks_df = pd.read_csv(os.path.join('data', 'RFTanks.csv'), encoding="ISO-8859-1")
        lf_tanks_df = pd.read_csv(os.path.join('data', 'LFTanks.csv'), encoding="ISO-8859-1")
        xenon_tanks_df = pd.read_csv(os.path.join('data', 'XenonTanks.csv'), encoding="ISO-8859-1")

        cost_lfox_fuel = rf_tanks_df['Liquid Fuel'] * Fuels.LF['Cost'] + rf_tanks_df['Oxidizer'] * \
                         Fuels.OX['Cost']
        cost_per_ton_structure = (rf_tanks_df['Cost Full'] - cost_lfox_fuel) / rf_tanks_df['Mass Empty']
        total_fuel_capacity = rf_tanks_df['Liquid Fuel'] + rf_tanks_df['Oxidizer']
        idx = self.make_dominant_tanks(cost_per_ton_structure, total_fuel_capacity)
        self.LFOX = {
            'percent_structure': (rf_tanks_df['Mass Empty'].iloc[idx] / rf_tanks_df['Mass Full'].iloc[idx]).min(),
            'cost_per_ton_structure': (cost_per_ton_structure[idx]).to_numpy(),
            'total_fuel_capacity': total_fuel_capacity.iloc[idx]}

        cost_lf_fuel = lf_tanks_df['Liquid Fuel'] * Fuels.LF['Cost']
        cost_per_ton_structure = (lf_tanks_df['Cost Full'] - cost_lf_fuel) / lf_tanks_df['Mass Empty']
        total_fuel_capacity = lf_tanks_df['Liquid Fuel']
        idx = self.make_dominant_tanks(cost_per_ton_structure, total_fuel_capacity)
        self.LF = {
            'percent_structure': (lf_tanks_df['Mass Empty'].iloc[idx] / lf_tanks_df['Mass Full'].iloc[idx]).min(),
            'cost_per_ton_structure': (cost_per_ton_structure[idx]).to_numpy(),
            'total_fuel_capacity': total_fuel_capacity.iloc[idx]}

        cost_xenon_fuel = xenon_tanks_df['Xenon'] * Fuels.Xenon['Cost']
        cost_per_ton_structure = (xenon_tanks_df['Cost Full'] - cost_xenon_fuel) / xenon_tanks_df['Mass Empty']
        total_fuel_capacity = xenon_tanks_df['Xenon']
        idx = self.make_dominant_tanks(cost_per_ton_structure, total_fuel_capacity)
        self.Xenon = {
            'percent_structure': (xenon_tanks_df['Mass Empty'].iloc[idx] / xenon_tanks_df['Mass Full'].iloc[idx]).min(),
            'cost_per_ton_structure': (cost_per_ton_structure[idx]).to_numpy(),
            'total_fuel_capacity': total_fuel_capacity.iloc[idx]}

        SRB = pd.read_csv(os.path.join('data', 'SRB.csv'))
        self.SolidFuel = {
            'percent_structure': SRB['Mass Empty'] / SRB['Mass Full'],
            'cost_per_ton_structure': [0],
            'total_fuel_capacity': SRB['Solid Fuel'],
            'names': SRB['Name']}

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
        x = pd.concat((total_fuel_capacity, cost_per_ton_structure), axis=1).to_numpy()
        idx = pareto(x, [1, 1])
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
            idx = np.searchsorted(self.LF['total_fuel_capacity'], total_fuel_capacity)
            bounded_idx = np.min((idx, np.full_like(idx, len(self.LF['total_fuel_capacity'])-1)))
            return self.LF['cost_per_ton_structure'][bounded_idx]
        if fuel_type == 'LFOX':
            idx = np.searchsorted(self.LFOX['total_fuel_capacity'], total_fuel_capacity)
            bounded_idx = np.min((idx, np.full_like(idx, len(self.LFOX['total_fuel_capacity'])-1)))
            return self.LFOX['cost_per_ton_structure'][bounded_idx]
        if fuel_type == 'Xenon':
            idx = np.searchsorted(self.Xenon['total_fuel_capacity'], total_fuel_capacity)
            bounded_idx = np.min((idx, np.full_like(idx, len(self.Xenon['total_fuel_capacity'])-1)))
            return self.Xenon['cost_per_ton_structure'][bounded_idx]
        if fuel_type == 'SolidFuel':
            return 0
        else:
            raise NotImplementedError('The fuel type you requested does not exist')
