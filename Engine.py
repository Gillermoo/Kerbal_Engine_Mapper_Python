import csv


class Engine:
    """This class represents an engine in Kerbal Space Program and contains all the data for that engine.

    Attributes:
        name (str): The name of the engine.
        size (str): The size of the engine.
        cost (int): The cost of the engine.
        mass (float): The mass of the engine.
        max_temp (int): The maximum temperature of the engine.
        tol_ms (int): The maximum speed the engine can withstand.
        tol_g (int): The maximum g-force the engine can withstand.
        thrust_asl (float): The thrust of the engine at sea level.
        thrust_vac (float): The thrust of the engine in a vacuum.
        twr_asl (float): The thrust to weight ratio of the engine at sea level.
        twr_vac (float): The thrust to weight ratio of the engine in a vacuum.
        max_fuel_cons (float): The maximum fuel consumption of the engine.
        isp_asl (int): The specific impulse of the engine at sea level.
        isp_vac (int): The specific impulse of the engine in a vacuum.

    Methods:
        __init__(self, name, size, cost, mass, max_temp, tolerance_mps, tolerance_g, thrust_asl, thrust_vac, twr_asl,
                    twr_vac, max_fuel_consumption, isp_asl, isp_vac): Initialises the engine object.
        __str__(self): Returns a string representation of the engine object.
        __repr__(self): Returns a string representation of the engine object.
        """

    def __init__(self, name: str, size: str, cost: int, mass: float, max_temp: int, tol_ms: int, tol_g: int,
                 thrust_asl: float, thrust_vac: float, twr_asl: float, twr_vac: float, max_fuel_cons: float,
                 isp_asl: int, isp_vac: int):
        self.name = name
        self.size = size
        self.cost = cost
        self.mass = mass
        self.max_temp = max_temp
        self.tol_ms = tol_ms
        self.tol_g = tol_g
        self.thrust_asl = thrust_asl
        self.thrust_vac = thrust_vac
        self.twr_asl = twr_asl
        self.twr_vac = twr_vac
        self.max_fuel_cons = max_fuel_cons
        self.isp_asl = isp_asl
        self.isp_vac = isp_vac

    def __str__(self):
        return f"""Name: {self.name}
Size: {self.size}
Cost: {self.cost}
Mass: {self.mass}
Max Temp: {self.max_temp}
Thrust ASL: {self.thrust_asl}
Thrust VAC: {self.thrust_vac}
TWR ASL: {self.twr_asl}
TWR VAC: {self.twr_vac}
Max Fuel Consumption: {self.max_fuel_cons}
ISP ASL: {self.isp_asl}
ISP VAC: {self.isp_vac}"""

    def __repr__(self):
        return self.__str__()


# Example usage on how we could use the Engine class
file_path = "file\\path\\here"
engine_list = []
with open(file_path, "r") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        engine_list.append(Engine(row["Name"], row["Size"], row["Cost"], row["Mass"], row["Max Temp"],
                                  row["Tolerance (m/s)"], row["Tolerance (g)"], row["Thrust ASL"], row["Thrust VAC"],
                                  row["TWR ASL"], row["TWR VAC"], row["Max Fuel Consumption"], row["ISP ASL"],
                                  row["ISP VAC"]))

print(engine_list[0])
