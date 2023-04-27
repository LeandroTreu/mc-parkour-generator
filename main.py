import config
from classes import JumpType
from classes import Block
from jumptypes import list_of_jumptypes
from typing import List
import numpy as np
from numpy.random import default_rng

list_of_placed_jumps: List[JumpType] = []
list_of_candidates: List[JumpType] = []
list_of_allowed_structure_types = ["SingleBlock"]
list_of_directions = ["Xpos", "Xneg", "Zpos", "Zneg"]

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

def shortcut_possible(new_block: Block, earlier_structure: JumpType):

    new_block_abs = new_block.abs_position

    for block in earlier_structure.blocks:

        old_X = block.abs_position[0]
        old_Y = block.abs_position[1]
        old_Z = block.abs_position[2]

        new_X = new_block_abs[0]
        new_Y = new_block_abs[1]
        new_Z = new_block_abs[2]

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
    
    return False

def can_be_placed(jumptype: JumpType, current_block_position, current_forward_direction):

    abs_position = compute_abs_coordinates_of_start_block(jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position)

    for block in jumptype.blocks:
        for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:

            if shortcut_possible(block, earlier_jump):
                
                return False

        
    return True


current_block_position = (0, 0, 0)
current_forward_direction = "Xpos"

for iteration in config.MaxParkourLength:

    for jumptype in list_of_jumptypes:

        if jumptype.structure_type in list_of_allowed_structure_types:
            
            if jumptype.difficulty <= config.Difficulty:

                if jumptype.flow >= config.Flow:

                    if can_be_placed(jumptype, current_block_position, current_forward_direction):

                        list_of_candidates.append(jumptype)
    
    
    rng = default_rng(12345)
    random_index = rng.integers(low=0, high=len(list_of_candidates), size=1)
    print(random_index)

    list_of_placed_jumps.append(list_of_candidates[random_index])


    
    



