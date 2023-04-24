from Engine import Engine
from FuelTank import FuelTank
from RocketStage import LinerStage

def main():
    RS = LinerStage.optimize_plot([.01, 100], [100, 10000], 100, 4, 'vac', 1)


if __name__ == "__main__":
    main()

