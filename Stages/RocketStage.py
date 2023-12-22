import numpy as np
from FuelTank import FuelTank
from Fuels import Fuels
from Engine import Engine, KSP2_Engine
from utils import get_allow_engines, rand_cmap, get_allow_engines_KSP2
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap


class RocketStage:
    """
    RocketStage KSP Rocket Stage
    """
    tanks = FuelTank()
    engines = Engine.setupEngines(get_allow_engines())
    fuels = Fuels

    '''
    This is what it would look like if you were creating a class that used the KSP2 Data
    tanks_KSP2 = FuelTank_KSP2()
    engines_KSP2 = KSP2_Engine.setupEngines(get_allow_engines_KSP2())
    '''
    g = 9.8

    def __init__(self, mass, engine, num_engines, cost, stage_type, dv, fuel):
        self.mass = mass
        self.engine = engine
        self.num_engines = num_engines
        self.cost = cost
        self.type = stage_type
        self.dv = dv
        self.fuel = fuel

    def toString(self, print_header=True):
        """
        toString Prints out the stage to a string
        """
        if print_header:
            str1 = '| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |'.format('Mass', 'Engine', 'Delta-V', 'Type',
                                                                           'Total Fuel')
            print(str1)
        str2 = '| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} |'.format(np.round(self.mass, 3),
                                                                       str(self.num_engines) + ' X ' + self.engine,
                                                                       self.dv, self.type, np.round(self.fuel))
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
        #dv_array = np.tile(dv_array, (1, 1, len(num_engines)))

        pl_array = np.expand_dims(pl_array, 2)
        #pl_array = np.tile(pl_array, (1, 1, len(num_engines)))

        is_radial = [eng.is_radial for eng in engines]
        is_radial = np.tile(is_radial, max_eng_quant)

        num_engines[np.where(is_radial & num_engines == 1)] = 2

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
    def optimize_point(cls, pl, dv, max_eng_quant, asl_or_vac, TWR_req, min_type):
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
        """
        Count repetition of numbers in a range.

        Args:
            reps (int): The number of repetitions.
            max_count (int): The maximum count of each number.

        Returns:
            numpy.ndarray: An array with repeated numbers.

        Example:
            >>> RocketStage.count_rep(3, 2)
            array([1, 1, 2, 2, 3, 3])
        """
        arr = np.arange(1, reps + 1)
        repeated = np.repeat(arr, max_count)
        return repeated

    @classmethod
    def forward_data_generator(cls, eng, flight_cond, pl_bounds, m100_bounds, pl_span, m100_span, n_eng_max):
        pl = np.logspace(np.log10(pl_bounds[0]), np.log10(pl_bounds[1]), pl_span)
        m100 = np.logspace(np.log10(m100_bounds[0]), np.log10(m100_bounds[1]), m100_span)

        pl_array, m100_array = np.meshgrid(pl, m100, indexing='ij')

        dv_array, pl_array, m100_array = cls._forward_data_generator(eng, flight_cond, pl_array, m100_array, n_eng_max)
        return dv_array, pl_array, m100_array

    @classmethod
    def _forward_data_generator(cls, eng, flight_cond, pl_array, m100_array, n_eng_max):
        raise NotImplementedError(f"""forward_data_generator function is not implemented for {cls.__class__}""")

    @classmethod
    def iterative_forward_optimizer(cls, eng, flight_cond, pl_bounds, dv_bounds, span, n_eng_max, max_iter=10,
                                    min_error=1e-1):
        pl = np.logspace(np.log10(pl_bounds[0]), np.log10(pl_bounds[1]), span)
        dv = np.linspace(dv_bounds[0], dv_bounds[1], span)

        pl_array, dv_array = np.meshgrid(pl, dv, indexing='ij')
        m100_array = np.ones_like(pl_array)

        dv_array = np.expand_dims(dv_array, 2)
        dv_array = np.tile(dv_array, (1, 1, n_eng_max))

        m100_array = np.expand_dims(m100_array, 2)
        m100_array = np.tile(m100_array, (1, 1, n_eng_max))

        tot_error = [0] * max_iter

        eta = 1e-6

        for i in range(max_iter):
            dv_array1, temp1, temp2 = cls._forward_data_generator(eng, flight_cond, pl_array, m100_array,
                                                                            n_eng_max)
            p1 = (dv_array1 - dv_array) ** 2
            dv_array2, temp1, temp2 = cls._forward_data_generator(eng, flight_cond, pl_array, m100_array + eta,
                                                                            n_eng_max)
            p2 = (dv_array2 - dv_array) ** 2
            d_error_d_m100 = (p2 - p1) / eta
            m100_array = m100_array - p1 / d_error_d_m100

            m100_array[np.isnan(m100_array)] = 1
            tot_error[i] = np.nanmean(p1)
            if tot_error[i] < min_error:
                break

        return dv_array, pl_array, m100_array

    @classmethod
    def plotDVPLDiagram(cls, min_tot_idx, all_engines, all_quant_engines, pl, dv, filename, condition, twr_req):
        max_eng_num = np.max(min_tot_idx)
        cmap = rand_cmap(max_eng_num, type='bright', first_color_black=False, last_color_black=False, verbose=False)
        plt.figure(figsize=(10, 10))
        DVDV, PLPL = np.meshgrid(dv, pl)
        plt.pcolormesh(DVDV, PLPL, min_tot_idx.transpose(), cmap=cmap)
        plt.yscale("log")
        def location_converter(point, dv, pl):
            transposed = [point[0, 0, 0], point[0, 0, 1]]
            transposed[0] = dv[transposed[0]]
            transposed[1] = pl[transposed[1]]
            return transposed

        for unique_id in np.unique(min_tot_idx):
            if unique_id == -1:
                continue
            #Find Centroid of the set of datapoints
            points = np.argwhere(min_tot_idx == unique_id)
            center = np.mean(points, axis=0)
            nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(points)
            nearest_idx = nbrs.kneighbors([center])
            nearest = location_converter(points[nearest_idx[1], :], dv, pl)
            plt.scatter(nearest[0], nearest[1], 20, color=cmap(unique_id / max_eng_num), edgecolors='k')
            plt.text(nearest[0], nearest[1], u"\u2190 " + str(all_quant_engines[unique_id]) + " " + all_engines[unique_id],
                     rotation=30, rotation_mode='anchor')
        plt.grid(which='both')
        plt.xlabel('Delta-V (m/s)')
        plt.ylabel('Payload (Metric Tons)')
        plt.title(condition + ' @ TWR: ' + str(twr_req))
        plt.savefig("plots/" + filename)



