INVALID_ROLL_FORMAT = "Invalid formatting"

def validate_dice(num_dice, die_type):
    try:
        int(num_dice)
    except:
        return INVALID_ROLL_FORMAT + ", number of dice: `" + num_dice + "`"

    try:
        int(die_type)
    except:
        return INVALID_ROLL_FORMAT + ", die type: `" + die_type + "`"

    if (int(num_dice) < 1):
        return INVALID_ROLL_FORMAT + ", number of dice must be positive"

    if (int(die_type) < 1):
        return INVALID_ROLL_FORMAT + ", die type must be positive"

    return "valid"