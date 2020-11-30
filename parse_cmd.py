import os
import random

from validator import *

INVALID_ROLL_FORMAT = "Invalid formatting"

def parse(msg) -> str:
    cmd_list = msg.content[5:].lower().split(" ")

    if (cmd_list[0] == "roll"):
        return roll(cmd_list[1:])
    elif(cmd_list[0] == "help"):
        return get_help()
    else:
        return "[AC] Sorry, that command doesn't exist!\nType '!dnd help' to view commands"

def get_help() -> str:
    return "```Adventure Companion v0.1\n Available Commands:\n- roll: rolls dice; formatting:\n    - <numDice>d<dieType> +/- <modifier>\n    - d/a 1d20 (rolls 1d20 at disadvantage/advantage)\n    - d/a 1d20 + 10```"

# rolls dice
def roll(cmd_list) -> str:
    # ensures they typed the command correctly
    if (len(cmd_list) < 1):
        return INVALID_ROLL_FORMAT

    # makes sure the user formatted the first parameter correctly
    if (len(cmd_list[0].split("d")) > 1):
        value = 0

        num_dice = cmd_list[0].split("d")[0]
        die_type = cmd_list[0].split("d")[1]
        
        res = validate_dice(num_dice, die_type)

        if (res != "valid"):
            return res

        add = False
        modifier = 0

        if (len(cmd_list) > 1):
            if (cmd_list[1] == "+"):
                add = True
            elif (cmd_list[1] == "-"):
                add = False
            else:
                return INVALID_ROLL_FORMAT + ", invalid operation: `" + cmd_list[1] + "`"

            if(len(cmd_list) < 3):
                return INVALID_ROLL_FORMAT + ", operator exists, but no modifier"
            
            try:
                modifier = int(cmd_list[2])
            except:
                return INVALID_ROLL_FORMAT + ", modifier: `" + cmd_list[2] + "`"

        for i in range(int(num_dice)):
            temp_val = random.randint(1, int(die_type) - 1)
            value += temp_val

        if (add):
            value += modifier
        else:
            value -= modifier

        if (value < 0):
            value = "You rolled a: 1, oof"

        return "You rolled a: " + str(value)

    else:
        return INVALID_ROLL_FORMAT + "invalid roll type: `" + cmd_list[0] + "`"