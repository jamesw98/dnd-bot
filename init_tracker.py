import discord
from messages import build_init_message

ERROR_ALREADY_TRACKING = "You are already tracking initiative.\nIf you want to clear your existing initiative type: ```!dnd init clear```"
ERROR_NOT_TRACKING = "Invalid formatting, initiative number must be larger than 0."
ERROR_NO_PLAYER = "No player was found with that name"
ERROR_GOING_BELOW_TWO = "You cannot remove any more players, you have to have at least 2 players in initiative to track.\nIf you want to clear your initiative, type ```!dnd init clear```"

INVALID_FORMAT_NO_CHARACTERS = "Invalid formatting, you did not include any characters after `init`.\nProper usage: ```!dnd init start Volo:18,Strahd:12,Drizzt:10,jombles:1```"
INVALID_FORMAT_ONE_CHARACTER = "Invalid formatting, there is only one character.\nI'm sure you can handle tracking one player without my help : )"
INVALID_FORMAT_CHARACTER_MISSING_COLON = "Invalid formatting, missing a colon in character.\nYou are missing a colon between a character than their initiative number"
INVALID_FORMAT_ZERO_OR_NEGATIVE = "Invalid formatting, initiative number must be larger than 0."
INVALID_FORMAT_NO_PLAYER = "Invalid formatting, no player was inputted"

users_tracking_init = [] # list of users currently tracking init
initiatives = {} # dict {"<discord id>:[array of Player objects]}
current_initiatives = {} # the current places in initiative for users

# parses command
def init_parse(cmd_list, author):
    if (len(cmd_list) < 1):
        return view_init(author)
    elif (cmd_list[0] == "start" or cmd_list[0] == "s"):
        return start_init(cmd_list[1:], author)
    elif (cmd_list[0] == "next" or cmd_list[0] == "n"):
        return cycle_init(author)
    elif (cmd_list[0] == "clear" or cmd_list[0] == "c"):
        return clear_init(author)
    elif (cmd_list[0] == "remove" or cmd_list[0] == "r"):
        return remove_player(author, cmd_list)
    elif (cmd_list[0] == "add" or cmd_list[0] == "a"):
        return add_to_init(cmd_list[1:], author)

# prints out the current initiative
def view_init(author):
    if (author.id not in users_tracking_init):
        return ERROR_NOT_TRACKING

    result_string = ""
    result_string += "Here you go:\n```"
    result_string += build_init_message(initiatives[author.id], current_initiatives[author.id])
    result_string += "```"

    return result_string

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
    # sets the first player in this user's initiative order to 
    # be the current player with initiative
    current_initiatives[author.id] = 1

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

    c = 1
    for player in initiatives[author.id]:
        player.place = c
        c += 1

    # builds message
    result_string = "Done! Here is your current initiative:\n```"
    result_string += build_init_message(initiatives[author.id], 1)
    result_string += "```"

    return result_string

# removes a player from a user's initiative list
def remove_player(author, cmd_list):
    if (author.id not in users_tracking_init):
        return ERROR_NOT_TRACKING

    if (len(cmd_list) == 1):
        return INVALID_FORMAT_NO_PLAYER

    player_name = cmd_list[1]

    if (len(initiatives[author.id]) == 2):
        return ERROR_GOING_BELOW_TWO
    
    ind = 0
    for player in initiatives[author.id]:
        if (player.name == player_name.lower()):
            del(initiatives[author.id][ind])
            return "Done! Removed player: " + player.name
        ind += 1
    
    return ERROR_NO_PLAYER

# adds player(s) to the initiative
def add_to_init(cmd_list, author):
    # makes sure the user is not already tracking
    if (author.id not in users_tracking_init):
        return ERROR_NOT_TRACKING

    # makes sure user ented some characters
    if (len(cmd_list) == 0):
        return INVALID_FORMAT_NO_CHARACTERS
    
    player_list = cmd_list[0].split(",")

    current_init = current_initiatives[author.id]
    player_name_current_init = initiatives[author.id][current_init].name

    for p in player_list:
        if (":" not in p):
            return INVALID_FORMAT_CHARACTER_MISSING_COLON
        
        p_name = p.split(":")[0]
        p_init = int(p.split(":")[1])

        initiatives[author.id].append(Player(p_name, p_init))
    
    initiatives[author.id].sort(key=lambda p: p.init_num, reverse=True)

    # makes sure the > stays in the right spot for the initiative list
    c = 1
    for p in initiatives[author.id]:
        if (p.name == player_name_current_init):
            current_initiatives[author.id] = c - 1
        c += 1

    return view_init(author)

# removes the user from init tracking and clears their list
def clear_init(author):
    if (author.id not in users_tracking_init):
        return ERROR_NOT_TRACKING
    
    users_tracking_init.remove(author.id)
    initiatives[author.id] = []
    current_initiatives[author.id] = 0

    return "Done! Your initiative is cleared"

# moves the > to the next player in initiative
def cycle_init(author):
    result_string = ""

    if ((current_initiatives[author.id]) + 1 > len(initiatives[author.id])):
        current_initiatives[author.id] = 1
    else: 
        current_initiatives[author.id] += 1

    return view_init(author)

class Player:
    def __init__(self, name, init_num):
        self.name = name
        self.init_num = init_num