from Stages.LinearStage import LinearStage as LS
from Stages.LinearStage import LinearStageKSP2 as LS2
from Stages.RocketStage import RocketStage
import time
from utils import rand_cmap


def main():
    pl_bounds = [.1, 300]
    dv_bounds = [100, 20000]
    span = 1000
    num_engines = 1
    asl_or_vac = 'vac'
    TWR_req = 1.5
    plot = True
    min_type = 'mass'
    #eng = RocketStage.engines[10]
    t0 = time.time()
    LS.optimize_plot(pl_bounds, dv_bounds, span, num_engines, asl_or_vac, TWR_req=TWR_req, plot=plot, min_type=min_type,
                     filename='KSP1vacbig')
    LS2.optimize_plot(pl_bounds, dv_bounds, span, num_engines, asl_or_vac, TWR_req=TWR_req, plot=plot, min_type=min_type,
                      filename='KSP2vacbig')
    print(1)

if __name__ == "__main__":
    main()