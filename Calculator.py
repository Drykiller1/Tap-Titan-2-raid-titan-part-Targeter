HEAD = 0
TORSO = 0
ARMS = 0
LEGS = 0
HEALTH_TARGETED = 0
SUBTRACT_LEGS = True
SUBTRACT_ARMS = True


def find_leg_index(titan_target_order):
    for index, name in enumerate(titan_target_order):
        if "Legs" in name:
            return index


def find_arm_index(titan_target_order):
    for index, name in enumerate(titan_target_order):
        if "Arms" in name:
            return index


def print_what_to_target():
    global HEAD, TORSO, ARMS, LEGS, HEALTH_TARGETED
    print(f"Health to damage: {round(HEALTH_TARGETED, 2)}")
    print(f"Head: {HEAD}")
    print(f"Torso: {TORSO}")
    print(f"Arms: {ARMS}")
    print(f"Legs: {LEGS}")

def int_or_float_input(text):
    user_input = input(f"{text} ")
    try:
        float(user_input)
    except ValueError:
        print("Enter a valid number.")
        int_or_float_input(text)
    else:
        user_input = float(user_input)
        return user_input


def add_head(head_health):
    global HEAD, HEALTH_TARGETED
    HEAD += 1
    HEALTH_TARGETED += head_health


def add_body(body_health):
    global TORSO, HEALTH_TARGETED
    TORSO += 1
    HEALTH_TARGETED += body_health


def add_hand(hand_health):
    global ARMS, HEALTH_TARGETED
    ARMS += 1
    HEALTH_TARGETED += (hand_health / 4)


def add_leg(leg_health):
    global LEGS, HEALTH_TARGETED
    LEGS += 1
    HEALTH_TARGETED += (leg_health / 2)


def remove_hand(hand_health):
    global ARMS, HEALTH_TARGETED
    ARMS -= 1
    HEALTH_TARGETED -= (hand_health / 4)


def remove_leg(leg_health):
    global LEGS, HEALTH_TARGETED
    LEGS -= 1
    HEALTH_TARGETED -= (leg_health / 2)


def attempt_reorder_list_index(titan_target_order, titan_target_health_order):
    arm_index, leg_index = find_arm_index(titan_target_order), find_leg_index(titan_target_order)
    if leg_index < arm_index:
        if titan_target_health_order[leg_index][0] == titan_target_health_order[arm_index][0]:
            if titan_target_health_order[leg_index][1] == titan_target_health_order[arm_index][1]:
                titan_target_order[arm_index], titan_target_order[leg_index] = titan_target_order[leg_index], titan_target_order[arm_index]
                titan_target_health_order[arm_index], titan_target_health_order[leg_index] = titan_target_health_order[leg_index], titan_target_health_order[arm_index]
    return titan_target_order, titan_target_health_order


def return_titan_health_values(titan, titan_parts):
    titan_health_values = []
    for index in range(len(titan_parts)):
        titan_health_values.append(titan[titan_parts[index]])
    return titan_health_values


def titan_part(number):
    if number == 0: return "Head"
    if number == 1: return "Torso"
    if number == 2: return "Arms"
    if number == 3: return "Legs"


def health_armor_ratio(titan):
    titan_parts = list(titan)
    new_values = []
    titan_health_values = return_titan_health_values(titan, titan_parts)
    for index in range(len(titan_parts)):
        values = titan[titan_parts[index]]
        newValue = (values[0] / values[1])
        new_values.append(newValue)
    new_values, titan_target_order, titan_target_health_order = zip(*sorted(zip(new_values, titan_parts, titan_health_values)))
    titan_target_order, titan_target_health_order = list(titan_target_order), list(titan_target_health_order)
    titan_target_order.reverse()
    titan_target_health_order.reverse()
    titan_target_order, titan_target_health_order = attempt_reorder_list_index(titan_target_order, titan_target_health_order)
    return titan_target_order, titan_target_health_order


def sort_titan_targeting_order():
    global titan, titan_max_health
    titan_target_order, titan_target_health_order = health_armor_ratio(titan)
    titan_target_health_order = [health[0] for health in titan_target_health_order]
    return titan_target_order, titan_target_health_order, titan_max_health


