import firebase_admin
import discord

from firebase_admin import credentials
from firebase_admin import db

def build_character_embed(character_name, user_id) -> discord.Embed:
    base_ref = db.reference("/users/" + str(user_id))
    character = base_ref.child(character_name).get()

    res = ""
    res += "\nLevel: " + character["lvl"] + " | HP: " + character["hp"] + " | AC: " + character["ac"]
   
    base_attributes = res

    embed_res = discord.Embed(title=character_name, description=res, color=color_for_character(character_name))

    strength =  character["attributes"]["str"] + " | " + calc_modifier(int(character["attributes"]["str"]))
    dexterity = character["attributes"]["dex"] + " | " + calc_modifier(int(character["attributes"]["dex"]))
    constitution = character["attributes"]["con"] + " | " + calc_modifier(int(character["attributes"]["con"]))
    intelligence = character["attributes"]["int"] + " | " + calc_modifier(int(character["attributes"]["int"]))
    wisdom = character["attributes"]["wis"] + " | " + calc_modifier(int(character["attributes"]["wis"]))
    charisma = character["attributes"]["cha"] + " | " + calc_modifier(int(character["attributes"]["cha"]))

    embed_res.add_field(name="Strength", value=strength, inline=True)
    embed_res.add_field(name="Dexterity", value=dexterity, inline=True)
    embed_res.add_field(name="Constitution", value=constitution, inline=True)
    embed_res.add_field(name="Intelligence", value=intelligence, inline=True)
    embed_res.add_field(name="Wisdom", value=wisdom, inline=True)
    embed_res.add_field(name="Charisma", value=charisma, inline=True)

    embed_res = add_additional_properties(embed_res, user_id, character_name)

    return embed_res

def add_additional_properties(embed_res, user_id, character_name):
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/image/").get()
    if (temp_res != None):
        if ("http" not in temp_res and "https" not in temp_res):
            temp_res = "http://" + temp_res
        
        embed_res.set_thumbnail(url=temp_res)

    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/proficiencies/").get()
    if (temp_res != None):
        embed_res.add_field(name="Proficiencies", value=temp_res, inline=False)

    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/race/").get()
    if (temp_res != None):
        embed_res.add_field(name="Race", value=temp_res, inline=True)
    
    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/class/").get()
    if (temp_res != None):
        embed_res.add_field(name="Class", value=temp_res, inline=True)

    temp_res = db.reference("/users/" + str(user_id) + "/" + character_name + "/alignment/").get()
    if (temp_res != None):
        embed_res.add_field(name="Alignment", value=temp_res, inline=False)
    
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

# TODO implement this
def spell_embed(name):
    pass

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
