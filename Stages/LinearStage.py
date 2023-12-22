from Stages.RocketStage import RocketStage
import numpy as np
from Fuels import FuelsKSP2
from utils import pareto
from Engine import KSP2_Engine
from utils import get_allow_engines_KSP2
from FuelTank import FuelTankKSP2


class LinearStage(RocketStage):

    def __init__(self, mass, engine, num_engines, cost, dv, fuel):
        super().__init__(mass, engine, num_engines, cost, 'Linear', dv, fuel)

    @classmethod
    def optimize_point(cls, pl, dv, max_eng_quant, asl_or_vac, TWR_req, min_type):
        stages = cls.optimize_plot([pl, pl], [dv, dv], 1, max_eng_quant, asl_or_vac, TWR_req,
                                   plot=False, min_type=min_type)
        return stages

    @classmethod
    def get_best_empty_fraction(cls, eng_type, max_eng_quant, num_engines):
        if eng_type == 'SolidFuel':
            best_empty_fraction = [eng.empty_ratio for eng in cls.engines if eng.fuel_type == eng_type]
            best_empty_fraction = np.tile(best_empty_fraction, max_eng_quant)
            best_empty_fraction = np.reshape(best_empty_fraction, [1, 1, len(num_engines)])
        else:
            best_empty_fraction = cls.tanks.__getattribute__(eng_type)['percent_structure']
        return best_empty_fraction

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, max_eng_quant, asl_or_vac, TWR_req, plot=True, min_type='mass',
                      filename='Optimal_Rocket_Plot.png'):
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
        all_mfs = np.empty([span, span, 0])

        all_mtot = np.empty([span, span, 0])
        all_costs = np.empty([span, span, 0])

        for eng_type in unique_eng_types:
            dv_array, pl_array, isp, T, eng_mass, eng_cost, eng_name, num_engines, built_in_fuel = \
                cls.setup_physics_arrays(dv, pl, eng_type, max_eng_quant, asl_or_vac)

            best_empty_fraction = cls.get_best_empty_fraction(eng_type, max_eng_quant, num_engines)

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

            # Calculate Ms which is the Structure
            ms = m100 * best_empty_fraction
            # Calculate Mf which is the mass of fuel
            mf = m100 - ms
            fuel_units = mf / cls.fuels.get_fuel_data(eng_type, 'Density')
            costs = ms * cls.tanks.best_cost_per_ton_structure(fuel_units, eng_type) + eng_cost + \
                    mf * cls.fuels.get_fuel_data(eng_type, 'Cost')
            # Calculate m_tot which is the Structure + fuel + PL + engine masses
            m_tot = m100 + pl_array + eng_mass
            TWR0 = T / (m_tot * 9.8)

            all_engines.extend(eng_name)
            all_quant_engines.extend(num_engines)

            m_tot[m100 <= 0] = np.inf
            costs[m100 <= 0] = np.inf

            m_tot[TWR0 < TWR_req] = np.inf
            costs[TWR0 < TWR_req] = np.inf

            if eng_type == 'SolidFuel':
                m_tot[built_in_fuel < fuel_units] = np.inf
                costs[built_in_fuel < fuel_units] = np.inf

            all_mtot = np.concatenate((all_mtot, m_tot), axis=2)
            all_costs = np.concatenate((all_costs, costs), axis=2)
            all_mfs = np.concatenate((all_mfs, fuel_units), axis=2)

        if plot:
            min_mtot = np.min(all_mtot, axis=2)
            min_costs = np.min(all_costs, axis=2)

            min_mtot_idx = np.argmin(all_mtot, axis=2)
            min_costs_idx = np.argmin(all_costs, axis=2)

            min_mtot_idx[min_mtot == np.inf] = -1
            min_costs_idx[min_costs_idx == np.inf] = -1

            if min_type == 'mass':
                cls.plotDVPLDiagram(min_mtot_idx, all_engines, all_quant_engines, pl, dv, filename, asl_or_vac, TWR_req)
            else:
                cls.plotDVPLDiagram(min_costs_idx, all_engines, all_quant_engines, pl, dv, filename, asl_or_vac, TWR_req)

        elif span == 1:
            if min_type == 'mass':
                idx = [np.argmin(all_mtot)]
            elif min_type == 'cost':
                idx = pareto(np.concatenate((all_costs[0, :, :], all_mtot[0, :, :]), axis=0).T, [-1, -1])
            else:
                raise NotImplementedError("Optimization is only implemented for mass or cost")
            stages = [None] * len(idx)
            for i in range(len(idx)):
                stages[i] = cls(all_mtot[0, 0, idx[i]], all_engines[idx[i]], all_quant_engines[idx[i]],
                                all_costs[0, 0, idx[i]], dv[0], all_mfs[0, 0, idx[i]])
            return stages
        else:
            raise NotImplementedError("Multi-span pareto optimization is currently not supported")

    @classmethod
    def _forward_data_generator(cls, eng, flight_cond, pl_array, m100_array, n_eng_max):

        num_eng = np.arange(1, n_eng_max + 1)

        if m100_array.ndim < 3:
            m100_array = np.expand_dims(m100_array, 2)
            m100_array = np.tile(m100_array, (1, 1, len(num_eng)))

        pl_array = np.expand_dims(pl_array, 2)
        pl_array = np.tile(pl_array, (1, 1, len(num_eng)))

        num_eng_in = np.arange(1, n_eng_max + 1)
        num_eng_in = np.reshape(num_eng_in, [1, 1, len(num_eng_in)])
        if eng.is_radial:
            num_eng_in[0] = 2
        best_empty_fraction = cls.get_best_empty_fraction(eng.fuel_type, n_eng_max, num_eng_in)
        m1 = pl_array + num_eng_in * eng.mass + m100_array * best_empty_fraction
        m0 = pl_array + num_eng_in * eng.mass + m100_array
        if flight_cond == 'asl':
            isp = eng.isp_asl
            T = eng.thrust_asl
        else:
            isp = eng.isp_vac
            T = eng.thrust_vac
        dv_array = isp * 9.8 * np.log(m0 / m1)

        return dv_array, pl_array, m100_array


class LinearStageKSP2(LinearStage):
    tanks = FuelTankKSP2()
    engines = KSP2_Engine.setupEngines(get_allow_engines_KSP2())
    fuels = FuelsKSP2
