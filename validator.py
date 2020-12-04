INVALID_ROLL_FORMAT = "Invalid formatting"

# makes sure a die roll is valid
def validate_dice(num_dice, die_type):
    # makes sure the entered a number for the number of dice
    try:
        int(num_dice)
    except:
        return INVALID_ROLL_FORMAT + ", number of dice: `" + num_dice + "`"

    # makes sure the entered a number for the type of dice
    try:
        int(die_type)
    except:
        return INVALID_ROLL_FORMAT + ", die type: `" + die_type + "`"

    if (int(num_dice) < 1):
        return INVALID_ROLL_FORMAT + ", number of dice must be positive"

    if (int(die_type) < 1):
        return INVALID_ROLL_FORMAT + ", die type must be positive"

    return "valid"