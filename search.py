import requests as rq
import concurrent.futures

from messages import *

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

    return None

def get_search_results(query):
    res = search(query.lower())
    
    if (res == None):
        sorry_res = "Sorry, but I couldn't find any results for: `" + query + "`"

        if (" " in query):
            sorry_res += "\nTry removing the space"
        return sorry_res

    res_type = res[0]
    json = res[1]

    query = query.replace("-", " ")

    result_string = "Here's what I found:\n"
    result_string += "```" + query + "```"


    if (res_type == "spell"):
        result_string += build_spell_string(json)
    elif (res_type == "equipment"):
        result_string += build_equipment_string(json)

    return(result_string)

### This multi threaded implementation of this search is actually slightly slower than
### the single threaded version, but it's still neat. 
### If there was an O(1) way to check the futures, it would most likely be faster
### or maybe a different pool implementation?

def search_threaded(query):
    with concurrent.futures.ThreadPoolExecutor() as exe:
        spell_future = exe.submit(search_spells, query)
        magic_item_future = exe.submit(search_magic_items, query)
        monsters_future = exe.submit(search_monsters, query)
        equipment_future = exe.submit(search_equipment, query)

        for future in [spell_future, magic_item_future, monsters_future, equipment_future]:
            if (future != None):
                return future.result()

        return None

def search_spells(query):
    results = None
    res_type = "none"

    if (rq.get(SPELLS_URL + "/" + query).status_code == 200):
        results =  rq.get(SPELLS_URL + "/" + query).json()
        res_type = "spell"
        return [res_type, results]
    
    return None

def search_magic_items(query):
    if (rq.get(MI_URL + "/" + query).status_code == 200):
        results =  rq.get(MI_URL + "/" + query).json()
        res_type = "magicitem"
        return [res_type, results] 

    return None

def search_monsters(query):
    if (rq.get(MONSTERS_URL + "/" + query).status_code == 200):
        results =  rq.get(MONSTERS_URL + "/" + query).json()
        res_type = "monster"
        return [res_type, results]
    
    return None

def search_equipment(query):
    if (rq.get(EQUIP_URL + "/" + query).status_code == 200):
        results =  rq.get(EQUIP_URL + "/" + query).json()
        res_type = "equipment"
        return [res_type, results]

    return None