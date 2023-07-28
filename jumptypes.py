import config
from classes import JumpType
from classes import Block
from typing import List

list_of_jumptypes: List[JumpType] = []

# SingleBlock Structures
list_of_jumptypes.append(JumpType(name="1 block gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (2, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)),  # Defined relative to the rel_start_block
                                  blocks=[], 
                                  difficulty=0.1, flow=0.2))

list_of_jumptypes.append(JumpType(name="2 blocks gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (3, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.1, flow=0.7))

list_of_jumptypes.append(JumpType(name="3 blocks gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (4, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.1, flow=1.0))

list_of_jumptypes.append(JumpType(name="4 blocks gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (5, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.8, flow=1.0))