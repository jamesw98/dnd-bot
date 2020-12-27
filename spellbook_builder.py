import firebase_admin
import discord

from firebase_admin import credentials
from firebase_admin import db

from embed_builder import build_spellbook_embed
from messages import build_spellbook_help_message

# error messages
ERROR_INVALID_COMMAND = "Sorry, that spellbook command doesn't exist!\nType `!dnd sb help` to view commands"
ERROR_CHARACTER_NOT_EXISTS = "I could not find a character with that name. To view your characters type:\n```!dnd character list```"
ERROR_NO_CLASS_SET = "Please set a class for your character before you run this command\n```!dnd c set class [class]```"
ERROR_ALREADY_INIT = "This character already has an initialized spellbook. If you'd like to clear it type:\n```!dnd sb clear [name]```"
ERROR_SPELL_ALREADY_IN_BOOK = "This character already has that spell! You can't have the same spell twice"
ERROR_NO_BOOK_CREATED = "You have not created a book for any character or have somehow switched to a character without a spellbook (this shouldn't be possible)"
ERROR_REMOVE_NOT_ENOUGH_ARGS = "You have to enter a spell to remove"
ERROR_NO_SPELL_FOUND = "We couldn't find that spell in your spellbook"
ERROR_NO_CHARACTERS = "You have not created any characters. To view character commands type:\n```!dnd character help```"

# invalid formatting messages
INVALID_FORMAT_CREATE = "Invalid formatting, you must enter a character name to create a spellbook for.\n```!dnd sb ceate [name]```"
INVALID_FORMAT_ADD = "Invalid formatting, you must enter a character name, and a spell:\n```!dnd sb add [spell name]``````!dnd sb add magic missile```"
INVALID_FORMAT_ADD_NO_LEVEL = "Invalid formatting, you did not enter a level.\n```!dnd sb add [spell name] [level]``````!dnd sb add mage hand 0```"
INVALID_FORMAT_ADD_LEVEL = "Invalid formmating, you entered a level that doesn't exist.\nValid levels: `0, 1, 2, 3, 4, 5, 6, 7, 8, 9` where cantrips are `0`"
INVALID_FORMAT_SWITCH = "Invalid formatting, you must enter a character to switch to"

# the possible spell levels
SPELL_LEVELS = ["Cantrips", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]

# parses the command
def spellbook_parse(cmd_list, author):
    if (len(cmd_list) == 0):
        return ERROR_INVALID_COMMAND
    elif (cmd_list[0] == "create" or cmd_list[0] == "c"):
        return init_spellbook(cmd_list[1:], author)
    elif (cmd_list[0] == "add" or cmd_list[0] == "a"):
        return add_spell(cmd_list[1:], author)
    elif (cmd_list[0] == "view" or cmd_list[0] == "v"):
        return view_spellbook(author)
    elif (cmd_list[0] == "remove" or cmd_list[0] == "r"):
        return remove_spell(cmd_list[1:], author)
    elif (cmd_list[0] == "switch" or cmd_list[0] == "s"):
        return switch_book(cmd_list[1:], author)
    elif (cmd_list[0] == "help" or cmd_list[0] == "h"):
        return build_spellbook_help_message()
    else:
        return ERROR_INVALID_COMMAND

# switches the current spellbook to another character
def switch_book(cmd_list, author):
    # ensures the user has characters
    base_ref = db.reference("/users/" + str(author.id)).get()
    if (base_ref == None):
        return ERROR_NO_CHARACTERS

    # ensures valid command formatting
    if (len(cmd_list) == 0):
        return INVALID_FORMAT_SWITCH
    
    # gets the character name from the user command
    character_name = cmd_list[0]

    # makes sure the character they want to switch to exists 
    character_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/")
    if (character_ref.get() == None):
        return ERROR_CHARACTER_NOT_EXISTS

    db.reference("/users/" + str(author.id) + "/sb_character").set(character_name)

    return "Success! Switched to characters: `" + character_name + "`"

