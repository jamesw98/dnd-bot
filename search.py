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

    query = query.replace("-", " ")

    result_string = "Here's what I found:\n"
    result_string += "```" + query + "```"

    if (json == None):
        sorry_res = "Sorry, but I couldn't find any results for: `" + query + "`"

        if (" " in query):
            sorry_res += "\nTry removing the space"
        return sorry_res

    if (res_type == "spell"):
        result_string += build_spell_string(json)
    elif (res_type == "equipment"):
        result_string += build_equipment_string(json)

    return(result_string)


def build_spell_string(json) -> str:
    result_string = ""
    spell_level = str(json["level"])
    spell_desc = json["desc"]

    result_string += "\nAttributes:"
    result_string += "\n```Level: " + spell_level + " | Range: " + json["range"] + "```\n"
    
    damage_string = ""
    try: 
        damage_string += "Damage:\n"
        if (spell_level != "0"):
            damage_string += "```\nAt base level: " + json["damage"]["damage_at_slot_level"][spell_level] + " | Type: " + json["damage"]["damage_type"]["name"] + "```\n"
        else:
            damage_string += "```\nAt character level 1: " + json["damage"]["damage_at_character_level"]["1"] + " | Type: " + json["damage"]["damage_type"]["name"] + "```\n"

        result_string += damage_string
    except:
        pass

    result_string += "Description:\n```"

    for i in spell_desc:
        result_string += i
        result_string += " "
    
    result_string += "```"
    return result_string

def build_equipment_string(json) -> str:
    result_string = ""
    equip_type = json["equipment_category"]["name"]

    result_string += "Equipment Type: ```" + equip_type + "```"

    if (equip_type == "Armor"):
        result_string += "Attributes: "
        result_string += "\n```Armor Type: " + json["armor_category"] + " | Armor Class: " + str(json["armor_class"]["base"]) + "```"

    elif (equip_type == "Weapon"):
        result_string += "Attributes: "
        result_string += "\n```Weapon Category: " + json["weapon_category"] + " | Range: " + json["weapon_range"] + "```"
        result_string += "Damage:"
        result_string += "\n```Damage Type: " + json["damage"]["damage_type"]["name"] + " | Damage Dice: " + json["damage"]["damage_dice"] + "```"

    return result_string