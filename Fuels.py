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
    liquidFuel = {'Cost': 0.8,
                  'Density': 5.0 / 1000}
    oxidizer = {'Cost': 0.18,
                'Density': 5.0 / 1000}
    solidFuel = {'Cost': 0.6,
                 'Density': 7.5 / 1000}
    xenon = {'Cost': 4.0,
             'Density': .1 / 1000}

    str_lookup = {'Liquid Fuel': liquidFuel,
                  'Oxidizer': oxidizer,
                  'Solid Fuel': solidFuel,
                  'Xenon': xenon}

    def get_data(self, fuel_str: str, param_str: str) -> float:
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
        return self.str_lookup[fuel_str][param_str]