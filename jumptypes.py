import config
from classes import JumpType
from classes import Block
from typing import List
from config import BlockType

StartBlock = JumpType(name="Parkour Start Structure", structure_type="Start", 
                      rel_start_block=Block(BlockType, (0, 0, 0)), 
                      rel_finish_block=Block(BlockType, (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (-1, 0, 1)), Block(BlockType, (-1, 0, -1)), 
                              Block(BlockType, (-1, 0, 0))],
                      difficulty=0.0, 
                      flow=1.0)
FinishBlock = JumpType(name="Parkour Finish Structure", structure_type="Finish", 
                      rel_start_block=Block(BlockType, (0, 0, 0)), 
                      rel_finish_block=Block(BlockType, (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (-1, 0, 1)), Block(BlockType, (-1, 0, -1)), 
                              Block(BlockType, (-1, 0, 0))],
                      difficulty=0.0, 
                      flow=1.0)
CheckpointBlock = JumpType(name="Parkour Checkpoint Structure", structure_type="Checkpoint", 
                      rel_start_block=Block(BlockType, (2, 0, 0)), 
                      rel_finish_block=Block(BlockType, (2, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block("minecraft:diamond_block", (1, 0, 0)), Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (2, 0, 1)), Block(BlockType, (2, 0, -1)), 
                              Block("minecraft:command_block", (1, -1, 0)), Block("minecraft:light_pressureplate", (1, 1, 0))
                              ],
                      difficulty=0.0, 
                      flow=1.0)

list_of_jumptypes: List[JumpType] = []

# SingleBlock Structures
list_of_jumptypes.append(JumpType(name="1 block gap straight", structure_type="SingleBlock",    #
                                  rel_start_block=Block(BlockType, (2, 0, 0)),                  #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                 #  +  +
                                  blocks=[],                                                    #
                                  difficulty=0.1, flow=0.2))                                    #

list_of_jumptypes.append(JumpType(name="2 blocks gap straight", structure_type="SingleBlock",   #
                                  rel_start_block=Block(BlockType, (3, 0, 0)),                  #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                 #  +    +
                                  blocks=[],                                                    #
                                  difficulty=0.1, flow=0.7))                                    #

list_of_jumptypes.append(JumpType(name="3 blocks gap straight", structure_type="SingleBlock",     #
                                  rel_start_block=Block(BlockType, (4, 0, 0)),                    #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                   #  +      +
                                  blocks=[],                                                      #
                                  difficulty=0.1, flow=1.0))                                      #

list_of_jumptypes.append(JumpType(name="4 blocks gap straight", structure_type="SingleBlock",     #
                                  rel_start_block=Block(BlockType, (5, 0, 0)),                    #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                   #  +        +
                                  blocks=[],                                                      #
                                  difficulty=0.8, flow=1.0))                                      #

list_of_jumptypes.append(JumpType(name="2 blocks gap displaced left", structure_type="SingleBlock",    #
                                  rel_start_block=Block(BlockType, (3, 0, -1)),                        #       +
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                        #  +
                                  blocks=[],                                                           #
                                  difficulty=0.3, flow=0.8))                                           #

list_of_jumptypes.append(JumpType(name="2 blocks gap displaced right", structure_type="SingleBlock",    #
                                  rel_start_block=Block(BlockType, (3, 0, 1)),                          #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                         #  +
                                  blocks=[],                                                            #       +
                                  difficulty=0.3, flow=0.8))                                            #

list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal left", structure_type="SingleBlock",  #       +
                                  rel_start_block=Block(BlockType, (3, 0, -2)),                     #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                     #  +
                                  blocks=[],                                                        #
                                  difficulty=0.6, flow=0.8))                                        #

list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal right", structure_type="SingleBlock",  #
                                  rel_start_block=Block(BlockType, (3, 0, 2)),                       #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                      #  +
                                  blocks=[],                                                         #
                                  difficulty=0.6, flow=0.8))                                         #       +

list_of_jumptypes.append(JumpType(name="1 block gap one up", structure_type="SingleBlock",           #
                                  rel_start_block=Block(BlockType, (2, 1, 0)),                       #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                      #  +  +
                                  blocks=[],                                                         #
                                  difficulty=0.2, flow=0.5))                                         #

list_of_jumptypes.append(JumpType(name="2 block gap one up", structure_type="SingleBlock",           #
                                  rel_start_block=Block(BlockType, (3, 1, 0)),                       #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                      #  +    +
                                  blocks=[],                                                         #
                                  difficulty=0.9, flow=0.7))                                         #

