import firebase_admin
import discord

from firebase_admin import credentials
from firebase_admin import db

SPELL_LEVELS = ["Cantrips", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]

# builds the character embed to send to the user
def build_character_embed(character_name, user_id) -> discord.Embed:
    base_ref = db.reference("/users/" + str(user_id))
    character = base_ref.child(character_name).get()
    
    # base attributes
    res = "\nLevel: " + character["lvl"] + " | HP: " + character["hp"] + " | AC: " + character["ac"]
    
    # builds the base embed
    embed_res = discord.Embed(title=character_name, description=res, color=color_for_character(character_name))

    # gets all the ability score values
    strength =  character["attributes"]["str"] + " | " + calc_modifier(int(character["attributes"]["str"]))
    dexterity = character["attributes"]["dex"] + " | " + calc_modifier(int(character["attributes"]["dex"]))
    constitution = character["attributes"]["con"] + " | " + calc_modifier(int(character["attributes"]["con"]))
    intelligence = character["attributes"]["int"] + " | " + calc_modifier(int(character["attributes"]["int"]))
    wisdom = character["attributes"]["wis"] + " | " + calc_modifier(int(character["attributes"]["wis"]))
    charisma = character["attributes"]["cha"] + " | " + calc_modifier(int(character["attributes"]["cha"]))
    # adds all the ability score values
    embed_res.add_field(name="Strength", value=strength, inline=True)
    embed_res.add_field(name="Dexterity", value=dexterity, inline=True)
    embed_res.add_field(name="Constitution", value=constitution, inline=True)
    embed_res.add_field(name="Intelligence", value=intelligence, inline=True)
    embed_res.add_field(name="Wisdom", value=wisdom, inline=True)
    embed_res.add_field(name="Charisma", value=charisma, inline=True)
    # gets any additional properties
    embed_res = add_additional_properties(embed_res, user_id, character_name)

    return embed_res

# gets additional properties for the character
def add_additional_properties(embed_res, user_id, character_name):
    # checks if there is an image for the character
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/image/").get()
    if (temp_res != None):
        if ("http" not in temp_res and "https" not in temp_res):
            temp_res = "http://" + temp_res
        
        embed_res.set_thumbnail(url=temp_res)

    # checks if the user has set proficiencies
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/proficiencies/").get()
    if (temp_res != None):
        embed_res.add_field(name="Proficiencies", value=temp_res, inline=False)

    # checks if the character has a race
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/race/").get()
    if (temp_res != None):
        embed_res.add_field(name="Race", value=temp_res, inline=True)
    
    # checks if the character has a class
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/class/").get()
    if (temp_res != None):
        embed_res.add_field(name="Class", value=temp_res, inline=True)

    # checks if the character has a alignment
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/alignment/").get()
    if (temp_res != None):
        embed_res.add_field(name="Alignment", value=temp_res, inline=False)
    
    # checks if the character has money
    money_types = ["platinum", "gold", "silver", "copper"]
    money_types_for_printing = ["Platinum", "Gold", "Silver", "Copper"]
    money_res = ""

    money_found = False

    c = 0
    for money in money_types:
        temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/" + money + "/").get()
        if (temp_res != None):
            money_found = True
            money_res += money_types_for_printing[c] + ": " + temp_res + "\n"
        c += 1

    if (money_found):
        embed_res.add_field(name="Money", value=money_res, inline=False)

    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/description/").get()
    if (temp_res != None):
        embed_res.add_field(name="Description", value="```" + temp_res + "```", inline=False)

    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/notes/").get()
    if (temp_res != None):
        embed_res.add_field(name="Notes", value="```" + temp_res + "```", inline=False)

    return embed_res

