from classes import JumpType, Block
import config

def compute_abs_coordinates_of_start_block(jumptype: JumpType, absolut_pos_of_last_block: tuple[int, int, int], forward_direction: str):

    y = absolut_pos_of_last_block[1] + jumptype.rel_start_block.rel_position[1]

    if forward_direction == "Xpos":
        x = absolut_pos_of_last_block[0] + \
            jumptype.rel_start_block.rel_position[0]
        z = absolut_pos_of_last_block[2] + \
            jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Xneg":
        x = absolut_pos_of_last_block[0] - \
            jumptype.rel_start_block.rel_position[0]
        z = absolut_pos_of_last_block[2] - \
            jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Zpos":
        x = absolut_pos_of_last_block[0] + \
            jumptype.rel_start_block.rel_position[2]
        z = absolut_pos_of_last_block[2] + \
            jumptype.rel_start_block.rel_position[0]
    else:
        x = absolut_pos_of_last_block[0] - \
            jumptype.rel_start_block.rel_position[2]
        z = absolut_pos_of_last_block[2] - \
            jumptype.rel_start_block.rel_position[0]

    return (x, y, z)


def shortcut_possible_checker(old_X: int, old_Y: int, old_Z: int, new_X: int, new_Y: int, new_Z: int):

    # 3 y-levels below (against obstruction of earlier jumps)
    if old_Y == new_Y - 3 and (old_X <= new_X + 3 and old_X >= new_X - 3) and (old_Z <= new_Z + 3 and old_Z >= new_Z - 3):
        return True

    # 2 y-levels below (against obstruction of earlier jumps)
    if old_Y == new_Y - 2 and (old_X <= new_X + 3 and old_X >= new_X - 3) and (old_Z <= new_Z + 3 and old_Z >= new_Z - 3):
        return True

    # One y-level below
    if old_Y == new_Y - 1 and (old_X <= new_X + 4 and old_X >= new_X - 4) and (old_Z <= new_Z + 4 and old_Z >= new_Z - 4):
        return True

    # Same height
    if old_Y == new_Y and (old_X <= new_X + 5 and old_X >= new_X - 5) and (old_Z <= new_Z + 5 and old_Z >= new_Z - 5):
        return True

    # One y-level up
    if old_Y == new_Y + 1 and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
        return True

    # Rest of the volume above the block in a 16x10x16 volume
    if (old_Y >= new_Y + 2 and old_Y <= new_Y + 12) and (old_X <= new_X + 8 and old_X >= new_X - 8) and (old_Z <= new_Z + 8 and old_Z >= new_Z - 8):
        return True

    return False


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


# Returns True only if the Block is inside the minecraft world bounds and the config defined Parkour bounds, else False.
# Also considers the height of the player hitbox, leaving 4 blocks headroom below the maximum y value of the volume.
def in_bounds(block: Block, parkour_volume: list[tuple[int, int]], enforce_parkour_volume: bool):

    x = block.abs_position[0]
    y = block.abs_position[1]
    z = block.abs_position[2]

    if x < config.MC_WORLD_MIN_X or x > config.MC_WORLD_MAX_X:
        return False
    if y < config.MC_WORLD_MIN_Y or y > config.MC_WORLD_MAX_Y:
        return False
    if z < config.MC_WORLD_MIN_Z or z > config.MC_WORLD_MAX_Z:
        return False

    if enforce_parkour_volume:
        if x < parkour_volume[0][0] or x > parkour_volume[0][1]:
            return False
        if y < parkour_volume[1][0] or y > parkour_volume[1][1] - 4:
            return False
        if z < parkour_volume[2][0] or z > parkour_volume[2][1]:
            return False

    return True


def can_be_placed(jumptype: JumpType, 
                  current_block_position: tuple[int, int, int], 
                  current_forward_direction: str, 
                  list_of_placed_jumps: list[JumpType],
                  enforce_parkour_volume: bool,
                  parkour_volume: list[tuple[int, int]]):

    abs_position = compute_abs_coordinates_of_start_block(
        jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # Check if new Structure is in bounds of the minecraft world and parkour volume (if enforced)
    if not in_bounds(jumptype.rel_start_block, parkour_volume, enforce_parkour_volume):
        return False
    if not in_bounds(jumptype.rel_finish_block, parkour_volume, enforce_parkour_volume):
        return False
    for block in jumptype.blocks:
        if not in_bounds(block, parkour_volume, enforce_parkour_volume):
            return False
    
    # TODO: quick check here if jumptype is even near earlier jump

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


def is_Ascending(jumptype: JumpType) -> bool:

    # TODO: also for rel_finish_block of more complex structures
    if jumptype.rel_start_block.rel_position[1] > 0:
        return True

    return False
