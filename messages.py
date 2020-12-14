import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

ERROR_CHARACTER_NOT_EXISTS = "I could not find a character with that name in your database"
VERSION = "v0.05"

# shows the help message
def build_help_message() -> str:
    res = "Adventure Companion " + VERSION
    res += "```'!dnd help': shows this message\n\n"
    res += "'!dnd roll': rolls dice; formatting:\n"
    res += "  - [numDice]d[dieType] +/- [modifier]\n"
    res += "  - 1d20 + 2 d/a (rolls 1d20 at disadvantage/advantage)\n\n"
    res += "'!dnd search [query]': searches for any spell, equipment, monster, or magic item\n\n"
    res += "'!dnd initiative (start, next, add, remove)`: for full documentation, see the github repo below\n\n"
    res += "'!dnd character help': view character help message\n\n"
    res += "'!dnd sb help': view spellbook help message\n\n"
    res += "```Created by **jombles#6380**\nFor full documentation see: <https://github.com/jamesw98/dnd-bot>"
    return res

def build_character_help_message() -> str:
    res = "Adventure Companion " + VERSION + " Character Help"
    res += "```'!dnd character help': shows this message\n\n"
    res += "'!dnd c list': lists the characters available to you\n"
    res += "'!dnd c list properties': lists the properties you are able to set for any characters\n\n"
    res += "'!dnd c add [name] lvl,hp,ac str,dex,con,int,wis,cha: adds a character\n(note the space between ...,ac and str,dex,...)\n\n"
    res += "'!dnd c [name] set [property name] [property value]: sets a property for a character\n(for notes, description, and alignment, spaces are allowed)\n\n"
    res += "'!dnd c remove [name]: removes a character from your list"
    res += "```Created by **jombles#6380**\nFor full documentation see: <https://github.com/jamesw98/dnd-bot>"
    return res

def build_init_help_message() -> str:
    res = "Adventure Companion " + VERSION + " Initiative Help"
    res += "```'!dnd initiative help': shows this message\n\n"
    res += "'!dnd init start [name1]:[init#],[name2]:[init#],[name3]:[init#],...`: starts tracking initiative\n"
    res += " ex: '!dnd initiative start volo:12,drizzt:18,strahd:22,tav:3'\n\n"
    res += "'!dnd init next': cycles to the next player in initiative\n\n"
    res += "'!dnd remove [name]': removes the player from initiative tracking\n\n"
    res += "'!dnd init add [name1]:[init#],[name2]:[init#],...': adds player(s) to the intiative\n\n"
    res += "'!dnd init': view the current initiative order\n\n"
    res += "'!dnd init clear': clears the initiative and stops tracking\n\n"
    res += "```Created by **jombles#6380**\nFor full documentation see: <https://github.com/jamesw98/dnd-bot>"
    return res

# builds the initiative message
def build_init_message(init_list, curr_place) -> str:
    count = 1
    res = ""

    for i in init_list:
        if (count == curr_place):
            res += "> " + i.name + "\n"
        else: 
            res += "  " + i.name + "\n"
        count += 1

    return res

def calc_modifier(score) -> str:
    mod = (score//2) - 5
    
    if (mod > 0):
        return "+" + str(mod)
    else:
        return " " + str(mod)
        