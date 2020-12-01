import os
import random

from validator import *
from search import get_search_results

INVALID_FORMAT = "Invalid formatting"

def parse(msg) -> str:
    cmd_list = msg.content[5:].lower().split(" ")

    if (cmd_list[0] == "roll"):
        return roll_dice(cmd_list[1:])
    elif (cmd_list[0] == "help"):
        return get_help()
    elif (cmd_list[0] == "search"):
        return search_helper(cmd_list[1:])
    else:
        return "[AC] Sorry, that command doesn't exist!\nType '!dnd help' to view commands"

# shows the help message
def get_help() -> str:
    res = "Adventure Companion v0.2\n"
    res += "```- '!dnd help': shows this message\n"
    res += "- '!dnd roll': rolls dice; formatting:\n"
    res += "  - <numDice>d<dieType> +/- <modifier>\n"
    res += "  - 1d20 + 2 d/a (rolls 1d20 at disadvantage/advantage, can be used for any number/type of dice)\n"
    res += "- '!dnd search <query>': searches for any spell or equipment item (more options coming soon)```"
    return res

def search_helper(cmd_list) -> str:
    if (len(cmd_list) < 1):
        return INVALID_FORMAT + ", you must enter a value after 'search'"
    
    query = ""
    if (len(cmd_list) > 1):
        for i in range(len(cmd_list)):
            query += cmd_list[i]
            if (i != len(cmd_list) - 1):
                query += "-"

    else:
        query = cmd_list[0]

    return get_search_results(query)

# parses the roll command and does error handling
def roll_dice(cmd_list) -> str:
    # ensures they typed the command correctly
    if (len(cmd_list) < 1):
        return INVALID_FORMAT

    # makes sure the user formatted the first parameter correctly
    if (len(cmd_list[0].split("d")) > 1):
        value = 0

        # gets the number of dice and die type
        num_dice = cmd_list[0].split("d")[0]
        die_type = cmd_list[0].split("d")[1]
        
        # makes sure these values are valid
        res = validate_dice(num_dice, die_type)

        if (res != "valid"):
            return res

        add = False
        modifier = 0

        # advantage value (n, a, d)
        advantage_val = "n"

        # checks to see if users inputed a modifier OR advantage/disadvantage
        if (len(cmd_list) > 1):
            advantage = False
            # gets the modifier type
            if (cmd_list[1] == "+"):
                add = True
            elif (cmd_list[1] == "-"):
                add = False
            elif (cmd_list[1] == "a"):
                advantage = True
                advantage_val = "a"
            elif (cmd_list[1] == "d"):
                advantage = True
                advantage_val = "d"
            else:
                # anything besides +, -, a, d is invalid
                return INVALID_FORMAT + ", invalid operation: `" + cmd_list[1] + "`"

            # if the user inputted an operator, but no modifier
            if(len(cmd_list) < 3 and not advantage):
                return INVALID_FORMAT + ", operator exists, but no modifier"
            
            # checks to make sure the modifier is valid
            if (not advantage):
                try:
                    modifier = int(cmd_list[2])
                except:
                    return INVALID_FORMAT + ", modifier: `" + cmd_list[2] + "`"
            
        # handle advantage or disadvantage
        if (len(cmd_list) == 4):
            if (cmd_list[3].lower() != 'a' and cmd_list[3].lower() != 'd'):
                return INVALID_FORMAT + ", invalid advantage/disadvantage: `" + cmd_list[3] + "`"
            
            advantage_val = cmd_list[3].lower()

        # user has advantage
        if (advantage_val == "a"):
            value = min([roll(num_dice, die_type), roll(num_dice, die_type)])

        # user has disadvantage
        elif (advantage_val == "d"):
            value = min([roll(num_dice, die_type), roll(num_dice, die_type)])

        # neither advantage or disadvantage
        else:
            value = roll(num_dice, die_type)

        # if there is a modifier, we add it or subtract it
        if (add):
            value += modifier
        else:
            value -= modifier

        # don't want to show negative or 0 to the user
        if (value < 0):
            value = "You rolled a: 1, oof"

        return "You rolled a: " + str(value)

    else:
        return INVALID_FORMAT + "invalid roll type: `" + cmd_list[0] + "`"

# rolls a set a of dice
def roll(num_dice, die_type):
    value = 0
    for i in range(int(num_dice)):
        value += random.randint(1, int(die_type))
    return value
