import os
import time
import numpy as np
import multiprocessing as mp

from definitions import ROOT_PATH
from steam.parsers import BaseParser, CsmoneyParser, SteamParser
from steam.utils.subs import load_json

# csmoney_parser = CsmoneyParser(name='...')
# csmoney_parser.run()
# csmoney_parser.save()

# steam_parser = SteamParser(name='...')
# steam_parser.run()
# steam_parser.save()

def func(i, skin_name):
    print(f'Запуск потока №{i + 1}')

    csmoney_parser = CsmoneyParser(name=skin_name)
    csmoney_parser.run()
    csmoney_parser.save()

    steam_parser = SteamParser(name=skin_name)
    steam_parser.run()
    steam_parser.save()

    print(f'Поток №{i + 1} выполнился.')

unique_skins = load_json(os.path.join('artifacts', 'skins.json'))
sample_unique_skins = np.random.choice(unique_skins, 10, replace=False)

if __name__ == '__main__':
    with mp.Pool(5) as pool:
        pool.starmap(func, enumerate(sample_unique_skins))
