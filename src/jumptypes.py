"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
from classes import JumpType
from classes import Block

def init_startblock(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Start Structure", structure_type="Start", 
                        rel_start_block=Block(block_type, (0, 0, 0)), 
                        rel_finish_block=Block(block_type, (1, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (-1, 0, 1)), Block(block_type, (-1, 0, -1)), 
                                Block(block_type, (-1, 0, 0))],
                        difficulty=0.0, 
                        flow=1.0)
    return b

def init_finishblock(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Finish Structure", structure_type="Finish", 
                        rel_start_block=Block(block_type, (0, 0, 0)), 
                        rel_finish_block=Block(block_type, (1, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (-1, 0, 1)), Block(block_type, (-1, 0, -1)), 
                                Block(block_type, (-1, 0, 0))],
                        difficulty=0.0, 
                        flow=1.0)
    return b

def init_checkpointblock(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Checkpoint Structure", structure_type="Checkpoint", 
                        rel_start_block=Block(block_type, (2, 0, 0)), 
                        rel_finish_block=Block(block_type, (2, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block("minecraft:diamond_block", (1, 0, 0)), Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (2, 0, 1)), Block(block_type, (2, 0, -1)), 
                                Block("minecraft:command_block", (1, -1, 0)), Block("minecraft:stone_pressure_plate", (1, 1, 0))
                                ],
                        difficulty=0.0, 
                        flow=1.0)
    return b

def init_commandcontrol(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Checkpoint Command Blocks Structure", structure_type="CommandControl", 
                        rel_start_block=Block("minecraft:air", (0, 0, 0)), 
                        rel_finish_block=Block("minecraft:air", (0, 0, 0)),
                            blocks=[],
                        difficulty=0.0, 
                        flow=1.0)
    return b

def init_dispenser(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Checkpoint Respawner Item Dispenser", structure_type="CommandControl", 
                                        rel_start_block=Block('minecraft:command_block{Command: "give @p minecraft:fishing_rod"}', (0, 0, 0)), 
                                        rel_finish_block=Block("minecraft:stone_button", (0, 1, 0)),
                                        blocks=[],
                                        difficulty=0.0, 
                                        flow=1.0)
    return b



