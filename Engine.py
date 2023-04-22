import pandas as pd
import os
from Fuels import Fuels

class Engine:
    """
    Class representing a rocket engine with its properties and methods to set up a list of engines.
    """

    def __init__(self, name: str, mass: float, Tasl: float, Tv: float, ISPasl: float, ISPv: float, cost: float, \
                 isRadial: bool, fuelType: str, builtInFuel: float):
        """
        Initializes an instance of the Engine class with its properties.

        Args:
            name (str): The name of the engine.
            mass (float): The mass of the engine in tons.
            Tasl (float): The thrust of the engine at sea level in kN.
            Tv (float): The thrust of the engine in a vacuum in kN.
            ISPasl (float): The specific impulse of the engine at sea level in seconds.
            ISPv (float): The specific impulse of the engine in a vacuum in seconds.
            cost (int): The cost of the engine in funds.
            isRadial (bool): True if the engine is radial mounted, False otherwise.
            fuelType (str): The type of fuel used by the engine.
            builtInFuel (int): The amount of fuel in units built into the engine. Set to 0 if there is none.
        """
        self.name = name
        self.mass = mass
        self.Tasl = Tasl
        self.Tv = Tv
        self.ISPasl = ISPasl
        self.ISPv = ISPv
        self.cost = cost
        self.isRadial = isRadial
        self.fuelType = fuelType
        self.builtInFuel = builtInFuel

    @staticmethod
    def setupEngines(allowedEngines: dict) -> list:
        """
        Reads the rocket engine data from CSV files, creates a list of engines and returns it.

        Args:
            allowedEngines (list): The list of allowed engine names to use in the game.

        Returns:
            list: A list of Engine objects created from the CSV files.
        """
        RF_engines = pd.read_csv(os.path.join('data', 'RFEngines.csv'))
        SRB = pd.read_csv(os.path.join('data', 'SRB.csv'))

        engines = []

        for idx, eng in RF_engines.iterrows():
            # Determine if the engine is radial or not
            if eng['Size'] == 'Radial mounted':
                isRadial = True
            else:
                isRadial = False

            # Determine the fuel type and amount of built-in fuel for the engine
            if eng['Name'] == 'Nerv':
                fuelType = 'LF'
            elif eng['Name'] == 'Dawn':
                fuelType = 'Xenon'
            else:
                fuelType = 'LFOX'

            if eng['Name'] == 'Twin-Boar':
                builtInFuel = 6400
            else:
                builtInFuel = 0

            # Create a new Engine object and add it to the list of engines
            if eng['Name'] in allowedEngines:
                engines.append(Engine(eng['Name'], eng['Mass'], eng['Thrust ASL'], eng['Thrust VAC'], eng['ISP ASL'],
                                      eng['ISP VAC'], eng['Cost'], isRadial, fuelType, builtInFuel))

        for idx, eng in SRB.iterrows():
            if eng['Name'] in allowedEngines:
                solidFuelCost = Fuels.solidFuel['Cost']
                emptyCost = eng['Cost'] - solidFuelCost * eng['Solid Fuel']

                if eng['Size'] == 'Radial mounted':
                    isRadial = True
                else:
                    isRadial = False

                engines.append(Engine(eng['Name'], eng['Mass Empty'], eng['Thrust ASL'], eng['Thrust VAC'], eng['ISP ASL'],
                                      eng['ISP VAC'], emptyCost, isRadial, fuelType, eng['Solid Fuel']))


        return engines