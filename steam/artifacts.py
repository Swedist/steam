import os, json
from definitions import ROOT_PATH


class InputData:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'raw_data')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')

    def __init__(self) -> None:
        if not os.listdir(self.INPUT_PATH):
            raise Exception(f"Dir {self.INPUT_PATH} is empty")
    
    def run(self) -> None:
        self.input_data = []
        for file_name in os.listdir(self.INPUT_PATH):
            with open(os.path.join(self.INPUT_PATH, file_name), 'r', encoding='utf-8') as file:
                temp_input_data = json.load(file)
            for elem in temp_input_data:
                self.input_data.append(elem)
        
        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.input_data, file, ensure_ascii=True, indent=4)


class Skins:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'skins.json')

    def __init__(self) -> None:
        if not os.path.isfile(self.INPUT_PATH):
            raise Exception(f"File {self.INPUT_PATH} does not exist")
        
        with open(self.INPUT_PATH, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)
    
    def run(self) -> None:
        self.skins = []
        for elem in self.input_data:
            temp_skin_id = elem['en_full_name']
            if temp_skin_id in self.skins:
                raise Exception(f"Skin {temp_skin_id} already exists")
            self.skins.append(temp_skin_id)
        
        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.skins, file, ensure_ascii=True, indent=4)


class SkinsInfo:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'skins_info.json')

    def __init__(self) -> None:
        if not os.path.isfile(self.INPUT_PATH):
            raise Exception(f"File {self.INPUT_PATH} does not exist")
        
        with open(self.INPUT_PATH, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)
    
    def run(self):
        self.skins_info = {}
        for elem in self.input_data:
            temp_skin_id = elem['en_full_name']
            if temp_skin_id in self.skins_info:
                raise Exception(f"Skin {temp_skin_id} already exists")
            self.skins_info[temp_skin_id] = {
                'ru_full_name': elem['ru_full_name'],
                'en_full_name': elem['en_full_name'],
                'ru_short_name': elem['ru_short_name'],
                'en_short_name': elem['en_short_name'],
                'ru_weapon_name': elem['ru_weapon_name'],
                'en_weapon_name': elem['en_weapon_name'],
                'ru_weapon_type_name': elem['ru_weapon_type_name'],
                'en_weapon_type_name': elem['en_weapon_type_name'],
                'isStatTrak': 'true' if elem['isStatTrak'] else 'false',
                'isSouvenir': 'true' if elem['isSouvenir'] else 'false',
                'ru_quality_name': elem['ru_quality_name'],
                'en_quality_name': elem['en_quality_name'],
                'ru_collection_name': elem['ru_collection_name'],
                'en_collection_name': elem['en_collection_name']
            }
        
        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.skins_info, file, ensure_ascii=True, indent=4)


class SteamDatabase:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'steam_db.json')

    def __init__(self) -> None:
        if not os.path.isfile(self.INPUT_PATH):
            raise Exception(f"File {self.INPUT_PATH} does not exist")
        
        with open(self.INPUT_PATH, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)
    
    def run(self):
        self.steam_db = {}
        for elem in self.input_data:
            temp_skin_id = elem['en_full_name']
            if temp_skin_id in self.steam_db:
                raise Exception(f"Skin {temp_skin_id} already exists")
            
            self.steam_db[temp_skin_id] = {
                'steam_id': elem['steam_id']
            }

        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.steam_db, file, ensure_ascii=True, indent=4)


class CSMoneyDatabase:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'csmoney_db.json')

    def __init__(self) -> None:
        if not os.path.isfile(self.INPUT_PATH):
            raise Exception(f"File {self.INPUT_PATH} does not exist")
        
        with open(self.INPUT_PATH, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)
    
    def run(self):
        self.csmoney_db = {}
        for elem in self.input_data:
            temp_skin_id = elem['en_full_name']
            if temp_skin_id in self.csmoney_db:
                raise Exception(f"Skin {temp_skin_id} already exists")
            
            self.csmoney_db[temp_skin_id] = {
                'csmoney_weapon_alias': elem['csmoney_weapon_alias'],
                'csmoney_weapon_type_alias': elem['csmoney_weapon_type_alias'],
                'csmoney_quality_alias': elem['csmoney_quality_alias'],
                'csmoney_collection_alias': elem['csmoney_collection_alias']
            }

        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.csmoney_db, file, ensure_ascii=True, indent=4)


class UniqueWeapons:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'weapons.json')

    def __init__(self) -> None:
        if not os.path.isfile(self.INPUT_PATH):
            raise Exception(f"File {self.INPUT_PATH} does not exist")
        
        with open(self.INPUT_PATH, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)
    
    def run(self):
        self.weapons = list(set([elem['en_weapon_name'] for elem in self.input_data]))

        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.weapons, file, ensure_ascii=True, indent=4)


class UniqueWeaponTypes:
    INPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'input_data.json')
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'weapon_types.json')

    def __init__(self) -> None:
        if not os.path.isfile(self.INPUT_PATH):
            raise Exception(f"File {self.INPUT_PATH} does not exist")
        
        with open(self.INPUT_PATH, 'r', encoding='utf-8') as file:
            self.input_data = json.load(file)
    
    def run(self):
        self.weapon_types = list(set([elem['en_weapon_type_name'] for elem in self.input_data]))

        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.weapon_types, file, ensure_ascii=True, indent=4)


class Proxies:
    INPUT_DATA = [
        "http://yZ1QYV:H997gs@46.232.11.238:8000",
        "http://QP5BLU:W7Uzgw@176.124.44.67:8000"
    ]
    OUTPUT_PATH = os.path.join(ROOT_PATH, 'artifacts', 'proxies.json')

    def __init__(self) -> None:
        pass

    def run(self):
        with open(self.OUTPUT_PATH, mode='w', encoding='utf-8') as file:
            json.dump(self.INPUT_DATA, file, ensure_ascii=True, indent=4)
