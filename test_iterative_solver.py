from Stages.LinearStage import LinearStage as LS
from Stages.LinearStage import LinearStage_KSP2 as LS2
from Stages.RocketStage import RocketStage
import time


def main():
    pl_bounds = [.1, 300]
    dv_bounds = [100, 6500]
    span = 100
    num_engines = 1
    asl_or_vac = 'asl'
    TWR_req = 1.5
    plot = True
    min_type = 'mass'
    #eng = RocketStage.engines[10]
    t0 = time.time()
    #LS.optimize_plot(pl_bounds, dv_bounds, span, num_engines, asl_or_vac, TWR_req=TWR_req, plot=plot, min_type=min_type,
    #                 filename='KSP1')
    LS2.optimize_plot(pl_bounds, dv_bounds, span, num_engines, asl_or_vac, TWR_req=TWR_req, plot=plot, min_type=min_type,
                      filename='KSP2')
    print(1)

if __name__ == "__main__":
    main()