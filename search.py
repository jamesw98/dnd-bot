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

    # checks if the query is a spell
    if (rq.get(SPELLS_URL + "/" + query).status_code == 200):
        results =  rq.get(SPELLS_URL + "/" + query).json()
        res_type = "spell"
        return [res_type, results]
    
    # checks if the query is a magic item
    if (rq.get(MI_URL + "/" + query).status_code == 200):
        results =  rq.get(MI_URL + "/" + query).json()
        res_type = "magicitem"
        return [res_type, results]

    # checks if the query is a monster
    if (rq.get(MONSTERS_URL + "/" + query).status_code == 200):
        results =  rq.get(MONSTERS_URL + "/" + query).json()
        res_type = "monster"
        return [res_type, results]

    # checks if the query is a equipment
    if (rq.get(EQUIP_URL + "/" + query).status_code == 200):
        results =  rq.get(EQUIP_URL + "/" + query).json()
        res_type = "equipment"
        return [res_type, results]

    # no result was found
    return None

# gets the search results and generates the message
def get_search_results(query):
    # searches for the query
    res = search(query.lower())
    
    # couldn't find anything
    if (res == None):
        sorry_res = "Sorry, but I couldn't find any results for: `" + query + "`"

        # give the user some hint about re-searching
        if (" " in query):
            sorry_res += "\nTry removing the space"
        return sorry_res

    # the result type (spell, equipment, monster, or magicitem)
    res_type = res[0]
    # the json object found
    json = res[1]

    # used for better looking printing in the message
    query = query.replace("-", " ")

    result_string = "Here's what I found:\n"
    result_string += "```" + query + "```"

    # gets the formatting for the type we are looking for
    if (res_type == "spell"):
        result_string += build_spell_string(json)
    elif (res_type == "equipment"):
        result_string += build_equipment_string(json)
    elif (res_type == "monster"):
        result_string += build_monster_string(json)
    elif (res_type == "magicitem"):
        result_string += build_magic_item_string(json)

    return(result_string)

### This multi-threaded implementation of this search is actually slightly slower than
### the single threaded version, but it's still neat. 
### Mutlithreading is kind of overkill for this particular situation, but it was 
### interesting to try it out

def search_threaded(query):
    with concurrent.futures.ThreadPoolExecutor() as exe:
        spell_future = exe.submit(search_spells, query)
        magic_item_future = exe.submit(search_magic_items, query)
        monsters_future = exe.submit(search_monsters, query)
        equipment_future = exe.submit(search_equipment, query)

        if (spell_future.result() != None):
            return spell_future.result()

        if (equipment_future.result() != None):
            return equipment_future.result()

        if (magic_item_future.result() != None):
            return magic_item_future.result()

        if (monsters_future.result() != None):
            return monsters_future.result()

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