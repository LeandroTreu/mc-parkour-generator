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

    for gap in [2, 3, 4, 5]:
        for y_level in [-3, -2, -1, 0, 1]:
            for displacement in [-3, -2, -1, 0, 1, 2, 3]:

                # Non-possible jumps
                if y_level == 1:
                    if gap > 4:
                        continue
                    if gap == 4 and abs(displacement) == 3:
                        continue
                if y_level == 0:
                    if abs(displacement) == 3 and gap == 5:
                        continue

                # SingleBlock Structures
                start_block_tuple = (gap, y_level, displacement)
                name = str(start_block_tuple)
                st = "SingleBlock"
                finish_block_tuple = (0, 0, 0)
                blocks = []
                d = 0.5
                f = 0.5
                list_of_jumptypes.append(
                    JumpType(name=name, structure_type=st,
                            rel_start_block=Block(block_type, start_block_tuple),
                            rel_finish_block=Block(block_type, finish_block_tuple),
                            blocks=blocks,
                            difficulty=d, flow=f)
                )

                # TwoBlock Structures
                start_block_tuple = (gap, y_level, displacement)
                name = str(start_block_tuple)
                st = "TwoBlock"
                finish_block_tuple = (1, 0, 0)
                blocks = []
                d = 0.5
                f = 0.5
                list_of_jumptypes.append(
                    JumpType(name=name, structure_type=st,
                            rel_start_block=Block(block_type, start_block_tuple),
                            rel_finish_block=Block(block_type, finish_block_tuple),
                            blocks=blocks,
                            difficulty=d, flow=f)
                )

                # FourBlock Structures
                start_block_tuple = (gap, y_level, displacement)
                name = str(start_block_tuple)
                st = "FourBlock"
                finish_block_tuple = (1, 0, 0)
                blocks = [Block(block_type, (0, 0, -1)), Block(block_type, (1, 0, -1))]
                d = 0.5
                f = 0.5
                list_of_jumptypes.append(
                    JumpType(name=name, structure_type=st,
                            rel_start_block=Block(block_type, start_block_tuple),
                            rel_finish_block=Block(block_type, finish_block_tuple),
                            blocks=blocks,
                            difficulty=d, flow=f)
                )

    return list_of_jumptypes