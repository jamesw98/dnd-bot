import firebase_admin
import discord

from firebase_admin import credentials
from firebase_admin import db

ERROR_INVALID_COMMAND = "Sorry, that spellbook command doesn't exist!\nType `!dnd sb help` to view commands"
ERROR_CHARACTER_NOT_EXISTS = "I could not find a character with that name. To view your characters type:\n```!dnd character list```"
ERROR_NO_CLASS_SET = "Please set a class for your character before you run this command\n```!dnd c [name] set class [class]```"
ERROR_ALREADY_INIT = "This character already has an initialized spellbook. If you'd like to clear it type:\n```!dnd sb clear [name]```"
ERROR_SPELL_ALREADY_IN_BOOK = "This character already has that spell! You can't have the same spell twice"

INVALID_FORMAT_CREATE = "Invalid formatting, you must enter a character name to create a spellbook for:\n```!dnd sb add```"
INVALID_FORMAT_ADD = "Invalid formatting, you must enter a character name, and a spell:\n```!dnd sb add [spell name]``````!dnd sb add magic missile```"
INVALID_FORMAT_ADD_NO_LEVEL = "Invalid formatting, you did not enter a level.\n```!dnd sb add [spell name] [level]``````!dnd sb add mage hand 0```"
INVALID_FORMAT_ADD_LEVEL = "Invalid formmating, you entered a level that doesn't exist.\nValid levels: `0, 1, 2, 3, 4, 5, 6, 7, 8, 9` where cantrips are `0`"

SPELL_LEVELS = ["cantrip", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]

characters_for_user = {}

# parses the command
def spellbook_parse(cmd_list, author):
    if (cmd_list[0] == "create" or cmd_list[0] == "c"): #!dnd sb create [character name]
        return init_spellbook(cmd_list[1:], author)
    elif (cmd_list[0] == "add" or cmd_list[0] == "a"):
        return add_spell(cmd_list[1:], author)
    else:
        return ERROR_INVALID_COMMAND

# initializes a spellbook for a character
def init_spellbook(cmd_list, author):
    # ensures valid formatting
    if (len(cmd_list) == 0):
        return INVALID_FORMAT_CREATE

    character_name = cmd_list[0]

    # ensures the character exists
    character_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/")
    if (character_ref.get() == None):
        return ERROR_CHARACTER_NOT_EXISTS

    # ensures the user has set a class for this character (this will come in to play eventually, but right now this doesn't really matter)
    # TODO make this matter
    character_class = db.reference("/users/" + str(author.id) + "/" + character_name + "/class").get()
    if (character_class == None):
        return ERROR_NO_CLASS_SET

    # ensures the user hasn't already created a spellbook for this character
    spell_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/spells").get()
    if (spell_ref != None):
        return ERROR_ALREADY_INIT

    # fills the character spellbook with empty slots
    for level in SPELL_LEVELS:
        character_ref.child("spells").child(level).set("empty")

    character_ref = db.reference("/users/" + str(author.id) + "/sb_character").set(character_name)

    character_message = "\nYou are now modifying `" + character_name + "`'s spellbook, all spellbook commands will run for that character. To switch characters type:```!dnd sb switch [name]```"
    return "Success! A spellbook for `" + character_name + "` has been created, but is empty.\nType `!dnd sb add [spell name] [level]` to add spells (cantrips are 0)" + character_message

def add_spell(cmd_list, author): #!dnd sb add [spell name] [level], !dnd sb add fireball 3, !dnd sb add acid arrow 2, !dnd sb add firebolt 0
    if (len(cmd_list) < 2):
        return INVALID_FORMAT_ADD

    character_name = db.reference("/users/" + str(author.id) + "/sb_character").get()

    spell_value = ""

    level = -1
    for i in cmd_list:
        try:
            level = int(i)
        except:
            spell_value += i + " "

    spell_value = spell_name = spell_value[:len(spell_value) - 1]
    
    if (level == -1):
        return INVALID_FORMAT_ADD_NO_LEVEL

    if (level < 0 or level > 9):
        return INVALID_FORMAT_ADD_LEVEL

    level_str = SPELL_LEVELS[level]

    spell_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/spells/" + level_str + "/")
    if (spell_ref.get() != "empty"):
        if (spell_value in spell_ref.get()):
            return ERROR_SPELL_ALREADY_IN_BOOK
        
        spell_value = spell_ref.get() + ", " + spell_value
    
    spell_ref.set(spell_value)

    return "Success! Added spell `" + spell_name + "` to `" + character_name + "`'s spellbook"




