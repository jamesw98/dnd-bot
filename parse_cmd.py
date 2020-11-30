import os
import random

def parse(msg) -> str:
    cmd_list = msg.content[5:].lower().split(" ")

    if (cmd_list[0] == "roll"):
        return roll(cmd_list[1:])
    elif(cmd_list[0] == "help"):
        return get_help()
    else:
        return "[AC] Sorry, that command doesn't exist!\nType '!dnd help' to view commands"

def get_help() -> str:
    return "```Adventure Companion v0.1\n Available Commands:\n- roll: rolls dice; formatting:\n    - 1d20, 2d4 + 2, 1d20 - 2\n    - d/a 1d20 (rolls 1d20 at disadvantage/advantage)\n    - d/a 1d20 + 10```"