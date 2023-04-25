from Engine import Engine
from FuelTank import FuelTank
from RocketStage import LinerStage

def main():
    RS = LinerStage.optimize_point(10, 3000, 4, 'asl', 1.5, 'cost')


if __name__ == "__main__":
    main()

