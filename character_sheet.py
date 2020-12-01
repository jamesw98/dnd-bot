import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

ERROR_CHARACTER_EXISTS = "You already have a character with that name in your database"

INVALID_FORMAT_ADD = "Invalid formatting, make add matches the below formatting:\n```!dnd character add name level,hp,ac attributes (str, dex, con, int, wis, cha)``````!dnd character add Volo 3,25,13 8,10,16,18,13,20```"
INVALID_FORMAT_ADD_BASE_ATTR = "Invalid formatting, something went wrong in your level,hp,ac fields"
INVALID_FORMAT_ADD_STATS = "Invalid formatting, something went wrong in your stats fields"

key = os.getenv("FIREBASE_KEY")

cred = credentials.Certificate("secret/dnd-discord-bot-66966-firebase-adminsdk-pncqe-3815ee866c.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://dnd-discord-bot-66966.firebaseio.com/"})

def character_parse(cmd_list, author):
    if (cmd_list[0] == "add" or cmd_list[0] == "a"):
        return create_character_for_user(cmd_list[1:], author)

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

    return "Success! Character added!"