def init_jumptypes(block_type: str) -> list[JumpType]:
    
    list_of_jumptypes: list[JumpType] = []

    # SingleBlock Structures
    list_of_jumptypes.append(JumpType(name="1 block gap straight", structure_type="SingleBlock",    #
                                    rel_start_block=Block(block_type, (2, 0, 0)),                  #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                 #  +  +
                                    blocks=[],                                                    #
                                    difficulty=0.1, flow=0.2))                                    #

    list_of_jumptypes.append(JumpType(name="2 blocks gap straight", structure_type="SingleBlock",   #
                                    rel_start_block=Block(block_type, (3, 0, 0)),                  #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                 #  +    +
                                    blocks=[],                                                    #
                                    difficulty=0.1, flow=0.7))                                    #

    list_of_jumptypes.append(JumpType(name="3 blocks gap straight", structure_type="SingleBlock",     #
                                    rel_start_block=Block(block_type, (4, 0, 0)),                    #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                   #  +      +
                                    blocks=[],                                                      #
                                    difficulty=0.1, flow=1.0))                                      #

    list_of_jumptypes.append(JumpType(name="4 blocks gap straight", structure_type="SingleBlock",     #
                                    rel_start_block=Block(block_type, (5, 0, 0)),                    #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                   #  +        +
                                    blocks=[],                                                      #
                                    difficulty=0.8, flow=1.0))                                      #

    list_of_jumptypes.append(JumpType(name="2 blocks gap displaced left", structure_type="SingleBlock",    #
                                    rel_start_block=Block(block_type, (3, 0, -1)),                        #       +
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                        #  +
                                    blocks=[],                                                           #
                                    difficulty=0.3, flow=0.8))                                           #

    list_of_jumptypes.append(JumpType(name="2 blocks gap displaced right", structure_type="SingleBlock",    #
                                    rel_start_block=Block(block_type, (3, 0, 1)),                          #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                         #  +
                                    blocks=[],                                                            #       +
                                    difficulty=0.3, flow=0.8))                                            #

    list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal left", structure_type="SingleBlock",  #       +
                                    rel_start_block=Block(block_type, (3, 0, -2)),                     #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                     #  +
                                    blocks=[],                                                        #
                                    difficulty=0.6, flow=0.8))                                        #

    list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal right", structure_type="SingleBlock",  #
                                    rel_start_block=Block(block_type, (3, 0, 2)),                       #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                      #  +
                                    blocks=[],                                                         #
                                    difficulty=0.6, flow=0.8))                                         #       +

    list_of_jumptypes.append(JumpType(name="1 block gap one up", structure_type="SingleBlock",           #
                                    rel_start_block=Block(block_type, (2, 1, 0)),                       #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                      #  +  +
                                    blocks=[],                                                         #
                                    difficulty=0.2, flow=0.5))                                         #

    list_of_jumptypes.append(JumpType(name="2 block gap one up", structure_type="SingleBlock",           #
                                    rel_start_block=Block(block_type, (3, 1, 0)),                       #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                      #  +    +
                                    blocks=[],                                                         #
                                    difficulty=0.9, flow=0.7))                                         #

    list_of_jumptypes.append(JumpType(name="1 block gap one up displaced left", structure_type="SingleBlock",  #
                                    rel_start_block=Block(block_type, (2, 1, -1)),                            #     +
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                            #  +
                                    blocks=[],                                                               #
                                    difficulty=0.3, flow=0.5))                                               #

    list_of_jumptypes.append(JumpType(name="1 block gap one up displaced right", structure_type="SingleBlock", #
                                    rel_start_block=Block(block_type, (2, 1, 1)),                             #
                                    rel_finish_block=Block(block_type, (0, 0, 0)),                            #  +
                                    blocks=[],                                                               #     +
                                    difficulty=0.3, flow=0.5))                                               #



    # TwoBlock Structures
    list_of_jumptypes.append(JumpType(name="1 block gap straight", structure_type="TwoBlock",       #
                                    rel_start_block=Block(block_type, (2, 0, 0)),                  #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                 #  +  ++
                                    blocks=[],                                                    #
                                    difficulty=0.1, flow=0.4))                                    #

    list_of_jumptypes.append(JumpType(name="2 blocks gap straight", structure_type="TwoBlock",      #
                                    rel_start_block=Block(block_type, (3, 0, 0)),                  #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                 #  +    ++
                                    blocks=[],                                                    #
                                    difficulty=0.1, flow=0.8))                                    #

    list_of_jumptypes.append(JumpType(name="3 blocks gap straight", structure_type="TwoBlock",        #
                                    rel_start_block=Block(block_type, (4, 0, 0)),                    #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                   #  +      ++
                                    blocks=[],                                                      #
                                    difficulty=0.1, flow=1.0))                                      #

    list_of_jumptypes.append(JumpType(name="4 blocks gap straight", structure_type="TwoBlock",        #
                                    rel_start_block=Block(block_type, (5, 0, 0)),                    #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                   #  +        ++
                                    blocks=[],                                                      #
                                    difficulty=0.8, flow=1.0))                                      #

    list_of_jumptypes.append(JumpType(name="2 blocks gap displaced left", structure_type="TwoBlock",       #
                                    rel_start_block=Block(block_type, (3, 0, -1)),                        #       ++
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                        #  +
                                    blocks=[],                                                           #
                                    difficulty=0.3, flow=0.8))                                           #

    list_of_jumptypes.append(JumpType(name="2 blocks gap displaced right", structure_type="TwoBlock",       #
                                    rel_start_block=Block(block_type, (3, 0, 1)),                          #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                         #  +
                                    blocks=[],                                                            #       ++
                                    difficulty=0.3, flow=0.8))                                            #

    list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal left", structure_type="TwoBlock",     #       ++
                                    rel_start_block=Block(block_type, (3, 0, -2)),                     #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                     #  +
                                    blocks=[],                                                        #
                                    difficulty=0.6, flow=0.8))                                        #

    list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal right", structure_type="TwoBlock",     #
                                    rel_start_block=Block(block_type, (3, 0, 2)),                       #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                      #  +
                                    blocks=[],                                                         #
                                    difficulty=0.6, flow=0.8))                                         #       ++

    list_of_jumptypes.append(JumpType(name="1 block gap one up", structure_type="TwoBlock",              #
                                    rel_start_block=Block(block_type, (2, 1, 0)),                       #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                      #  +  ++
                                    blocks=[],                                                         #
                                    difficulty=0.2, flow=0.5))                                         #

    list_of_jumptypes.append(JumpType(name="2 block gap one up", structure_type="TwoBlock",              #
                                    rel_start_block=Block(block_type, (3, 1, 0)),                       #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                      #  +    ++
                                    blocks=[],                                                         #
                                    difficulty=0.9, flow=0.7))                                         #

    list_of_jumptypes.append(JumpType(name="1 block gap one up displaced left", structure_type="TwoBlock",     #
                                    rel_start_block=Block(block_type, (2, 1, -1)),                            #     ++
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                            #  +
                                    blocks=[],                                                               #
                                    difficulty=0.3, flow=0.5))                                               #

    list_of_jumptypes.append(JumpType(name="1 block gap one up displaced right", structure_type="TwoBlock",    #
                                    rel_start_block=Block(block_type, (2, 1, 1)),                             #
                                    rel_finish_block=Block(block_type, (1, 0, 0)),                            #  +
                                    blocks=[],                                                               #     ++
                                    difficulty=0.3, flow=0.5))                                               #
    
    return list_of_jumptypes

