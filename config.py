from steam.artifacts import (
    InputData,
    Skins,
    SkinsInfo,
    SteamDatabase,
    CSMoneyDatabase,
    UniqueWeapons,
    UniqueWeaponTypes
)

if __name__ == '__main__':
    input_data = InputData()
    input_data.run()

    skins = Skins()
    skins.run()
    
    skins_info = SkinsInfo()
    skins_info.run()
    
    steam_db = SteamDatabase()
    steam_db.run()

    csmoney_db = CSMoneyDatabase()
    csmoney_db.run()
    
    weapons = UniqueWeapons()
    weapons.run()
    
    weapon_types = UniqueWeaponTypes()
    weapon_types.run()
