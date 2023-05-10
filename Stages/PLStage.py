from Stages.RocketStage import RocketStage


class PayloadStage(RocketStage):
    def __init__(self, pl):
        super().__init__(pl, [], 0, 0, 'PL', 0, 0)

    @classmethod
    def optimize_point(cls, pl, dv, max_eng_quant, asl_or_vac, TWR_req, min_type):
        return cls(pl)

    @classmethod
    def optimize_plot(cls, pl_span, dv_span, span, max_eng_quant, asl_or_vac, TWR_req):
        pass
