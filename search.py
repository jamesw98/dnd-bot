import requests as rq

EQUIP_URL = "https://www.dnd5eapi.co/api/equipment"
MI_URL = "https://www.dnd5eapi.co/api/magic-items"
MONSTERS_URL = "https://www.dnd5eapi.co/api/monsters"
SPELLS_URL = "https://www.dnd5eapi.co/api/spells"

def search(query):
    results = None
    res_type = "none"

    try:
        rq.get(SPELLS_URL + "/" + query).json()['index']
        results =  rq.get(SPELLS_URL + "/" + query).json()
        res_type = "spell"
    except:
        pass

    try:
        rq.get(MI_URL + "/" + query).json()['index']
        results =  rq.get(MI_URL + "/" + query).json()
        res_type = "magicitem"
    except:
        pass

    try:
        rq.get(MONSTERS_URL + "/" + query).json()['index']
        results =  rq.get(MONSTERS_URL + "/" + query).json()
        res_type = "monster"
    except:
        pass

    try:
        rq.get(EQUIP_URL + "/" + query).json()['index']
        results =  rq.get(EQUIP_URL + "/" + query).json()
        res_type = "equipment"
    except:
        pass
    
    return [res_type, results]


def get_search_results(query):
    res = search(query.lower())

    res_type = res[0]
    json = res[1]

    result_string = "Here's what I found:\n"

    query = query.replace("-", " ")

    if (json == None):
        return "Sorry, but I couldn't find any results for: `" + query + "`"

    if (res_type == "spell"):
        result_string += build_spell_string(json, query)

    return(result_string)


def build_spell_string(json, query) -> str:
    result_string = ""
    spell_level = str(json["level"])
    spell_desc = json["desc"]

    result_string += "```" + query + "```\nBase Attributes:"
    result_string += "\n```Level: " + spell_level + " | Range: " + json["range"] + "```\n"
    result_string += "Damage:\n"
    if (spell_level != "0"):
        result_string += "```\nAt base level: " + json["damage"]["damage_at_slot_level"][spell_level] + " | Type: " + json["damage"]["damage_type"]["name"] + "```\n"
    else:
        result_string += "```\nAt character level 1: " + json["damage"]["damage_at_character_level"]["1"] + " | Type: " + json["damage"]["damage_type"]["name"] + "```\n"
    result_string += "Description:\n```"

    for i in spell_desc:
        result_string += i
        result_string += " "
    
    result_string += "```"
    return result_string
