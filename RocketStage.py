import numpy as np
from FuelTank import FuelTank
from Engine import Engine
from utils import get_allow_engines
from Fuels import Fuels
from matplotlib import pyplot as plt


class RocketStage:
    """
    RocketStage KSP Rocket Stage
    """
    tanks = FuelTank()
    engines = Engine.setupEngines(get_allow_engines())
    g = 9.8

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
    def setup_physics_arrays(cls, dv, pl, eng_type, max_eng_quant, asl_or_vac):
        """
        setup_physics_arrays sets up a multi-dimensional array to be used in the mathematical modeling of the engines.
        """
        engines = [eng for eng in cls.engines if eng.fuel_type == eng_type]
        num_engines = cls.count_rep(max_eng_quant, len(engines))

        dv_array, pl_array = np.meshgrid(dv, pl, indexing='ij')
        dv_array = np.expand_dims(dv_array, 2)
        np.tile(dv_array, (1, 1, len(engines)))

        pl_array = np.expand_dims(pl_array, 2)
        np.tile(pl_array, (1, 1, len(engines)))

        if asl_or_vac == 'asl':
            isp = np.array([eng.isp_asl for eng in engines])
            T = np.array([eng.thrust_asl for eng in engines])
        elif asl_or_vac == 'vac':
            isp = np.array([eng.isp_vac for eng in engines])
            T = np.array([eng.thrust_vac for eng in engines])
        else:
            raise NotImplementedError('Other values for asl_or_vac have not been implemented')
        isp = np.tile(isp, max_eng_quant)
        isp = np.reshape(isp, [1, 1, len(num_engines)])

        T = np.tile(T, max_eng_quant) * num_engines
        T = np.reshape(T, [1, 1, len(num_engines)])

        eng_mass = [eng.mass for eng in engines]
        eng_mass = np.tile(eng_mass, max_eng_quant) * num_engines
        eng_mass = np.reshape(eng_mass, [1, 1, len(num_engines)])

        eng_cost = [eng.cost for eng in engines]
        eng_cost = np.tile(eng_cost, max_eng_quant) * num_engines
        eng_cost = np.reshape(eng_cost, [1, 1, len(num_engines)])

        eng_name = [eng.name for eng in engines]
        eng_name = np.tile(eng_name, max_eng_quant)

        built_in_fuel = [eng.built_in_fuel for eng in engines]
        built_in_fuel = np.tile(built_in_fuel, max_eng_quant) * num_engines
        built_in_fuel = np.reshape(built_in_fuel, [1, 1, len(num_engines)])

        return dv_array, pl_array, isp, T, eng_mass, eng_cost, eng_name, num_engines, built_in_fuel

    @classmethod
    def optimize_point(cls, pl, dv, max_eng_quant, asl_or_vac, TWR_req):
        """
        Optimizes a rocket stage for a given point

        Returns:
            RocketStage: An optimized rocket stage.
        """
        raise NotImplementedError(f"""optimize_point() function is not implemented for {cls.__class__}""")

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, max_eng_quant, asl_or_vac, TWR_req):
        """
        Optimizes a rocket stage for a given sweep of points

        Plots:
            Plot of Engine indicies that are labeled for each engine type
        """
        raise NotImplementedError(f"""optimize_plot() function is not implemented for {cls.__class__}""")

    @staticmethod
    def count_rep(reps, max_count):
        arr = np.arange(1, reps + 1)
        repeated = np.repeat(arr, max_count)
        return repeated


class PayloadStage(RocketStage):
    def __init__(self, pl):
        super().__init__(pl, [], 0, 0, 'PL', 0, 0, 0, 0, 0)

    @classmethod
    def optimize_point(cls, pl, dv, max_eng_quant, asl_or_vac, TWR_req):
        return cls(pl)

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, max_eng_quant, asl_or_vac, TWR_req):
        pass


