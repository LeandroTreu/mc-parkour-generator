import config
from classes import JumpType
from jumptypes import list_of_jumptypes
from typing import List

list_of_placed_jumps: List[JumpType] = []
list_of_candidates: List[JumpType] = []
list_of_allowed_structure_types = ["SingleBlock"]

def can_be_placed(jumptype: JumpType):
    return True


for iteration in config.MaxParkourLength:

    for jumptype in list_of_jumptypes:

        if jumptype.structure_type in list_of_allowed_structure_types:
            
            if jumptype.difficulty <= config.Difficulty:

                if jumptype.flow >= config.Flow:

                    if can_be_placed(jumptype):

                        list_of_candidates.add(jumptype)
    
    



