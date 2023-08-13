import config
from classes import JumpType, Block

def compute_abs_coordinates_of_start_block(jumptype: JumpType, absolut_pos_of_last_block, forward_direction):

    Y = absolut_pos_of_last_block[1] + jumptype.rel_start_block.rel_position[1]

    if forward_direction == "Xpos":
        X = absolut_pos_of_last_block[0] + jumptype.rel_start_block.rel_position[0]
        Z = absolut_pos_of_last_block[2] + jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Xneg":
        X = absolut_pos_of_last_block[0] - jumptype.rel_start_block.rel_position[0]
        Z = absolut_pos_of_last_block[2] - jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Zpos":
        X = absolut_pos_of_last_block[0] + jumptype.rel_start_block.rel_position[2]
        Z = absolut_pos_of_last_block[2] + jumptype.rel_start_block.rel_position[0]
    elif forward_direction == "Zneg":
        X = absolut_pos_of_last_block[0] - jumptype.rel_start_block.rel_position[2]
        Z = absolut_pos_of_last_block[2] - jumptype.rel_start_block.rel_position[0]
    
    return (X, Y, Z)


def shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):

     # First zone, one y-level below
        if old_Y == new_Y - 1 and (old_X <= new_X + 2 and old_X >= new_X - 2) and (old_Z <= new_Z + 2 and old_Z >= new_Z - 2):
            return True
        
        # Same height
        if old_Y == new_Y and (old_X <= new_X + 4 and old_X >= new_X - 4) and (old_Z <= new_Z + 4 and old_Z >= new_Z - 4):
            return True

        # One y-level up
        if old_Y == new_Y + 1 and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
            return True

        # Rest of the volume above the block in a 16x10x16 volume
        if (old_Y <= new_Y + 12 and old_Y >= new_Y + 2) and (old_X <= new_X + 8 and old_X >= new_X - 8) and (old_Z <= new_Z + 8 and old_Z >= new_Z - 8):
            return True


def shortcut_possible(new_block: Block, earlier_structure: JumpType):

    new_block_abs = new_block.abs_position

    new_X = new_block_abs[0]
    new_Y = new_block_abs[1]
    new_Z = new_block_abs[2]

    # Check for the rel start block
    old_X = earlier_structure.rel_start_block.abs_position[0]
    old_Y = earlier_structure.rel_start_block.abs_position[1]
    old_Z = earlier_structure.rel_start_block.abs_position[2]

    if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):
        return True
    
    # Check for the rel finish block
    old_X = earlier_structure.rel_finish_block.abs_position[0]
    old_Y = earlier_structure.rel_finish_block.abs_position[1]
    old_Z = earlier_structure.rel_finish_block.abs_position[2]

    if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):
        return True

    for block in earlier_structure.blocks:

        old_X = block.abs_position[0]
        old_Y = block.abs_position[1]
        old_Z = block.abs_position[2]

        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):
            return True
    
    return False


# Returns True only if the Block is in the config defined Parkour bounds, else False
def in_bounds(block: Block):
    
    # X coordinate
    if block.abs_position[0] >= config.ParkourVolume[0][0] and block.abs_position[0] <= config.ParkourVolume[0][1]:
        # Y coordinate
        if block.abs_position[1] >= config.ParkourVolume[1][0] and block.abs_position[1] <= config.ParkourVolume[1][1]:
            # Z coordinate
            if block.abs_position[2] >= config.ParkourVolume[2][0] and block.abs_position[2] <= config.ParkourVolume[2][1]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def can_be_placed(jumptype: JumpType, current_block_position: tuple, current_forward_direction: str, list_of_placed_jumps: list):

    abs_position = compute_abs_coordinates_of_start_block(jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # Check if new Structure is in bounds of the config.ParkourVolume
    if config.EnforceParkourVolume:

        if not in_bounds(jumptype.rel_start_block):
            return False
        if not in_bounds(jumptype.rel_finish_block):
            return False
        for block in jumptype.blocks:

            if not in_bounds(block):
                return False


    # For start and finish blocks
    for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:

            if shortcut_possible(jumptype.rel_start_block, earlier_jump):
                
                return False
            if shortcut_possible(jumptype.rel_finish_block, earlier_jump):
                
                return False
    
    # For rest of the structure
    for block in jumptype.blocks:
        for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:

            if shortcut_possible(block, earlier_jump):
                
                return False

        
    return True


def is_Ascending(jumptype: JumpType):

    if jumptype.rel_start_block.rel_position[1] > 0:
        return True

    return False


