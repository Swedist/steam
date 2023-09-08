import os
import time
import random
import numpy as np
import multiprocessing as mp
from typing import Dict, Any
from fake_useragent import UserAgent

from definitions import ROOT_PATH
from steam.parsers import CsmoneyPipeline, SteamPipeline
from steam.utils.subs import load_json


def parse_csmoney_skin(name: str, **kwargs: Dict[str, Any]) -> None:

    print(f'Запуск csmoney потока по расчету {name}')
    csmoney_pipeline = CsmoneyPipeline(name=name, **kwargs)
    csmoney_pipeline.run()

    file_name = name.replace(' ', '_') + '.json'
    file_path = os.path.join(csmoney_pipeline.PARSER_OUTPUT_PATH, file_name)
    if os.path.isfile(file_path):
        print(f'SUCCESS: Csmoney поток по расчету {name} успешно выполнился')
    else:
        print(f'ERROR: Csmoney поток по расчету {name} завершился с ошибкой')

def parse_steam_skin(name: str, **kwargs: Dict[str, Any]) -> None:

    print(f'Запуск steam потока по расчету {name}')
    steam_pipeline = SteamPipeline(name=name, **kwargs)
    steam_pipeline.run()

    file_name = name.replace(' ', '_') + '.json'
    file_path = os.path.join(steam_pipeline.PARSER_OUTPUT_PATH, file_name)
    if os.path.isfile(file_path):
        print(f'SUCCESS: Steam поток по расчету {name} успешно выполнился')
    else:
        print(f'ERROR: Steam поток по расчету {name} завершился с ошибкой')

def parse_skin(name: str, kwargs: Dict[str, Any]) -> None:
    parse_csmoney_skin(name=name, **kwargs)
    parse_steam_skin(name=name, **kwargs)
    time.sleep(7)

def main(n_jobs: int):
    unique_skins = load_json(os.path.join(ROOT_PATH, 'artifacts', 'skins.json'))
    proxies = load_json(os.path.join(ROOT_PATH, 'artifacts', 'proxies.json'))
    skins_slice = np.random.choice(unique_skins, 25, replace=False)

    num_proxies = len(proxies)
    user_agent = UserAgent()
    args = [
        (
            name,
            {
                "headers": {
                    'user-agent': user_agent.random
                },
                "proxies": {
                    "https": proxies[i % num_proxies]
                }
            }
        )
        for i, name in enumerate(skins_slice)
    ]
    
    with mp.Pool(processes=n_jobs) as pool:
        pool.starmap(parse_skin, args)

if __name__ == '__main__':
    main(n_jobs=2)