def choose_part(titan_target_order, titan_target_health_order):
    global HEAD, TORSO, ARMS, LEGS, HEALTH_TARGETED
    if HEAD == 0 and titan_target_order[0] == "Head": add_head(titan_target_health_order[0])
    elif TORSO == 0 and titan_target_order[0] == "Torso": add_body(titan_target_health_order[0])
    elif HEAD == 0 and titan_target_order[1] == "Head": add_head(titan_target_health_order[1])
    elif TORSO == 0 and titan_target_order[1] == "Torso": add_body(titan_target_health_order[1])
    elif ARMS < 4 and titan_target_order[0] == "Arms": add_hand(titan_target_health_order[0])
    elif ARMS < 4 and titan_target_order[1] == "Arms": add_hand(titan_target_health_order[1])
    elif ARMS < 4 and titan_target_order[2] == "Arms": add_hand(titan_target_health_order[2])
    elif LEGS < 2 and titan_target_order[0] == "Legs": add_leg(titan_target_health_order[0])
    elif LEGS < 2 and titan_target_order[1] == "Legs": add_leg(titan_target_health_order[1])
    elif LEGS < 2 and titan_target_order[2] == "Legs": add_leg(titan_target_health_order[2])
    elif HEAD == 0 and titan_target_order[2] == "Head": add_head(titan_target_health_order[2])
    elif TORSO == 0 and titan_target_order[2] == "Torso": add_body(titan_target_health_order[2])
    elif ARMS < 4 and titan_target_order[3] == "Arms": add_hand(titan_target_health_order[3])
    elif LEGS < 2 and titan_target_order[3] == "Legs": add_leg(titan_target_health_order[3])
    elif HEAD == 0 and titan_target_order[3] == "Head": add_head(titan_target_health_order[3])
    elif TORSO == 0 and titan_target_order[3] == "Torso": add_body(titan_target_health_order[3])


def parts_kill_calculator(titan_target_order, titan_target_health_order, titan_max_health):
    global HEALTH_TARGETED
    while titan_max_health > HEALTH_TARGETED:
        choose_part(titan_target_order, titan_target_health_order)


def try_part_subtract(titan_target_order, titan_target_health_order, titan_max_health):
    global SUBTRACT_LEGS, SUBTRACT_ARMS, HEALTH_TARGETED
    arm_index, leg_index = find_arm_index(titan_target_order), find_leg_index(titan_target_order)
    if SUBTRACT_ARMS and ARMS > 0:
        remove_hand(titan_target_health_order[arm_index])
        if titan_max_health > HEALTH_TARGETED:
            add_hand(titan_target_health_order[arm_index])
            SUBTRACT_ARMS = False
    if SUBTRACT_LEGS and LEGS > 0:
        remove_leg(titan_target_health_order[leg_index])
        if titan_max_health > HEALTH_TARGETED:
            add_leg(titan_target_health_order[leg_index])
            SUBTRACT_LEGS = False


def try_convert_leg_for_arm(titan_target_order, titan_target_health_order, titan_max_health):
    global HEALTH_TARGETED
    arm_index, leg_index = find_arm_index(titan_target_order), find_leg_index(titan_target_order)
    if LEGS > 0 and ARMS < 4:
        remove_leg(titan_target_health_order[leg_index])
        add_hand(titan_target_health_order[arm_index])
        if titan_max_health > HEALTH_TARGETED:
            add_leg(titan_target_health_order[leg_index])
            remove_hand(titan_target_health_order[arm_index])


def main_calculator():
    global HEALTH_TARGETED, HEAD, TORSO, ARMS, LEGS
    titan_target_order, titan_target_health_order, titan_max_health = sort_titan_targeting_order()
    parts_kill_calculator(titan_target_order, titan_target_health_order, titan_max_health)
    for n in range(6):
        try_part_subtract(titan_target_order, titan_target_health_order, titan_max_health)
    for n in range (2):
        try_convert_leg_for_arm(titan_target_order, titan_target_health_order, titan_max_health)
    print_what_to_target()

# this is a test environment
# titan_max_health = 310
# titan = {'Head': [62.0, 62.0], 'Torso': [143.22, 54.25], 'Arms': [62.0, 77.5], 'Legs': [62.0, 77.5]}
titan = {}
titan_max_health = int_or_float_input(text=f"What's the titan's needed health to kill?: ")
for key in range(4):
    partName = titan_part(key)
    titan[partName] = [int_or_float_input(text=f"{partName} Health: "), int_or_float_input(text=f"{partName} Armor: ")]


main_calculator()
input('Press ENTER to exit')