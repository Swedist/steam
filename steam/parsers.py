import os
import json
import requests
import random
import time
from typing import Dict, Any

from definitions import ROOT_PATH
from steam.utils.subs import load_json


# load artifacts
skins_info = load_json(file_path=os.path.join(ROOT_PATH, 'artifacts', 'skins_info.json'))
csmoney_db = load_json(file_path=os.path.join(ROOT_PATH, 'artifacts', 'csmoney_db.json'))
steam_db = load_json(file_path=os.path.join(ROOT_PATH, 'artifacts', 'steam_db.json'))


class BaseParser:

    # inside params
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'output')
    PARSER_OUTPUT_PATH = None

    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        self.name = name

        if "headers" in kwargs:
            self.headers = kwargs["headers"]
        else:
            self.headers = None
        
        if "proxies" in kwargs:
            self.proxies = kwargs["proxies"]
        else:
            self.proxies = None
    
    def run(self) -> None:
        raise NotImplementedError('This is a parent class')

    def save(self) -> None:
        raise NotImplementedError('This is a parent class')


class CsmoneyParser(BaseParser):

    # inside params
    URL = "https://cs.money/1.0/market/sell-orders?"
    PARSER_OUTPUT_PATH = os.path.join(BaseParser.OUTPUT_PATH, 'temp_csmoney')
    
    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        super().__init__(name=name, **kwargs)
    
    @classmethod
    def _create_href(cls, **kwargs: Dict[str, Any]) -> str:
        return cls.URL + '&'.join([f"{elem[0]}={elem[1]}" for elem in list(kwargs.items())])
    
    @classmethod
    def _create_response(cls, **kwargs: Dict[str, Any]) -> Any:
        return requests.get(**kwargs)
    
    def _create_request(self, **kwargs: Dict[str, Any]) -> Any:
        repeats = 2
        while repeats:
            response = self._create_response(**kwargs)
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

    def _run(self) -> Dict[str, Any]:
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
                items = self._create_request(url=temp_url, headers=self.headers, proxies=self.proxies)

                temp_result = list(map(
                    lambda elem: self._csmoney_skin_parser(item=elem),
                    items
                )) if items else []
                self.result += temp_result
                offset += batch_size
            
            if len(temp_result) < 60:
                break
        
    def _save(self) -> None:
        if not bool(self.result):
            return None
        
        os.makedirs(self.PARSER_OUTPUT_PATH, exist_ok=True)
        file_name = self.name.replace(' ', '_') + '.json'
        self.result = sorted(self.result, key=lambda elem: elem['price']['computed_price'])
        with open(os.path.join(self.PARSER_OUTPUT_PATH, file_name), mode='w', encoding='utf-8') as file:
            json.dump(self.result, file)


class CsmoneyPipeline(CsmoneyParser):

    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        super().__init__(name=name, **kwargs)
    
    def run(self):
        self._run()
        self._save()


class SteamParser(BaseParser):

    # inside params
    URL = "https://steamcommunity.com/market/itemordershistogram?country=EN&language=english&currency=1&item_nameid={steam_item_id}&two_factor=0"
    PARSER_OUTPUT_PATH = os.path.join(BaseParser.OUTPUT_PATH, 'temp_steam')
    
    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        super().__init__(name=name, **kwargs)
    
    @classmethod
    def _create_href(cls, **kwargs):
        return cls.URL.format(**kwargs)

    @classmethod
    def _create_response(cls, **kwargs: Dict[str, Any]) -> Any:
        return requests.get(**kwargs)
    
    def _create_request(self, **kwargs: Dict[str, Any]) -> Any:
        repeats = 2
        while repeats:
            response = self._create_response(**kwargs)
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

    def _run(self) -> Dict[str, Any]:
        url_params = {
            "steam_item_id": steam_db[self.name]['steam_id']
        }
        url = self._create_href(**url_params)
        items = self._create_request(url=url, headers=self.headers, proxies=self.proxies)
        self.result = list(map(
            lambda elem: self._steam_skin_parser(item=elem),
            items
        )) if items else []
    
    def _save(self) -> None:
        if not bool(self.result):
            return None

        os.makedirs(self.PARSER_OUTPUT_PATH, exist_ok=True)
        file_name = self.name.replace(' ', '_') + '.json'
        with open(os.path.join(self.PARSER_OUTPUT_PATH, file_name), mode='w', encoding='utf-8') as file:
            json.dump(self.result, file)


class SteamPipeline(SteamParser):

    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        super().__init__(name=name, **kwargs)
    
    def run(self):
        self._run()
        self._save()
