class RocketStage:
    def __init__(self, mass, engine, numEngines, cost, stage_type, dv, fuel, LF, OX, xenon):
        self.mass = mass
        self.engine = engine
        self.num_engines = numEngines
        self.cost = cost
        self.type = stage_type
        self.dv = dv
        self.fuel = fuel
        self.LF = LF
        self.OX = OX
        self.xenon = xenon

    def toString(obj, print_header=True):
        """
        toString Prints out the stage to a string
        """
        if print_header:
            str1 = '| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |'.format('Mass', 'Engine', 'Delta-V', 'Type',
                                                                           'Total Fuel')
            print(str1)
        str2 = '| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |'.format(obj.mass, obj.engines, obj.dv, obj.type,
                                                                       obj.fuel)
        print(str2)

    def optimize_point(self):
        """
        Optimizes a rocket stage for a given point

        Returns:
            RocketStage: An optimized rocket stage.
        """
        raise NotImplementedError(f"""optimize_point() function is not implemented for {self.__class__}""")

    def optimize_plot(self):
        """
        Optimizes a rocket stage for a given sweep of points

        Plots:
            Plot of Engine indicies that are labeled for each engine type
        """
        raise NotImplementedError(f"""optimize_plot() function is not implemented for {self.__class__}"""

class Payload_Stage(RocketStage):
    def __init__(self, PL):
        super.__init__(self, PL, [], 0, 0, 'PL', 0, 0, 0, 0, 0)
    def optimize_point(self):
        return self

    def optimize_plot(self):
        pass