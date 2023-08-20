import os
import json
import requests
import random
import time
from typing import Dict, Any
from fake_useragent import UserAgent

from definitions import ROOT_PATH


# load artifacts
with open(os.path.join(ROOT_PATH, 'artifacts', 'csmoney_db.json'), mode='r', encoding='utf-8') as file:
    csmoney_db = json.load(file)

with open(os.path.join(ROOT_PATH, 'artifacts', 'skins_info.json'), mode='r', encoding='utf-8') as file:
    skins_info = json.load(file)

with open(os.path.join(ROOT_PATH, 'artifacts', 'steam_db.json'), mode='r', encoding='utf-8') as file:
    steam_db = json.load(file)

with open(os.path.join(ROOT_PATH, 'artifacts', 'skins.json'), mode='r', encoding='utf-8') as file:
    unique_skins = json.load(file)

with open(os.path.join(ROOT_PATH, 'artifacts', 'weapon_types.json'), mode='r', encoding='utf-8') as file:
    unqiue_weapon_types = json.load(file)

with open(os.path.join(ROOT_PATH, 'artifacts', 'weapons.json'), mode='r', encoding='utf-8') as file:
    unqiue_weapons = json.load(file)


class BaseParser:

    # inside params
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'output')
    PARSER_OUTPUT_PATH = None

    # outside params
    USER_AGENT = UserAgent()
    PROXIES = {
        "https": "http://yZ1QYV:H997gs@46.232.11.238:8000"
    }

    def __init__(self, name: str = None) -> None:
        self.name = name
    
    def run(self) -> None:
        raise NotImplementedError('This is a parent class')

    def save(self) -> None:
        raise NotImplementedError('This is a parent class')


class CsmoneyParser(BaseParser):

    # inside params
    URL = "https://cs.money/1.0/market/sell-orders?"
    PARSER_OUTPUT_PATH = os.path.join(BaseParser.OUTPUT_PATH, 'csmoney')
    
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
    
    @classmethod
    def _create_href(cls, *args, **kwargs) -> str:
        return cls.URL + '&'.join([f"{elem[0]}={elem[1]}" for elem in list(kwargs.items())])
    
    @classmethod
    def _create_response(cls, url: str) -> Any:
        return requests.get(
            url=url,
            headers={
                'user-agent': cls.USER_AGENT.random
            },
            proxies=cls.PROXIES
        )
    
    def create_request(self, url: str) -> None:
        repeats = 5
        while repeats:
            response = self._create_response(url=url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    items = data.get('items')
                    return items
            else:
                repeats -= 1
                time.sleep(random.randint(2, 6))
                continue
        return None
    
    @classmethod
    def _csmoney_skin_parser(cls, item: Dict[str, Any]) -> Dict[str, Any]:

        # get item screenshot
        item_screenshot = item.get('asset', {}).get('images', {}).get('screenshot', None)

        # get item floar
        item_float = item.get('asset', {}).get('float', None)

        # get item prices
        item_price = {
            'default': item.get('pricing', {}).get('default', None),
            'extra_price': sum(list(item.get('pricing', {}).get('extra', {}).values())) if bool(item.get('pricing', {}).get('extra', {})) else 0,
            'price_before_discount': item.get('pricing', {}).get('priceBeforeDiscount', None),
            'discount': item.get('pricing', {}).get('discount', None),
            'computed_price': item.get('pricing', {}).get('computed', None)
        }
        
        # get item stickers:
        item_stickers = []
        if bool(item.get('stickers')):
            for temp_sticker in item.get('stickers'):
                if bool(temp_sticker):
                    item_stickers.append(
                        {
                            'name': temp_sticker.get('name', None),
                            'wear': temp_sticker.get('wear', None),
                            'collection': temp_sticker.get('collection', {}).get('name', None),
                            'price': temp_sticker.get('pricing', {}).get('default', None),
                            'rarity': temp_sticker.get('pricing', {}).get('rarity', None)
                        }
                    )
                else:
                    item_stickers.append(None)

        return {
            'screenshot': item_screenshot,
            'float': item_float,
            'price': item_price,
            'stickers': item_stickers
        }

    def run(self) -> Dict[str, Any]:
        short_name = skins_info[self.name]['en_short_name']
        quality_alias = csmoney_db[self.name]['csmoney_quality_alias']
        isStatTrak = skins_info[self.name]['isStatTrak']
        isSouvenir = skins_info[self.name]['isSouvenir']
        offset = 0
        batch_size = 60
        self.result = []
        while True:
            for item in range(offset, offset + batch_size, 60):
                temp_url_params = {
                    "limit": 60,
                    "offset": item,
                    "name": short_name,
                    "quality": quality_alias,
                    "isStatTrak": isStatTrak,
                    "isSouvenir": isSouvenir
                }
                temp_url = self._create_href(**temp_url_params)
                items = self.create_request(url=temp_url)

                temp_result = list(map(
                    lambda elem: self._csmoney_skin_parser(item=elem),
                    items
                )) if items else []
                self.result += temp_result
                offset += batch_size
            
            if len(temp_result) < 60:
                break
        
    def save(self) -> None:
        if not bool(self.result):
            return None
        
        os.makedirs(self.PARSER_OUTPUT_PATH, exist_ok=True)
        file_name = self.name.replace(' ', '_') + '.json'
        self.result = sorted(self.result, key=lambda elem: elem['price']['computed_price'])
        with open(os.path.join(self.PARSER_OUTPUT_PATH, file_name), mode='w', encoding='utf-8') as file:
            json.dump(self.result, file)


class SteamParser(BaseParser):

    # inside params
    URL = "https://steamcommunity.com/market/itemordershistogram?country=EN&language=english&currency=1&item_nameid={steam_item_id}&two_factor=0"
    PARSER_OUTPUT_PATH = os.path.join(BaseParser.OUTPUT_PATH, 'steam')
    
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
    
    @classmethod
    def _create_href(cls, *args, **kwargs):
        return cls.URL.format(**kwargs)

    @classmethod
    def _create_response(cls, url: str) -> Any:
        return requests.get(
            url=url,
            headers={
                'user-agent': cls.USER_AGENT.random
            },
            proxies=cls.PROXIES
        )
    
    def create_request(self, url: str) -> None:
        repeats = 5
        while repeats:
            response = self._create_response(url=url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    items = data.get('sell_order_graph')
                    return items
            else:
                repeats -= 1
                time.sleep(random.randint(2, 6))
                continue
        return None
    
    @classmethod
    def _steam_skin_parser(cls, item: Dict[str, Any]) -> Dict[str, Any]:

        # get item price
        item_price = {
            'computed_price': item[0]
        }

        return {
            'price': item_price
        }

    def run(self) -> Dict[str, Any]:
        url_params = {
            "steam_item_id": steam_db[self.name]['steam_id']
        }
        url = self._create_href(**url_params)
        items = self.create_request(url=url)
        self.result = list(map(
            lambda elem: self._steam_skin_parser(item=elem),
            items
        )) if items else []
    
    def save(self) -> None:
        if not bool(self.result):
            return None

        os.makedirs(self.PARSER_OUTPUT_PATH, exist_ok=True)
        file_name = self.name.replace(' ', '_') + '.json'
        with open(os.path.join(self.PARSER_OUTPUT_PATH, file_name), mode='w', encoding='utf-8') as file:
            json.dump(self.result, file)
