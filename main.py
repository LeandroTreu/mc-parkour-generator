import config
from classes import JumpType
from jumptypes import list_of_jumptypes
from typing import List
import numpy as np
from numpy.random import default_rng

list_of_placed_jumps: List[JumpType] = []
list_of_candidates: List[JumpType] = []
list_of_allowed_structure_types = ["SingleBlock"]
list_of_directions = ["Xpos", "Xneg", "Zpos", "Zneg"]

def compute_abs_coordinates_of_start_block(jumptype: JumpType, absolut_pos_of_last_block, forward_direction):

    Y = absolut_pos_of_last_block[1] + jumptype.rel_start[1]

    if forward_direction == "Xpos":
        X = absolut_pos_of_last_block[0] + jumptype.rel_start[0]
        Z = absolut_pos_of_last_block[2] + jumptype.rel_start[2]
    elif forward_direction == "Xneg":
        X = absolut_pos_of_last_block[0] - jumptype.rel_start[0]
        Z = absolut_pos_of_last_block[2] - jumptype.rel_start[2]
    elif forward_direction == "Zpos":
        X = absolut_pos_of_last_block[0] + jumptype.rel_start[2]
        Z = absolut_pos_of_last_block[2] + jumptype.rel_start[0]
    elif forward_direction == "Zneg":
        X = absolut_pos_of_last_block[0] - jumptype.rel_start[2]
        Z = absolut_pos_of_last_block[2] - jumptype.rel_start[0]
    
    return (X, Y, Z)

def shortcut_possible(new_block: tuple, earlier_structure: JumpType):

    new_block_abs = new_block[2]
    rel_zone_of_invalid_blocks = []
    abs_zone_of_invalid_blocks = []

    for rel_tuple in rel_zone_of_invalid_blocks:
        abs_tuple = (rel_tuple[0]+new_block_abs[0], rel_tuple[1]+new_block_abs[1], rel_tuple[2]+new_block_abs[2])
        abs_zone_of_invalid_blocks.append(abs_tuple)


    for block in earlier_structure.blocks:
        if block[2] in abs_zone_of_invalid_blocks:
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


    
    



