# Здесь я расскажу как мы парсим и некоторые нюансы

## Нюансы
- Формат файла - .json
- Соблюдайте табуляцию
- Добавление лишнего пробела все сломает
- Название файла - название коллекции, где пробелы заменены на знак "_" и все буквы переведены в нижний регистр, например "the_bank_collection.json"
- Не забывайте, что оружия разного качества - это разные оружия

## Как парсим
- Заходим на сайт https://www.csgodatabase.com
- Ищем нужную коллекцию

### Пример 1 оружия

[
    {
        "steam_id": 8987895,
        "ru_full_name": "SG 553 | Армейский блеск (Прямо с завода)",
        "en_full_name": "SG 553 | Army Sheen (Factory New)",
        "ru_short_name": "SG 553 | Армейский блеск",
        "en_short_name": "SG 553 | Army Sheen",
        "ru_weapon_name": "SG 553",
        "en_weapon_name": "SG 553",
        "csmoney_weapon_alias": "SG 553",
        "ru_weapon_type_name": "Штурмовые винтовки",
        "en_weapon_type_name": "Assault Rifles",
        "csmoney_weapon_type_alias": 3,
        "isStatTrak": false,
        "isSouvenir": false,
        "ru_quality_name": "Прямо с завода",
        "en_quality_name": "Factory New",
        "csmoney_quality_alias": "fn",
        "ru_collection_name": "Коллекция «Bank»",
        "en_collection_name": "The Bank Collection",
        "csmoney_collection_alias": "The Bank Collection"
    },
    {
        ...
    }
]

### 1. steam_id
- Подтягивается из steam, например 8987895

### 2. ru_full_name
- Подтягивается из steam, например "SG 553 | Армейский блеск (Прямо с завода)"

### 3. en_full_name
- Подтягивается из steam, например "SG 553 | Army Sheen (Factory New)"

### 4. ru_short_name
- Подтягивается из steam, например "SG 553 | Армейский блеск"
- Берем из п.2

### 5. en_short_name
- Подтягивается из steam, например "SG 553 | Army Sheen"
- Берем из п.3

### 6. ru_weapon_name
- Подтягивается из steam, например "SG 553"
- Берем из п.2

### 7. en_weapon_name
- Подтягивается из steam, например "SG 553"
- Берем из п.3

### 8. csmoney_weapon_alias
- Подтягивается из steam, например "SG 553"
- Берем из п.7
- Чаще всего будет английское название оружия

### 9. ru_weapon_type_name
- Подтягивается с сайта csmoney, например "Штурмовые винтовки"

### 10. en_weapon_type_name
- Подтягивается с сайта csmoney, например "Assault Rifles"

### 11. csmoney_weapon_type_alias
- Подтягивается с сайта csmoney, например 3

### 12. isStatTrak
- Принимает 2 значения - true/false
- Если в названии есть StatTrak - значит true

### 13. isSouvenir
- Принимает 2 значения - true/false
- Если в названии есть Souvenir - значит true

### 14. ru_quality_name
- Берем из п.2, например "Прямо с завода"

### 15. en_quality_name
- Берем из п.3, например "Factory New"

### 16. csmoney_quality_alias
- Подтягивается с сайта csmoney, например "fn"

### 17. ru_collection_name
- Подтягивается из steam, например "Коллекция «Bank»"

### 18. en_collection_name
- Подтягивается из steam, например "The Bank Collection"

### 19. csmoney_collection_alias
- Подтягивается из csmoney, например "The Bank Collection"
- Берем из п.18
- Чаще всего будет английское название оружия







