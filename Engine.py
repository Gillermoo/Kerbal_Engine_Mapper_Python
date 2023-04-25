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
        self.thrust_asl = Tasl
        self.thrust_vac = Tv
        self.isp_asl = ISPasl
        self.isp_vac = ISPv
        self.cost = cost
        self.is_Radial = isRadial
        self.fuel_type = fuelType
        self.built_in_fuel = builtInFuel

    def __str__(self):
        return f"""Name: {self.name}
                Size: {self.size}
                Cost: {self.cost}
                Mass: {self.mass}
                Thrust ASL: {self.thrust_asl}
                Thrust VAC: {self.thrust_vac}
                TWR ASL: {self.thrust_asl/self.mass}
                TWR VAC: {self.thrust_vac/self.mass}
                ISP ASL: {self.isp_asl}
                ISP VAC: {self.isp_vac}"""

    def __repr__(self):
        return self.__str__()

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
                solidFuelCost = Fuels.SolidFuel['Cost']
                emptyCost = eng['Cost'] - solidFuelCost * eng['Solid Fuel']

                if eng['Size'] == 'Radial mounted':
                    isRadial = True
                else:
                    isRadial = False

                engines.append(SRB_Engine(eng['Name'], eng['Mass Empty'], eng['Thrust ASL'], eng['Thrust VAC'], eng['ISP ASL'],
                                      eng['ISP VAC'], emptyCost, isRadial, 'SolidFuel', eng['Solid Fuel'],
                               eng['Mass Empty'] / eng['Mass Full']))


        return engines

class SRB_Engine(Engine):

    def __init__(self, name: str, mass: float, Tasl: float, Tv: float, ISPasl: float, ISPv: float, cost: float, \
                 isRadial: bool, fuelType: str, builtInFuel: float, empty_ratio: float):
        super().__init__(name, mass, Tasl, Tv, ISPasl, ISPv, cost, isRadial, fuelType, builtInFuel)
        self.empty_ratio = empty_ratio
