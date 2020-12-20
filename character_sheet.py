import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from messages import build_character_help_message

from embed_builder import *

# error messages
ERROR_CHARACTER_EXISTS = "You already have a character with that name in your database"
ERROR_CHARACTER_NOT_EXISTS = "I could not find a character with that name. To view your characters type:\n```!dnd character list```"
ERROR_INVALID_PROPERTY = "You entered an invalid property.\nTo view valid properties type:```!dnd character list props```"
ERROR_INVALID_LIST = "I'm not sure what you are trying to list. To view character help type:```!dnd character help```"
ERROR_INVALID_COMMAND = "Sorry, that character command doesn't exist!\nType `!dnd character help` to view commands"
ERROR_CHARACTER_NO_NOTES = "Sorry, I couldn't find any notes for that character"
ERROR_PROF_NO_COMMA = "You must enter at least 2 profeciencies, seperated by commas:\n```!dnd character Rich set profs arcana,insight,religion```"
ERROR_NO_CHARACTERS = "You have not created any characters. To view character commands type:\n```!dnd character help```"

# invalid format warnings
INVALID_FORMAT_VIEW = "Invalid formatting, you didn't enter a name"
INVALID_FORMAT_ADD = "Invalid formatting, make add matches the below formatting:\n```!dnd character add name level,hp,ac attributes (str, dex, con, int, wis, cha)``````!dnd character add Volo 3,25,13 8,10,16,18,13,20```"
INVALID_FORMAT_SET = "Invalid formatting, make add matches the below formatting:\n```!dnd character [character name] set [property name] [property]``````!dnd character Rich set image bit.ly/2L2kvgV```"
INVALID_FORMAT_REMOVE = "Invalid formatting, you need to enter a character to remove:\n```!dnd character remove [character name]```"
INVALID_FORMAT_ADD_BASE_ATTR = "Invalid formatting, something went wrong in your level,hp,ac fields"
INVALID_FORMAT_ADD_STATS = "Invalid formatting, something went wrong in your stats fields"
INVALID_FORMAT_ALIGN = "Invalid formatting, you didn't enter a proper alignment\nMake sure it is 2 words separated by a space. ie. chaotic good, lawful evil, etc"
INVALID_FORMAT_SWITCH = "Invalid formatting, you must enter a character name:```!dnd character switch volo```"

VALID_PROPERTIES = ["race", "class", "image", "notes", "description", "alignment", "proficiencies", "copper", "silver", "gold", "platinum"]

cred = credentials.Certificate("/etc/dnd-discord-bot-66966-firebase-adminsdk-pncqe-3815ee866c.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://dnd-discord-bot-66966.firebaseio.com/"})

# parses the character command
def character_parse(cmd_list, author):
    if (len(cmd_list) == 0):
        return ERROR_INVALID_COMMAND
    # user wants to add a character
    elif (cmd_list[0] == "add" or cmd_list[0] == "a"):
        return create_character_for_user(cmd_list[1:], author)
    # user wants to view their characters
    elif (cmd_list[0] == "view" or cmd_list[0] == "v"):
        return view_character(cmd_list[1:], author)
    # user wants to set a property for one of their characters
    elif (cmd_list[0] == "set" or cmd_list[1] == "s"):
        return set_character_property(cmd_list[1:], author)
    # user wants to list their characters or the property list
    elif (cmd_list[0] == "list" or cmd_list[0] == "l"):
        return list_helper(cmd_list[1:], author)
    # user wants to remove one of their characters
    elif (cmd_list[0] == "remove" or cmd_list[0] == "r"):
        return remove_character(cmd_list[1:], author)
    # user wants to view the help message
    elif (cmd_list[0] == "help" or cmd_list[0] == "h"):
        return build_character_help_message()
    elif (cmd_list[0] == "switch" or cmd_list[0] == "s"):
        return switch_character(cmd_list[1:], author)
    else:
        return ERROR_INVALID_COMMAND

# determines what kind of list to show
def list_helper(cmd_list, author):
    # lists characters for user
    if (len(cmd_list) == 0):
        return "Here are your characters: " + build_character_list_message(db.reference("/users/" + str(author.id)).get().keys())
    # lists valid properties
    elif (cmd_list[0] == "properties" or cmd_list[0] == "props"):
        return "Available Properties:\n" + build_property_message()
    else:
        return ERROR_INVALID_LIST

# creates a character for a user and adds the character
# to the user's firebase database
def create_character_for_user(cmd_list, author):
    # make sure input is proper
    if (len(cmd_list) != 3):
        return INVALID_FORMAT_ADD

    char_name = cmd_list[0]

    base_ref = db.reference("/users/" + str(author.id))

    # makes sure the user doesn't already have a character
    # with the name they are trying to add
    if (base_ref.child(char_name).get() != None):
        return ERROR_CHARACTER_EXISTS

    # makes sure input is proper
    if (len(cmd_list[1].split(",")) != 3):
        return INVALID_FORMAT_ADD_BASE_ATTR

    # gets the level, hit points, and armor class for the character
    char_lvl = str(cmd_list[1].split(",")[0])
    char_hp =  str(cmd_list[1].split(",")[1])
    char_ac =  str(cmd_list[1].split(",")[2])

    # makes sure input is proper
    if (len(cmd_list[2].split(",")) != 6):
        return INVALID_FORMAT_ADD_STATS
    
    # gets the attributes for the character
    char_str = str(cmd_list[2].split(",")[0])
    char_dex = str(cmd_list[2].split(",")[1])
    char_con = str(cmd_list[2].split(",")[2])
    char_int = str(cmd_list[2].split(",")[3])
    char_wis = str(cmd_list[2].split(",")[4])
    char_cha = str(cmd_list[2].split(",")[5])

    # adds the character to the user's database
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

    db.reference("/users/" + str(author.id) + "/curr_character").set(char_name)

    character_message = "\nYou are now modifying `" + char_name + "`, all character names commands will now be run on this character. To switch characters type:```!dnd character switch [name]```"
    return "Success! Character added!\nType `!dnd character view " + char_name + "` to view them" + character_message

