import config
from classes import JumpType
from typing import List

list_of_jumptypes: List[JumpType] = []

# SingleBlock Structures
list_of_jumptypes.append(JumpType(name="1 block straight", structure_type="SingleBlock", 
                                  rel_pos=(1, 0, 0), rel_finish=(1, 0, 0), blocks=[(1, 0, 0, "solid")], 
                                  difficulty=0.1, flow=0.2))