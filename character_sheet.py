import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from messages import build_character_message

ERROR_CHARACTER_EXISTS = "You already have a character with that name in your database"

INVALID_FORMAT_VIEW = "Invalid formatting, you didn't enter a name"
INVALID_FORMAT_ADD = "Invalid formatting, make add matches the below formatting:\n```!dnd character add name level,hp,ac attributes (str, dex, con, int, wis, cha)``````!dnd character add Volo 3,25,13 8,10,16,18,13,20```"
INVALID_FORMAT_SET = "Invalid formatting, make add matches the below formatting:\n```!dnd character [character name] set [property name] [property]``````!dnd character Rich set image bit.ly/2L2kvgV```"
INVALID_FORMAT_ADD_BASE_ATTR = "Invalid formatting, something went wrong in your level,hp,ac fields"
INVALID_FORMAT_ADD_STATS = "Invalid formatting, something went wrong in your stats fields"

VALID_PROPERTIES = ["image", "notes", "description", "alignment", "copper", "silver", "gold", "platinum"]

cred = credentials.Certificate("secret/dnd-discord-bot-66966-firebase-adminsdk-pncqe-3815ee866c.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://dnd-discord-bot-66966.firebaseio.com/"})

# parses the character command
def character_parse(cmd_list, author):
    if (cmd_list[0] == "add" or cmd_list[0] == "a"):
        return create_character_for_user(cmd_list[1:], author)
    elif (cmd_list[0] == "view" or cmd_list[0] == "v"):
        return view_character(cmd_list[1:], author)
    elif (len(cmd_list) > 2 and (cmd_list[1] == "set" or cmd_list[1] == "s")):
        return set_character_property(cmd_list[1:], author)
    elif (cmd_list[0] == "list"):
        return list_helper(cmd_list[1:], author)

def list_helper(cmd_list, author):
    if (len(cmd_list) == 0):
        # print(db.reference("/users/" + str(author.id)).get().keys())
        return "Here are your characters: " + build_character_list_message(db.reference("/users/" + str(author.id)).get().keys())
        pass
    elif (cmd_list[0] == "properties" or cmd_list[0] == "props"):
        return "Available Properties:\n" + build_property_message()

def create_character_for_user(cmd_list, author):
    if (len(cmd_list) != 3):
        return INVALID_FORMAT_ADD

    char_name = cmd_list[0]

    base_ref = db.reference("/users/" + str(author.id))

    if (base_ref.child(char_name).get() != None):
        return ERROR_CHARACTER_EXISTS

    if (len(cmd_list[1].split(",")) != 3):
        return INVALID_FORMAT_ADD_BASE_ATTR

    char_lvl = str(cmd_list[1].split(",")[0])
    char_hp =  str(cmd_list[1].split(",")[1])
    char_ac =  str(cmd_list[1].split(",")[2])

    if (len(cmd_list[2].split(",")) != 6):
        return INVALID_FORMAT_ADD_STATS
    
    char_str = str(cmd_list[2].split(",")[0])
    char_dex = str(cmd_list[2].split(",")[1])
    char_con = str(cmd_list[2].split(",")[2])
    char_int = str(cmd_list[2].split(",")[3])
    char_wis = str(cmd_list[2].split(",")[4])
    char_cha = str(cmd_list[2].split(",")[5])

    base_ref.child(char_name).set({
        "name":char_name,
            "lvl":char_lvl,
            "ac":char_ac,
            "hp":char_hp,
            "attributes":{
                "str":char_str,
                "dex":char_dex,
                "con":char_con,
                "int":char_int,
                "wis":char_wis,
                "cha":char_cha
            }
    })

    return "Success! Character added!\n" + build_character_message(char_name, author.id)

def set_character_property(cmd_list, author):
    if (len(cmd_list) != 4):
        return INVALID_FORMAT_SET

def view_character(cmd_list, author):
    if (len(cmd_list) < 1):
        return INVALID_FORMAT_VIEW
    return build_character_message(cmd_list[0], author.id)

def build_property_message():
    c = 0
    res = "```"
    for i in VALID_PROPERTIES:
        if (c != len(VALID_PROPERTIES) - 1):
            res += i + ", "
        else:
            res += i
        c += 1
    res += "```"
    return res

def build_character_list_message(char_list):
    c = 0
    res = "```"
    for i in char_list:
        if (c != len(char_list) - 1):
            res += i + ", "
        else:
            res += i
        c += 1
    res += "```"
    return res
