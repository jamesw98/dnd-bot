from messages import *
import requests as rq

EQUIP_URL = "https://www.dnd5eapi.co/api/equipment"
MI_URL = "https://www.dnd5eapi.co/api/magic-items"
MONSTERS_URL = "https://www.dnd5eapi.co/api/monsters"
SPELLS_URL = "https://www.dnd5eapi.co/api/spells"

def search(query):
    results = None
    res_type = "none"

    if (rq.get(SPELLS_URL + "/" + query).status_code == 200):
        results =  rq.get(SPELLS_URL + "/" + query).json()
        res_type = "spell"
        return [res_type, results]
    
    if (rq.get(MI_URL + "/" + query).status_code == 200):
        results =  rq.get(MI_URL + "/" + query).json()
        res_type = "magicitem"
        return [res_type, results]

    if (rq.get(MONSTERS_URL + "/" + query).status_code == 200):
        results =  rq.get(MONSTERS_URL + "/" + query).json()
        res_type = "monster"
        return [res_type, results]

    if (rq.get(EQUIP_URL + "/" + query).status_code == 200):
        results =  rq.get(EQUIP_URL + "/" + query).json()
        res_type = "equipment"
        return [res_type, results]

    return [None, None]
    
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