# switches the character that is currently being modified
def switch_character(cmd_list, author):
    base_ref = db.reference("/users/" + str(author.id)).get()
    if (base_ref == None):
        return ERROR_NO_CHARACTERS

    if (len(cmd_list) == 0):
        return INVALID_FORMAT_SWITCH

    character_name = cmd_list[0]

    character_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/")
    if (character_ref.get() == None):
        return ERROR_CHARACTER_NOT_EXISTS

    db.reference("/users/" + str(author.id) + "/curr_character").set(character_name)

    return "Success! Switched to characters: `" + character_name + "`"

# sets a property for a character
def set_character_property(cmd_list, author):
    character_name = db.reference("/users/" + str(author.id) + "/curr_character").get()
    if (character_name == None):
        return ERROR_CHARACTER_NOT_EXISTS

    # makes sure input is proper
    if (len(cmd_list) < 2):
        return INVALID_FORMAT_SET
    
    # gets the base ref for the user runnning the command
    base_ref = db.reference("/users/" + str(author.id))

    # makes sure character exists
    if (base_ref.child(character_name).get() == None):
        return ERROR_CHARACTER_NOT_EXISTS
    
    property_type = cmd_list[0].lower()

    # makes sure the property they are trying to set is valid
    if (property_type not in VALID_PROPERTIES):
        print(property_type)
        return ERROR_INVALID_PROPERTY

    
    if (property_type == "proficiencies" or property_type == "profs"):
        if ("," not in cmd_list[1]):
            return ERROR_PROF_NO_COMMA
        
        modify_db_char_property(property_type, author, character_name, cmd_list[1])

        return "Success! Added proficiencies to your character"

    # alignments are a special case, they should be 2 words 
    # separated by a space
    elif (property_type == "alignment"):
        if (len(cmd_list) != 3):
            return INVALID_FORMAT_ALIGN
        
        align_first = cmd_list[1] # get the first word
        align_second = cmd_list[2] # get the second

        # modifies the property for the character
        modify_db_char_property(property_type, author, character_name, align_first + " " + align_second)

        return "Success! Set " + property_type + " to `" + align_first + " " + align_second + "` to character: `" + character_name + "`"

    elif (property_type == "notes"):
        temp_res = ""

        notes_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/notes")

        if (cmd_list[1] == "clear"):
            if (notes_ref.get() != None):
                notes_ref.delete()
                return "Success! Cleared your notes"
            else:
                return ERROR_CHARACTER_NO_NOTES

        if (notes_ref.get() != None):
            temp_res = notes_ref.get() + "\n\n"
        
        for prop in cmd_list[1:]:
            temp_res += prop + " "
        
        # modifies the property for the character
        modify_db_char_property(property_type, author, character_name, temp_res)

        return "Success! Set property: `" + property_type + "`"

    # description and notes are also special, since they can contain spaces
    elif (property_type == "description"):
        temp_res = ""
        for prop in cmd_list[1:]:
            temp_res += prop + " "
        
        # modifies the property for the character
        modify_db_char_property(property_type, author, character_name, temp_res)

        return "Success! Set property: `" + property_type + "`"
    # everything else should be handled here
    else:
        property_value = cmd_list[1]

        # modifies the property for the character
        modify_db_char_property(property_type, author, character_name, property_value)  

        return "Success! Set " + property_type + " to `" + property_value + "` for character: `" + character_name + "`"

# helper for the above function
def modify_db_char_property(property_type, author, character_name, property_value):
    base_ref = db.reference("/users/" + str(author.id) + "/" + character_name)
    base_ref.child(property_type).set(property_value)

# remove a character from a user's list
def remove_character(cmd_list, author):
    base_ref = db.reference("/users/" + str(author.id))

    # ensures valid formatting
    if (len(cmd_list) == 0):
        return INVALID_FORMAT_REMOVE
    
    character_name = cmd_list[0]

    # ensures the character exists
    if (base_ref.child(character_name).get() == None):
        return ERROR_CHARACTER_NOT_EXISTS

    db.reference("/users/" + str(author.id) + "/" + character_name + "/").delete()

    return "Success! Your character: " + character_name + " has been removed"

# displays character info
def view_character(cmd_list, author):
    if (len(cmd_list) < 1):
        return INVALID_FORMAT_VIEW

    base_ref = db.reference("/users/" + str(author.id))

    if (base_ref.child(cmd_list[0]).get() == None):
        return ERROR_CHARACTER_NOT_EXISTS

    return build_character_embed(cmd_list[0], author.id)

# builds the property message 
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

# builds the character list message
def build_character_list_message(char_list):
    c = 0
    res = "```"
    for i in char_list:
        if (i == "sb_character"):
            continue
        if (c != len(char_list) - 1):
            res += i + ", "
        else:
            res += i
        c += 1
    res += "```"
    return res
