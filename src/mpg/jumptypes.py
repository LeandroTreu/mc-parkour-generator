"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
from mpg.classes import JumpType
from mpg.classes import Block

def init_startblock(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Start Structure", structure_type="Start", 
                        rel_start_block=Block(block_type, (0, 0, 0)), 
                        rel_finish_block=Block(block_type, (1, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (-1, 0, 1)), Block(block_type, (-1, 0, -1)), 
                                Block(block_type, (-1, 0, 0))],
                        difficulty="easy", 
                        pace="fast")
    return b

def init_finishblock(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Finish Structure", structure_type="Finish", 
                        rel_start_block=Block(block_type, (2, 0, 0)), 
                        rel_finish_block=Block(block_type, (1, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (2, 0, 1)), Block(block_type, (2, 0, -1)), 
                                Block(block_type, (2, 0, 0))],
                        difficulty="easy", 
                        pace="fast")
    return b

def init_checkpointblocks(block_type: str) -> list[JumpType]:
    list_of_jumptypes: list[JumpType] = []
    list_of_jumptypes.append(JumpType(name="Parkour Checkpoint Structure standard", structure_type="Checkpoint", 
                        rel_start_block=Block(block_type, (3, 0, 0)), 
                        rel_finish_block=Block(block_type, (2, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block("minecraft:diamond_block", (1, 0, 0)), Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (2, 0, 1)), Block(block_type, (2, 0, -1)), 
                                Block("minecraft:command_block", (1, -1, 0)), Block("minecraft:stone_pressure_plate", (1, 1, 0))
                                ],
                        difficulty="easy", 
                        pace="fast"))
    list_of_jumptypes.append(JumpType(name="Parkour Checkpoint Structure standard up", structure_type="Checkpoint", 
                        rel_start_block=Block(block_type, (3, 1, 0)), 
                        rel_finish_block=Block(block_type, (2, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block("minecraft:diamond_block", (1, 0, 0)), Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (2, 0, 1)), Block(block_type, (2, 0, -1)), 
                                Block("minecraft:command_block", (1, -1, 0)), Block("minecraft:stone_pressure_plate", (1, 1, 0))
                                ],
                        difficulty="easy", 
                        pace="fast"))
    list_of_jumptypes.append(JumpType(name="Parkour Checkpoint Structure standard down", structure_type="Checkpoint", 
                        rel_start_block=Block(block_type, (3, -1, 0)), 
                        rel_finish_block=Block(block_type, (2, 0, 0)),
                        blocks=[Block(block_type, (0, 0, -1)), Block(block_type, (0, 0, 1)), 
                                Block("minecraft:diamond_block", (1, 0, 0)), Block(block_type, (1, 0, -1)), Block(block_type, (1, 0, 1)), 
                                Block(block_type, (2, 0, 1)), Block(block_type, (2, 0, -1)), 
                                Block("minecraft:command_block", (1, -1, 0)), Block("minecraft:stone_pressure_plate", (1, 1, 0))
                                ],
                        difficulty="easy", 
                        pace="fast"))
    # list_of_jumptypes.append(JumpType(name="Parkour Checkpoint Structure SingleBlock", structure_type="Checkpoint", 
    #                     rel_start_block=Block(block_type, (3, 0, 0)), 
    #                     rel_finish_block=Block(block_type, (0, 0, 0)),
    #                     blocks=[Block("minecraft:diamond_block", (0, 0, 0)), Block("minecraft:command_block", (0, -1, 0)), 
    #                             Block("minecraft:stone_pressure_plate", (0, 1, 0))
    #                             ],
    #                     difficulty="easy", 
    #                     pace="fast"))
    # list_of_jumptypes.append(JumpType(name="Parkour Checkpoint Structure SingleBlock up", structure_type="Checkpoint", 
    #                     rel_start_block=Block(block_type, (3, 1, 0)), 
    #                     rel_finish_block=Block(block_type, (0, 0, 0)),
    #                     blocks=[Block("minecraft:diamond_block", (0, 0, 0)), Block("minecraft:command_block", (0, -1, 0)), 
    #                             Block("minecraft:stone_pressure_plate", (0, 1, 0))
    #                             ],
    #                     difficulty="easy", 
    #                     pace="fast"))
    # list_of_jumptypes.append(JumpType(name="Parkour Checkpoint Structure SingleBlock down", structure_type="Checkpoint", 
    #                     rel_start_block=Block(block_type, (3, -1, 0)), 
    #                     rel_finish_block=Block(block_type, (0, 0, 0)),
    #                     blocks=[Block("minecraft:diamond_block", (0, 0, 0)), Block("minecraft:command_block", (0, -1, 0)), 
    #                             Block("minecraft:stone_pressure_plate", (0, 1, 0))
    #                             ],
    #                     difficulty="easy", 
    #                     pace="fast"))
    return list_of_jumptypes