list_of_jumptypes.append(JumpType(name="1 block gap one up displaced left", structure_type="SingleBlock",  #
                                  rel_start_block=Block(BlockType, (2, 1, -1)),                            #     +
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                            #  +
                                  blocks=[],                                                               #
                                  difficulty=0.3, flow=0.5))                                               #

list_of_jumptypes.append(JumpType(name="1 block gap one up displaced right", structure_type="SingleBlock", #
                                  rel_start_block=Block(BlockType, (2, 1, 1)),                             #
                                  rel_finish_block=Block(BlockType, (0, 0, 0)),                            #  +
                                  blocks=[],                                                               #     +
                                  difficulty=0.3, flow=0.5))                                               #



# TwoBlock Structures
list_of_jumptypes.append(JumpType(name="1 block gap straight", structure_type="TwoBlock",       #
                                  rel_start_block=Block(BlockType, (2, 0, 0)),                  #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                 #  +  ++
                                  blocks=[],                                                    #
                                  difficulty=0.1, flow=0.4))                                    #

list_of_jumptypes.append(JumpType(name="2 blocks gap straight", structure_type="TwoBlock",      #
                                  rel_start_block=Block(BlockType, (3, 0, 0)),                  #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                 #  +    ++
                                  blocks=[],                                                    #
                                  difficulty=0.1, flow=0.8))                                    #

list_of_jumptypes.append(JumpType(name="3 blocks gap straight", structure_type="TwoBlock",        #
                                  rel_start_block=Block(BlockType, (4, 0, 0)),                    #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                   #  +      ++
                                  blocks=[],                                                      #
                                  difficulty=0.1, flow=1.0))                                      #

list_of_jumptypes.append(JumpType(name="4 blocks gap straight", structure_type="TwoBlock",        #
                                  rel_start_block=Block(BlockType, (5, 0, 0)),                    #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                   #  +        ++
                                  blocks=[],                                                      #
                                  difficulty=0.8, flow=1.0))                                      #

list_of_jumptypes.append(JumpType(name="2 blocks gap displaced left", structure_type="TwoBlock",       #
                                  rel_start_block=Block(BlockType, (3, 0, -1)),                        #       ++
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                        #  +
                                  blocks=[],                                                           #
                                  difficulty=0.3, flow=0.8))                                           #

list_of_jumptypes.append(JumpType(name="2 blocks gap displaced right", structure_type="TwoBlock",       #
                                  rel_start_block=Block(BlockType, (3, 0, 1)),                          #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                         #  +
                                  blocks=[],                                                            #       ++
                                  difficulty=0.3, flow=0.8))                                            #

list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal left", structure_type="TwoBlock",     #       ++
                                  rel_start_block=Block(BlockType, (3, 0, -2)),                     #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                     #  +
                                  blocks=[],                                                        #
                                  difficulty=0.6, flow=0.8))                                        #

list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal right", structure_type="TwoBlock",     #
                                  rel_start_block=Block(BlockType, (3, 0, 2)),                       #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                      #  +
                                  blocks=[],                                                         #
                                  difficulty=0.6, flow=0.8))                                         #       ++

list_of_jumptypes.append(JumpType(name="1 block gap one up", structure_type="TwoBlock",              #
                                  rel_start_block=Block(BlockType, (2, 1, 0)),                       #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                      #  +  ++
                                  blocks=[],                                                         #
                                  difficulty=0.2, flow=0.5))                                         #

list_of_jumptypes.append(JumpType(name="2 block gap one up", structure_type="TwoBlock",              #
                                  rel_start_block=Block(BlockType, (3, 1, 0)),                       #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                      #  +    ++
                                  blocks=[],                                                         #
                                  difficulty=0.9, flow=0.7))                                         #

list_of_jumptypes.append(JumpType(name="1 block gap one up displaced left", structure_type="TwoBlock",     #
                                  rel_start_block=Block(BlockType, (2, 1, -1)),                            #     ++
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                            #  +
                                  blocks=[],                                                               #
                                  difficulty=0.3, flow=0.5))                                               #

list_of_jumptypes.append(JumpType(name="1 block gap one up displaced right", structure_type="TwoBlock",    #
                                  rel_start_block=Block(BlockType, (2, 1, 1)),                             #
                                  rel_finish_block=Block(BlockType, (1, 0, 0)),                            #  +
                                  blocks=[],                                                               #     ++
                                  difficulty=0.3, flow=0.5))                                               #

