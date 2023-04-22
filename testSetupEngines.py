from Engine import Engine
from FuelTank import FuelTank
import pandas as pd

def main():
    allowedEngines = {
    'Spider'        :True,
    'Twitch'        :True,
    'Thud'          :True,
    'Ant'           :True,
    'Spark'         :True,
    'Terrier'       :True,
    'Reliant'       :True,
    'Swivel'        :True,
    'Vector'        :True,
    'Dart'          :True,
    'Nerv'          :True,
    'Poodle'        :True,
    'Skipper'       :True,
    'Mainsail'      :True,
    'Twin-Boar'     :True,
    'Rhino'         :True,
    'Mammoth'       :True,
    'R.A.P.I.E.R.'  :True,
    'Dawn'          :True,
    'Mastodon'      :True,
    'Cheetah'       :True,
    'Bobcat'        :True,
    'Skiff'         :True,
    'Wolfhound'     :True,
    'Kodiak'        :True,
    'Cub'           :True,
    'Flea'          :True,
    'Hammer'        :True,
    'Thumper'       :True,
    'Kickback'      :True,
    'Sepratron I'   :True,
    'Shrimp'        :True,
    'Mite'          :True,
    'Thoroughbred'  :True,
    'Clydesdale'    :True,
    'Pullox'        :True}
    engines = Engine.setupEngines(allowedEngines)
    tanks = FuelTank()
    tanks.best_cost_per_ton_structure(500, 'LF')


if __name__ == "__main__":
    main()