def init_commandcontrol(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Checkpoint Command Blocks Structure", structure_type="CommandControl", 
                        rel_start_block=Block("minecraft:air", (0, 0, 0)), 
                        rel_finish_block=Block("minecraft:air", (0, 0, 0)),
                            blocks=[],
                        difficulty="easy", 
                        pace="fast")
    return b

def init_dispenser(block_type: str) -> JumpType:
    b = JumpType(name="Parkour Checkpoint Respawner Item Dispenser", structure_type="CommandControl", 
                                        rel_start_block=Block('minecraft:command_block{Command: "give @p minecraft:fishing_rod"}', (0, 0, 0)), 
                                        rel_finish_block=Block("minecraft:stone_button", (0, 1, 0)),
                                        blocks=[],
                                        difficulty="easy", 
                                        pace="fast")
    return b

def init_jumptypes(block_type: str) -> list[JumpType]:
    
    list_of_jumptypes: list[JumpType] = []

    for fw_delta in [2, 3, 4, 5]:
        for y_level in [-3, -2, -1, 0, 1]:
            for lr_delta in [-3, -2, -1, 0, 1, 2, 3]:

                # Non-possible jumps
                if y_level == 1:
                    if fw_delta > 4:
                        continue
                    if fw_delta == 4 and abs(lr_delta) == 3:
                        continue
                if y_level == 0:
                    if abs(lr_delta) == 3 and fw_delta == 5:
                        continue

                # Set difficulty and pace
                if fw_delta == 5:
                    d = "hard"
                    p = "fast"
                elif y_level == 1 and fw_delta > 3:
                    d = "hard"
                    p = "fast"
                elif y_level == 1 and abs(lr_delta) > 2:
                    d = "hard"
                    p = "fast"
                elif fw_delta > 3:
                    d = "medium"
                    p = "fast"
                elif fw_delta == 3 and (abs(lr_delta) > 2 or y_level == 1) and lr_delta != 0:
                    d = "medium"
                    p = "fast"
                elif fw_delta == 2 and abs(lr_delta) <= 2:
                    d = "easy"
                    p = "slow"
                else:
                    d = "easy"
                    p = "fast"

                start_block_tuple = (fw_delta, y_level, lr_delta)
                name = str(start_block_tuple)

                # SingleBlock Structures
                st = "SingleBlock"
                finish_block_tuple = (0, 0, 0)
                blocks = []
                list_of_jumptypes.append(
                    JumpType(name=name, structure_type=st,
                            rel_start_block=Block(block_type, start_block_tuple),
                            rel_finish_block=Block(block_type, finish_block_tuple),
                            blocks=blocks,
                            difficulty=d, pace=p)
                )

                # TwoBlock Structures
                st = "TwoBlock"
                finish_block_tuple = (1, 0, 0)
                blocks = []
                list_of_jumptypes.append(
                    JumpType(name=name, structure_type=st,
                            rel_start_block=Block(block_type, start_block_tuple),
                            rel_finish_block=Block(block_type, finish_block_tuple),
                            blocks=blocks,
                            difficulty=d, pace=p)
                )

                # FourBlock Structures
                st = "FourBlock"
                finish_block_tuple = (1, 0, -1)
                blocks = [Block(block_type, (0, 0, -1)), Block(block_type, (1, 0, 0))]
                list_of_jumptypes.append(
                    JumpType(name=name, structure_type=st,
                            rel_start_block=Block(block_type, start_block_tuple),
                            rel_finish_block=Block(block_type, finish_block_tuple),
                            blocks=blocks,
                            difficulty=d, pace=p)
                )

    return list_of_jumptypes