import config
from classes import JumpType
from jumptypes import list_of_jumptypes
from typing import List
import numpy as np
from numpy.random import default_rng

list_of_placed_jumps: List[JumpType] = []
list_of_candidates: List[JumpType] = []
list_of_allowed_structure_types = ["SingleBlock"]

def compute_abs_coordinates_of_start_block(jumptype: JumpType, absolut_pos_of_last_block):

    abs_pos_of_start_block = (0, 0, 0)
    
    return abs_pos_of_start_block

def shortcut_possible(new_block: tuple, earlier_structure: JumpType):

    
    
    return True

def can_be_placed(jumptype: JumpType, current_block_position):

    abs_position = compute_abs_coordinates_of_start_block(jumptype, current_block_position)

    jumptype.set_absolut_coordinates()

    for block in jumptype.blocks:
        for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:

            if shortcut_possible(block, earlier_jump):
                
                return False

        
    return True


current_block_position = (0, 0, 0)

for iteration in config.MaxParkourLength:

    for jumptype in list_of_jumptypes:

        if jumptype.structure_type in list_of_allowed_structure_types:
            
            if jumptype.difficulty <= config.Difficulty:

                if jumptype.flow >= config.Flow:

                    if can_be_placed(jumptype, current_block_position):

                        list_of_candidates.add(jumptype)
    
    
    rng = default_rng(12345)
    random_index = rng.integers(low=0, high=len(list_of_candidates), size=1)
    print(random_index)

    list_of_placed_jumps.add(list_of_candidates[random_index])


    
    



