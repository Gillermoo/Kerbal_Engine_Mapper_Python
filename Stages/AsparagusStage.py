from Stages.RocketStage import RocketStage
import numpy as np


class AsparagusStage(RocketStage):

    def __init__(self, mass, engine, num_engines_array, cost, dv, fuel):
        super().__init__(mass, engine, np.sum(num_engines_array), cost, 'Asparagus', dv, fuel)
        self.num_engines_array = num_engines_array

    @classmethod
    def optimize_point(cls, pl, dv, max_eng_quant, asl_or_vac, TWR_req, min_type):
        pass

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, max_eng_quant, asl_or_vac, TWR_req):
        pass
