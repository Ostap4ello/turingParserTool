import json

def load_locale(path: str):
    with open(path) as f:
        return json.load(f)

def print_message(category: str, key: str, locale: dict):
    if category not in locale:
        print("Category not found: %s" % category)
        return
    if key not in locale[category]:
        print("Key not found: %s/%s" % (category, key))
        return
    print(locale[category][key]);