# initializes a spellbook for a character
def init_spellbook(cmd_list, author):
    base_ref = db.reference("/users/" + str(author.id)).get()
    if (base_ref == None):
        return ERROR_NO_CHARACTERS

    # ensures valid formatting
    if (len(cmd_list) == 0):
        return INVALID_FORMAT_CREATE

    character_name = cmd_list[0]

    # ensures the character exists
    character_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/")
    if (character_ref.get() == None):
        return ERROR_CHARACTER_NOT_EXISTS

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

# adds a spell to a character for a user
def add_spell(cmd_list, author): 
    base_ref = db.reference("/users/" + str(author.id)).get()
    if (base_ref == None):
        return ERROR_NO_CHARACTERS
    
    # ensures valid formatting
    if (len(cmd_list) < 2):
        return INVALID_FORMAT_ADD

    # ensures they have created a book
    character_name = db.reference("/users/" + str(author.id) + "/sb_character").get()
    if (character_name == None):
        return ERROR_NO_BOOK_CREATED

    spell_value = ""

    # ensures they entered a level number as well as builds the spell string
    level = -1
    for i in cmd_list:
        try:
            level = int(i)
            break
        except:
            spell_value += i + " "

    # removes the space from the back 
    spell_value = spell_name = spell_value[:len(spell_value) - 1]
    
    # ensures they entered a level
    if (level == -1):
        return INVALID_FORMAT_ADD_NO_LEVEL

    # ensures the entered a valid level
    if (level < 0 or level > 9):
        return INVALID_FORMAT_ADD_LEVEL

    # gets the level string from the list
    level_str = SPELL_LEVELS[level]

    # attemps to add the spell to the character's book
    spell_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/spells/" + level_str + "/")
    # if spells have been added
    if (spell_ref.get() != "empty"):
        # checks to see if they already have this spell in the book
        if (spell_value in spell_ref.get()):
            return ERROR_SPELL_ALREADY_IN_BOOK
        # adds the spell to their list of spells in this level
        temp_ref = spell_ref.get()
        temp_ref.append(spell_value)
        spell_ref.set(temp_ref)
    else :
        # if they don't have any spells in this level, just set the level to only contain this spell
        spell_ref.set([spell_value])

    return "Success! Added spell `" + spell_name + "` to `" + character_name + "`'s spellbook"

# removes spells from the character's spellbook
def remove_spell(cmd_list, author):
    base_ref = db.reference("/users/" + str(author.id)).get()
    if (base_ref == None):
        return ERROR_NO_CHARACTERS

    # ensures proper formatting
    if (len(cmd_list) < 1):
        return ERROR_REMOVE_NOT_ENOUGH_ARGS

    # ensures they have created a book
    character_name = db.reference("/users/" + str(author.id) + "/sb_character").get()
    if (character_name == None):
        return ERROR_NO_BOOK_CREATED
    
    spell_value = ""
    for i in cmd_list:
        spell_value += i + " "

    # removes the space at the end
    spell_value = spell_value[:len(spell_value) - 1]
    
    character_ref = db.reference("/users/" + str(author.id) + "/" + character_name + "/")

    result_level = None
    spell_level = None
    # goes through all the spell levels
    for level in SPELL_LEVELS:
        # gets the spells for this level
        spell_level = character_ref.child("spells").child(level).get()
        # checks if there are spells for this level and if the spell is in it
        if (spell_level != "empty" and spell_value in spell_level):
            spell_level.remove(spell_value)

            if (len(spell_level) == 0):
                spell_level = "empty"

            character_ref.child("spells").child(level).set(spell_level)
            return "Success! Removed spell: `" + spell_value + "` from `" + character_name + "`'s spellbook"
   
    return "Couldn't find that spell"    

# shows an embed for the current character's spellbook
def view_spellbook(author):
    base_ref = db.reference("/users/" + str(author.id)).get()
    if (base_ref == None):
        return ERROR_NO_CHARACTERS

    # ensures the user has created a spellbook 
    character_name = db.reference("/users/" + str(author.id) + "/sb_character").get()
    if (character_name == None):
        return ERROR_NO_BOOK_CREATED

    return build_spellbook_embed(character_name, author.id)