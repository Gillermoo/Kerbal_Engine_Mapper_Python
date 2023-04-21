from Engine import Engine
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
    Engine.setupEngines(allowedEngines)

if __name__ == "__main__":
    main()

