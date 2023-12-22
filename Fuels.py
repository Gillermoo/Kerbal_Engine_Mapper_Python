class Fuels:
    """
    A class representing various fuel types with their associated costs and densities.

    Attributes:
    -----------
    liquidFuel: dict
        A dictionary representing the properties of liquid fuel, including the cost in Funds/Unit and density in Tons/Unit.
    oxidizer: dict
        A dictionary representing the properties of oxidizer fuel, including the cost in Funds/Unit and density in Tons/Unit.
    solidFuel: dict
        A dictionary representing the properties of solid fuel, including the cost in Funds/Unit and density in Tons/Unit.
    xenon: dict
        A dictionary representing the properties of xenon fuel, including the cost in Funds/Unit and density in Tons/Unit.

    Methods:
    --------
    get_data(fuel_str: str, param_str: str) -> Union[float, int]
        Given a fuel type and parameter, returns the associated value.
    """

    # Cost in Funds/Unit
    # Density in Tons/Unit
    LF = {'Cost': 0.8,
          'Density': 5.0 / 1000}
    OX = {'Cost': 0.18,
          'Density': 5.0 / 1000}
    SolidFuel = {'Cost': 0.6,
                 'Density': 7.5 / 1000}
    Xenon = {'Cost': 4.0,
             'Density': .1 / 1000}
    LFOX = {'Cost': (0.9 * LF['Cost'] + 1.1 * LF['Cost']) / 2.0,
            'Density': (0.9 * LF['Density'] + 1.1 * LF['Density']) / 2.0}

    @classmethod
    def get_fuel_data(cls, fuel_str: str, param_str: str) -> float:
        """
        Given a fuel type and parameter, returns the associated value.

        Parameters:
        -----------
        fuel_str: str
            The name of the fuel type to look up.
        param_str: str
            The name of the parameter to retrieve.

        Returns:
        --------
        Union[float, int]
            The value associated with the fuel type and parameter.
        """
        return getattr(cls, fuel_str)[param_str]


class FuelsKSP2(Fuels):
    LF = {'Cost': 0,
          'Density': 1}
    OX = {'Cost': 0,
          'Density': 1}
    SolidFuel = {'Cost': 0,
                 'Density': 1}
    Xenon = {'Cost': 0,
             'Density': 1}
    LFOX = {'Cost': 0,
            'Density': 1}
    Hydrogen = {'Cost': 0,
                'Density': 1}
