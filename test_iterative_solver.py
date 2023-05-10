from Stages.LinearStage import LinearStage as LS
from Stages.RocketStage import RocketStage
import time


def main():
    pl_bounds = [.01, 1000]
    dv_bounds = [100, 4000]
    span = 500
    eng = RocketStage.engines[10]
    t0 = time.time()
    LS.iterative_forward_optimizer(eng, 'asl', pl_bounds, dv_bounds, span, 4, max_iter=20)
    t1 = time.time()
    total = t1 - t0
    print(total)


if __name__ == "__main__":
    main()