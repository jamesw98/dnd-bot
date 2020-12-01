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

def  build_monster_string(json) -> str:
    result_string = ""
    
    result_string += "Attributes:"
    result_string += "\n```Size: " + json["size"] + " | Type: " + json["type"] + " | Speed: " + json["speed"]["walk"]
    result_string += "\nArmor Class: " + str(json["armor_class"]) + " | Hit Points: " + str(json["hit_points"]) + " | Hit Dice: " + json["hit_dice"] + "```"

    return result_string

def build_magic_item_string(json) -> str:
    result_string = ""
    item_desc = json["desc"]

    result_string += "Description:"
    result_string += "\n```"

    for i in item_desc:
        result_string += i
        result_string += " "

    result_string += "```"
    
    return result_string 