# builds spellbook embed 
def build_spellbook_embed(character_name, user_id):
    base_ref = db.reference("/users/" + str(user_id))
    character_spells = "Spells for " + character_name

    embed_res = discord.Embed(title=character_spells, color=color_for_character(character_name))
    
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/image/").get()
    if (temp_res != None):
        if ("http" not in temp_res and "https" not in temp_res):
            temp_res = "http://" + temp_res
        
        embed_res.set_thumbnail(url=temp_res)
    
    for level in SPELL_LEVELS:
        spells_for_level = base_ref.child(character_name).child("spells").child(level).get()
        if (spells_for_level != "empty"):
            res_string = ""
            count = 0
            for spell in spells_for_level:
                res_string += spell

                if (count != len(spells_for_level) - 1):
                    res_string += ", "

                count += 1

            embed_res.add_field(name=level, value=res_string, inline=False)
    
    return embed_res

def build_spell_embed(json):
    spell_level = str(json["level"])
    spell_desc = json["desc"]

    embed_res = discord.Embed(title="Search Results", description="Result Type: Spell", color=color_for_character("spell"))

    embed_res.add_field(name="Spell Level", value=str(json["level"]), inline=True)
    embed_res.add_field(name="Range", value=json["range"], inline=True)

    try:
        if (spell_level != "0"):
            embed_res.add_field(name="Damage at Base Level", value=json["damage"]["damage_at_slot_level"][spell_level], inline=False)
        else:
            embed_res.add_field(name="Damange at Level 1", value=json["damage"]["damage_at_character_level"]["1"])
        
        embed_res.add_field(name="Damage Type", value=json["damage"]["damage_type"]["name"], inline=True)
    except:
        pass

    desc_res = ""
    for i in spell_desc:
        desc_res += i + " "

    embed_res.add_field(name="Description", value=desc_res, inline=False)

    return embed_res

def build_equipment_embed(json):
    embed_res = discord.Embed(title="Search Results", description="Result Type: Equipment", color=color_for_character("equipment"))

    equip_type = json["equipment_category"]["name"]

    embed_res.add_field(name="Equipment Type", value=equip_type, inline=False)
    
    if (equip_type == "Armor"):
        embed_res.add_field(name="Armor Type", value=json["armor_category"], inline=True)
        embed_res.add_field(name="Armor Class", value=str(json["armor_class"]["base"]), inline=True)
    elif (equip_type == "Weapon"):
        embed_res.add_field(name="Damage Type", value=json["damage"]["damage_type"]["name"], inline=True)
        embed_res.add_field(name="Damage Dice", value=json["damage"]["damage_dice"], inline=True)

    return embed_res

def build_monster_embed(json):
    embed_res = discord.Embed(title="Search Results", description="Result Type: Monster", color=color_for_character("monster"))

    embed_res.add_field(name="Size", value=json["size"], inline=True)
    embed_res.add_field(name="Type", value=json["type"], inline=True)
    embed_res.add_field(name="Speed", value=json["speed"]["walk"], inline=True)

    embed_res.add_field(name="Armor Class", value=str(json["armor_class"]), inline=False)
    embed_res.add_field(name="Hit Points", value= str(json["hit_points"]), inline=True)
    embed_res.add_field(name="Hit Dice", value= json["hit_dice"], inline=True)
    
    return  embed_res

def build_magic_item_embed(json):
    item_desc = json["desc"]
    item_name = json["name"]
    embed_res = discord.Embed(title="Search Results", description="Result Type: Magic Item", color=color_for_character("magic item"))

    embed_res.add_field(name="Name", value=item_name, inline=False)

    desc_res = item_desc[0] + " " + item_desc[1] + "..."
        
    embed_res.add_field(name="Description", value=desc_res, inline=False)

    link = "https://roll20.net/compendium/dnd5e/" + item_name.replace(" ", "%20") + "#content"

    embed_res.add_field(name="Link", value=link, inline=False)
    
    return embed_res


def color_for_character(name):
    hash = 0
    for i in range(len(name)):
        hash = ord(name[0]) + ((hash << 5) - hash)
    
    return hash & 0x00FFFFFF

def calc_modifier(score) -> str:
    mod = (score//2) - 5
    
    if (mod > 0):
        return "+" + str(mod)
    else:
        return " " + str(mod)
