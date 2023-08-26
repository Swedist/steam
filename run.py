import os
import time
import random
import multiprocessing as mp
from typing import Dict, Any

from definitions import ROOT_PATH
from steam.parsers import CsmoneyPipeline, SteamPipeline
from steam.utils.subs import load_json


def parse_csmoney_skin(name: str, **kwargs: Dict[str, Any]) -> None:
    print(f'Запуск csmoney потока по расчету {name}')
    csmoney_pipeline = CsmoneyPipeline(name=name, **kwargs)
    csmoney_pipeline.run()



# def create_csmoney_pipeline(name: str) -> None:
#     print(f'Запуск csmoney потока по расчету {name}')

#     csmoney_pipeline = CsmoneyPipeline(name=name)
#     csmoney_pipeline.run()

#     file_name = name.replace(' ', '_') + '.json'
#     file_path = os.path.join(csmoney_pipeline.PARSER_OUTPUT_PATH, file_name)

#     if os.path.isfile(file_path):
#         print(f'SUCCESS: Csmoney поток по расчету {name} успешно выполнился')
#     else:
#         print(f'ERROR: Csmoney поток по расчету {name} завершился с ошибкой')

# def create_steam_pipeline(name: str) -> None:
#     print(f'Запуск steam потока по расчету {name}')

#     steam_pipeline = SteamPipeline(name=name)
#     steam_pipeline.run()

#     file_name = name.replace(' ', '_') + '.json'
#     file_path = os.path.join(steam_pipeline.PARSER_OUTPUT_PATH, file_name)

#     if os.path.isfile(file_path):
#         print(f'SUCCESS: Steam поток по расчету {name} успешно выполнился')
#     else:
#         print(f'ERROR: Steam поток по расчету {name} завершился с ошибкой')

# def main(n_jobs: int) -> None:
#     unique_skins = load_json(os.path.join('artifacts', 'skins.json'))
#     skins_info = load_json(os.path.join('artifacts', 'skins_info.json'))
#     parsed_skins = [elem for elem in unique_skins if skins_info[elem]['en_collection_name'] == 'The Operation Hydra Collection'][3:5]

#     with mp.Pool(processes=n_jobs) as pool:

#         csmoney_flow = pool.map_async(create_csmoney_pipeline, parsed_skins)
#         steam_flow = pool.map_async(create_steam_pipeline, parsed_skins)

#         csmoney_flow.wait()
#         steam_flow.wait()

#     print(f'Все потоки завершились')

# if __name__ == '__main__':
#     main(n_jobs=2)
