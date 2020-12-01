import discord
from messages import build_init_message

ALREADY_TRACKING = "You are already tracking initiative.\nIf you want to clear your existing initiative type: ```!dnd init clear```"
INVALID_FORMAT_NO_CHARACTERS = "Invalid formatting, you did not include any characters after `init`.\nProper usage: ```!dnd init Volo:18,Strahd:12,Drizzt:10,jombles:1```"
INVALID_FORMAT_ONE_CHARACTER = "Invalid formatting, there is only one character.\nI'm sure you can handle tracking one player without my help : )"
INVALID_FORMAT_CHARACTER_MISSING_COLON = "Invalid formatting, missing a colon in character.\nYou are missing a colon between a character than their initiative number"
INVALID_FORMAT_DUPLICATE = "Invalid formatting, there is a duplicate character."
INVALID_FORMAT_ZERO_OR_NEGATIVE = "Invalid formatting, initiative number must be larger than 0."

users_tracking_init = [] # list of users currently tracking init, just the usernames
initiatives = {} # dict {"<discord id>:[array of Player objects]}
out_of_initiative = [] 

def init_parse(cmd_list, author):
    if (cmd_list[0] == "start" or cmd_list[0] == "s"):
        return start_init(cmd_list[1:], author)
    elif (cmd_list[0] == "next" or cmd_list[0] == "n"):
        pass
        # cycle initative

def start_init(cmd_list, author):
    if (author.id in users_tracking_init):
        return ALREADY_TRACKING

    if (len(cmd_list) == 0):
        return INVALID_FORMAT_NO_CHARACTERS

    player_list = cmd_list[0].split(",")
    if (len(player_list) == 1):
        return INVALID_FORMAT_ONE_CHARACTER

    users_tracking_init.append(author.id)
    initiatives[author.id] = []

    for p in player_list:
        if (":" not in p):
            return INVALID_FORMAT_CHARACTER_MISSING_COLON

        p_name = p.split(":")[0]
        p_init = int(p.split(":")[1])

        if (p_name in initiatives[author.id]):
            return INVALID_FORMAT_DUPLICATE
        
        if (p_init <= 0):
            return INVALID_FORMAT_ZERO_OR_NEGATIVE

        initiatives[author.id].append(Player(p_name, p_init))

    initiatives[author.id].sort(key=lambda p: p.init_num, reverse=True)

    result_string = "Done! Here is your current initiative:\n```"
    result_string += build_init_message(initiatives[author.id])
    result_string += "```"

    return result_string

class Player:
    def __init__(self, name, init_num):
        self.name = name
        self.init_num = init_num