class LinerStage(RocketStage):
    def __init__(self, mass, engine, num_engines, cost, dv, fuel, lf, ox, xenon):
        super().__init__(mass, engine, num_engines, cost, 'Linear', dv, fuel, lf, ox, xenon)

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, max_eng_quant, asl_or_vac, TWR_req):
        """
        Optimizes a rocket stage for a given sweep of points

        Plots:
            Plot of Engine indicies that are labeled for each engine type
        """
        pl = np.logspace(np.log10(pl_span[0]), np.log10(pl_span[1]), span)
        dv = np.linspace(dv_span[0], dv_span[1], span)

        # Group engines by fuel type
        unique_eng_types = set([eng.fuel_type for eng in cls.engines])

        all_engines = []
        all_quant_engines = []

        all_mtot = np.empty([span, span, 0])
        all_costs = np.empty([span, span, 0])

        for eng_type in unique_eng_types:
            dv_array, pl_array, isp, T, eng_mass, eng_cost, eng_name, num_engines, built_in_fuel = \
                cls.setup_physics_arrays(dv, pl, eng_type, max_eng_quant, asl_or_vac)
            if eng_type == 'SolidFuel':
                best_empty_fraction = [eng.empty_ratio for eng in cls.engines if eng.fuel_type == eng_type]
                best_empty_fraction = np.tile(best_empty_fraction, max_eng_quant)
                best_empty_fraction = np.reshape(best_empty_fraction, [1, 1, len(num_engines)])
            else:
                best_empty_fraction = cls.tanks.__getattribute__(eng_type)['percent_structure']
            # Solve the rocket equation for the total mass of fuel tanks m100
            # Δv = ISP * g * ln(m0 / m1)
            # Given:
            # m100 = mass_structure + mass_fuel
            # ms = mass_structure = m100 * empty_fraction
            # m0  = mass_PL + mass_engines + mass_structure + mass_fuel = mass_PL + mass_engines + m100
            # m1 = mass_PL + mass_engines + ms = mass_PL + mass_engines + m100 * empty_fraction
            #                 Δv
            # exp =  e ^ _____________
            #              (isp * g)
            #
            #          (PL + mass_engine) * (1 - exp)
            # m100 = _________________________________
            #             empty_fraction * exp - 1

            exp = np.exp(dv_array / (isp * cls.g))
            # Calculate M100 which is the Structure + fuel
            m100 = (pl_array + eng_mass) * (1 - exp) / (best_empty_fraction * exp - 1)
            m100[m100 <= 0] = np.inf
            # Calculate Ms which is the Structure
            ms = m100 * best_empty_fraction
            # Calculate Mf which is the mass of fuel
            mf = m100 - ms
            fuel_units = mf / Fuels.get_fuel_data(eng_type, 'Density')
            costs = ms * cls.tanks.best_cost_per_ton_structure(fuel_units, eng_type) + eng_cost + \
                    mf * Fuels.get_fuel_data(eng_type, 'Cost')
            # Calculate m_tot which is the Structure + fuel + PL + engine masses
            m_tot = m100 + pl_array + eng_mass
            TWR0 = T / m_tot

            all_engines.append(eng_name)
            all_quant_engines.append(num_engines)

            m_tot[TWR0 < TWR_req] = np.inf
            costs[TWR0 < TWR_req] = np.inf

            if eng_type == 'SolidFuel':
                m_tot[built_in_fuel < fuel_units] = np.inf
                costs[built_in_fuel < fuel_units] = np.inf

            all_mtot = np.concatenate((all_mtot, m_tot), axis=2)
            all_costs = np.concatenate((all_costs, costs), axis=2)

        min_mtot = np.min(all_mtot, axis=2)
        min_costs = np.min(all_costs, axis=2)

        min_mtot_idx = np.argmin(all_mtot, axis=2)
        min_costs_idx = np.argmin(all_costs, axis=2)

        min_mtot_idx[min_mtot == np.inf] = -1
        min_costs_idx[min_costs_idx == np.inf] = -1

        plt.imshow(min_mtot_idx, cmap='tab20c')
        plt.show()