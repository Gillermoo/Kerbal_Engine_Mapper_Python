class RocketStage:
    def __init__(self, mass, engine, num_engines, cost, stage_type, dv, fuel, lf, ox, xenon):
        self.mass = mass
        self.engine = engine
        self.num_engines = num_engines
        self.cost = cost
        self.type = stage_type
        self.dv = dv
        self.fuel = fuel
        self.LF = lf
        self.OX = ox
        self.xenon = xenon

    def toString(self, print_header=True):
        """
        toString Prints out the stage to a string
        """
        if print_header:
            str1 = '| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |'.format('Mass', 'Engine', 'Delta-V', 'Type',
                                                                           'Total Fuel')
            print(str1)
        str2 = '| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |'.format(self.mass, self.engines, self.dv, self.type,
                                                                       self.fuel)
        print(str2)

    @classmethod
    def optimize_point(cls, pl, dv, allow_engines, max_eng_quant):
        """
        Optimizes a rocket stage for a given point

        Returns:
            RocketStage: An optimized rocket stage.
        """
        raise NotImplementedError(f"""optimize_point() function is not implemented for {cls.__class__}""")

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, allow_engines, max_eng_quant):
        """
        Optimizes a rocket stage for a given sweep of points

        Plots:
            Plot of Engine indicies that are labeled for each engine type
        """
        raise NotImplementedError(f"""optimize_plot() function is not implemented for {cls.__class__}"""

class PayloadStage(RocketStage):
    def __init__(self, pl):
        super().__init__(pl, [], 0, 0, 'PL', 0, 0, 0, 0, 0)

    @classmethod
    def optimize_point(cls, pl, dv, allow_engines, max_eng_quant):
        return cls(pl)

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, allow_engines, max_eng_quant):
        pass

class LinerStage(RocketStage):
    def __init__(self, mass, engine, num_engines, cost, dv, fuel, lf, ox, xenon):
        super().__init__(mass, engine, num_engines, cost, 'Linear', dv, fuel, lf, ox, xenon)

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, allow_engines, max_eng_quant):


