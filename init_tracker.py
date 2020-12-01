import discord
from messages import build_init_message

ERROR_ALREADY_TRACKING = "You are already tracking initiative.\nIf you want to clear your existing initiative type: ```!dnd init clear```"
ERROR_NOT_TRACKING = "Invalid formatting, initiative number must be larger than 0."

INVALID_FORMAT_NO_CHARACTERS = "Invalid formatting, you did not include any characters after `init`.\nProper usage: ```!dnd init Volo:18,Strahd:12,Drizzt:10,jombles:1```"
INVALID_FORMAT_ONE_CHARACTER = "Invalid formatting, there is only one character.\nI'm sure you can handle tracking one player without my help : )"
INVALID_FORMAT_CHARACTER_MISSING_COLON = "Invalid formatting, missing a colon in character.\nYou are missing a colon between a character than their initiative number"
INVALID_FORMAT_ZERO_OR_NEGATIVE = "Invalid formatting, initiative number must be larger than 0."

users_tracking_init = [] # list of users currently tracking init, just the usernames
initiatives = {} # dict {"<discord id>:[array of Player objects]}

# parses command
def init_parse(cmd_list, author):
    if (cmd_list[0] == "start" or cmd_list[0] == "s"):
        return start_init(cmd_list[1:], author)
    elif (cmd_list[0] == "next" or cmd_list[0] == "n"):
        # TODO implement this
        # cycle initative
        pass
    elif (cmd_list[0] == "clear" or cmd_list[0] == "c"):
        return clear_init(author)

# starts tracking init for a user
def start_init(cmd_list, author):
    # makes sure the user is not already tracking
    if (author.id in users_tracking_init):
        return ERROR_ALREADY_TRACKING

    # makes sure user ented some characters
    if (len(cmd_list) == 0):
        return INVALID_FORMAT_NO_CHARACTERS
    
    player_list = cmd_list[0].split(",")

    # makes sure user entered > 1 characters
    if (len(player_list) == 1):
        return INVALID_FORMAT_ONE_CHARACTER

    # adds the user to the list of tracked users
    users_tracking_init.append(author.id)
    # creates an empty list in the dictionary for this user
    initiatives[author.id] = []

    # loops through the players the user entered
    for p in player_list:
        # ensures proper formatting
        if (":" not in p):
            clear_init(author)
            return INVALID_FORMAT_CHARACTER_MISSING_COLON

        # gets the name of the current player from the user
        p_name = p.split(":")[0]
        # gets the initative number for the current player from the user
        p_init = int(p.split(":")[1])

        # makes sure the initiative number is valid
        if (p_init <= 0):
            clear_init(author)
            return INVALID_FORMAT_ZERO_OR_NEGATIVE

        # adds the current player to the user's list of players
        initiatives[author.id].append(Player(p_name, p_init))

    # sorts the players based on their initiative numbers
    initiatives[author.id].sort(key=lambda p: p.init_num, reverse=True)

    # builds message
    result_string = "Done! Here is your current initiative:\n```"
    result_string += build_init_message(initiatives[author.id])
    result_string += "```"

    return result_string

# removes the user from init tracking and clears their list
def clear_init(author):
    if (author.id not in users_tracking_init):
        return ERROR_NOT_TRACKING
    
    users_tracking_init.remove(author.id)
    initiatives[author.id] = []

    return "Done! Your initiative is cleared"

class Player:
    def __init__(self, name, init_num):
        self.name = name
        self.init_num = init_num