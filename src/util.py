"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
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


def shortcut_possible_checker(old_X: int, old_Y: int, old_Z: int, new_X: int, new_Y: int, new_Z: int, check_below: bool, check_same_h: bool, check_above: bool):

    if check_below:            
        # 3 y-levels below (against obstruction of earlier jumps)
        if old_Y == new_Y - 3 and (old_X <= new_X + 3 and old_X >= new_X - 3) and (old_Z <= new_Z + 3 and old_Z >= new_Z - 3):
            return True

        # 2 y-levels below (against obstruction of earlier jumps)
        if old_Y == new_Y - 2 and (old_X <= new_X + 3 and old_X >= new_X - 3) and (old_Z <= new_Z + 3 and old_Z >= new_Z - 3):
            return True

        # One y-level below
        if old_Y == new_Y - 1 and (old_X <= new_X + 4 and old_X >= new_X - 4) and (old_Z <= new_Z + 4 and old_Z >= new_Z - 4):
            return True

    if check_same_h:
        # Same height
        if old_Y == new_Y and (old_X <= new_X + 5 and old_X >= new_X - 5) and (old_Z <= new_Z + 5 and old_Z >= new_Z - 5):
            return True

    if check_above:
        # One y-level up
        if old_Y == new_Y + 1 and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
            return True

        # Rest of the volume above the block in a 12x5x12 volume
        if (old_Y >= new_Y + 2 and old_Y <= new_Y + 7) and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
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

    if "command_block" in new_block.name:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=False, check_above=False):
            return True
    else:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=True, check_above=True):
            return True

    # Check for the rel finish block
    old_X = earlier_structure.rel_finish_block.abs_position[0]
    old_Y = earlier_structure.rel_finish_block.abs_position[1]
    old_Z = earlier_structure.rel_finish_block.abs_position[2]

    if "command_block" in new_block.name:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=False, check_above=False):
            return True
    else:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=True, check_above=True):
            return True

    for block in earlier_structure.blocks:

        old_X = block.abs_position[0]
        old_Y = block.abs_position[1]
        old_Z = block.abs_position[2]

        if "command_block" in new_block.name:
            if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=False, check_above=False):
                return True
        else:
            if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=True, check_above=True):
                return True

    return False


# Returns True only if the Block is inside the minecraft world bounds and the config defined Parkour bounds, else False.
# Also considers the height of the player hitbox, leaving 4 blocks headroom below the maximum y value of the volume.
def in_bounds(block: Block, parkour_volume: list[tuple[int, int]], enforce_parkour_volume: bool, mc_version: str):

    x = block.abs_position[0]
    y = block.abs_position[1]
    z = block.abs_position[2]

    if mc_version == "1.13 - 1.17.1":
        max_y = config.MC_WORLD_MAX_Y_OLD
        min_y = config.MC_WORLD_MIN_Y_OLD
    else:
        max_y = config.MC_WORLD_MAX_Y
        min_y = config.MC_WORLD_MIN_Y

    if x < config.MC_WORLD_MIN_X or x > config.MC_WORLD_MAX_X:
        return False
    if y < min_y or y > max_y:
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

def near_jump(block: Block, earlier_jump: JumpType) -> bool:

    radius = 20
    x = block.abs_position[0]
    y = block.abs_position[1]
    z = block.abs_position[2]
    e_x = earlier_jump.rel_finish_block.abs_position[0]
    e_y = earlier_jump.rel_finish_block.abs_position[1]
    e_z = earlier_jump.rel_finish_block.abs_position[2]

    if abs(x - e_x) < radius and abs(y - e_y) < radius and abs(z - e_z) < radius:
        return True
    
    return False

def can_be_placed(jumptype: JumpType, 
                  current_block_position: tuple[int, int, int], 
                  current_forward_direction: str, 
                  list_of_placed_jumps: list[JumpType],
                  enforce_parkour_volume: bool,
                  parkour_volume: list[tuple[int, int]],
                  mc_version: str):

    abs_position = compute_abs_coordinates_of_start_block(
        jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # Check if new Structure is in bounds of the minecraft world and parkour volume (if enforced)
    if not in_bounds(jumptype.rel_start_block, parkour_volume, enforce_parkour_volume, mc_version):
        return False
    if not in_bounds(jumptype.rel_finish_block, parkour_volume, enforce_parkour_volume, mc_version):
        return False
    for block in jumptype.blocks:
        if not in_bounds(block, parkour_volume, enforce_parkour_volume, mc_version):
            return False
    
    # Check if shortcut possible
    for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:
        # If start block not near earlier jump the no detailed checks necessary
        if not near_jump(jumptype.rel_start_block, earlier_jump):
            continue

        if shortcut_possible(jumptype.rel_start_block, earlier_jump):
            return False
        if shortcut_possible(jumptype.rel_finish_block, earlier_jump):
            return False
        for block in jumptype.blocks:
            if shortcut_possible(block, earlier_jump):
                return False

    return True


def is_ascending(jumptype: JumpType) -> bool:

    if jumptype.rel_start_block.rel_position[1] + jumptype.rel_finish_block.rel_position[1] > 0:
        return True

    return False

def is_descending(jumptype: JumpType) -> bool:

    if jumptype.rel_start_block.rel_position[1] + jumptype.rel_finish_block.rel_position[1] < 0:
        return True

    return False