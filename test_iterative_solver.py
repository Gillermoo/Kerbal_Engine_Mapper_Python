from Stages.LinearStage import LinearStage as LS
from Stages.RocketStage import RocketStage
import time


def main():
    pl_bounds = [.01, 4000]
    dv_bounds = [100, 6500]
    span = 1000
    eng = RocketStage.engines[10]
    t0 = time.time()
    LS.optimize_plot(pl_bounds, dv_bounds, 500, 5, 'asl', TWR_req=1, plot=True, min_type='mass')


if __name__ == "__main__":
    main()