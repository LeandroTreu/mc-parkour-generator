"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
import mpg.config

class Block:

    def __init__(self, name: str, rel_position: tuple[int, int, int]) -> None:
        
        self.name = name                    # Minecraft block name
        self.rel_position = rel_position    # Relative position to last jump block in parkour
        self.abs_position: tuple[int, int, int] = (0, 0, 0)       # Absolute coordinates in the minecraft world

    def __str__(self) -> str:
        
        printstr = {
            "name": self.name,
            "rel_position": self.rel_position,
            "abs_position": self.abs_position
        }

        return str(printstr)
    
    def set_abs_position(self, abs_coordinates: tuple[int, int, int]):

        self.abs_position = abs_coordinates

class JumpType:

    def __init__(self, name: str, structure_type: str, rel_start_block: Block, rel_finish_block: Block, blocks: list[Block], difficulty: str, pace: str) -> None:
        
        self.name = name                            # Name of the jump type
        self.structure_type = structure_type        # Name of the structure type
        self.rel_start_block = rel_start_block      # Start block of the JumpType: Its relative position is defined relative to the last jump block in the parkour
        self.rel_finish_block = rel_finish_block    # Finish block of the JumpType, defined relative to the start block of this JumpType
        self.blocks = blocks                        # List of all remaining blocks in the structure (excluding the rel_start_block and the rel_finish_block) defined relative to the start block of this JumpType
        
        self.difficulty = difficulty
        self.pace = pace
    
    def __str__(self) -> str:
        
        printstr = f"name: {self.name} \nstructure_type: {self.structure_type} \nrel_start_block: {str(self.rel_start_block)} \nrel_finish_block: {str(self.rel_finish_block)} \nblocks: {[str(b) for b in self.blocks]}"
                    

        return "\n"+str(printstr)
    
    def set_absolut_coordinates(self, abs_tuple: tuple[int, int, int], forward_direction: str):

        self.rel_start_block.set_abs_position(abs_tuple)

        # For finish block
        abs_coordinates = self.compute_abs_coordinates(self.rel_start_block.abs_position, self.rel_finish_block, forward_direction)
        self.rel_finish_block.set_abs_position(abs_coordinates)

        for block in self.blocks:

            abs_coordinates = self.compute_abs_coordinates(self.rel_start_block.abs_position, block, forward_direction)
            block.set_abs_position(abs_coordinates)

        return
    
    def compute_abs_coordinates(self, abs_start_block: tuple[int, int, int], relative_block: Block, forward_direction: str) -> tuple[int, int, int]:
        
        y = abs_start_block[1] + relative_block.rel_position[1]

        if forward_direction == "Xpos":
            x = abs_start_block[0] + relative_block.rel_position[0]
            z = abs_start_block[2] + relative_block.rel_position[2]
        elif forward_direction == "Xneg":
            x = abs_start_block[0] - relative_block.rel_position[0]
            z = abs_start_block[2] - relative_block.rel_position[2]
        elif forward_direction == "Zpos":
            x = abs_start_block[0] + relative_block.rel_position[2]
            z = abs_start_block[2] + relative_block.rel_position[0]
        else:
            x = abs_start_block[0] - relative_block.rel_position[2]
            z = abs_start_block[2] - relative_block.rel_position[0]
        
        return (x, y, z)

class Cluster():

    def __init__(self, jumps: list[JumpType]):

        self.jumps: list[JumpType] = jumps
        self.volume = self.calculate_volume()
    
    def calculate_volume(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:

        x_min = mpg.config.MC_WORLD_MAX_X
        x_max = mpg.config.MC_WORLD_MIN_X
        y_min = mpg.config.MC_WORLD_MAX_Y
        y_max = mpg.config.MC_WORLD_MIN_Y
        z_min = mpg.config.MC_WORLD_MAX_Z
        z_max = mpg.config.MC_WORLD_MIN_Z

        if len(self.jumps) == 0:
            return ((x_min, x_max), (y_min, y_max), (z_min, z_max))

        for jump in self.jumps:
            if len(jump.blocks) > 0:
                blocks_x_min = min([b.abs_position[0] for b in jump.blocks])
                blocks_y_min = min([b.abs_position[1] for b in jump.blocks])
                blocks_z_min = min([b.abs_position[2] for b in jump.blocks])
                blocks_x_max = max([b.abs_position[0] for b in jump.blocks])
                blocks_y_max = max([b.abs_position[1] for b in jump.blocks])
                blocks_z_max = max([b.abs_position[2] for b in jump.blocks])
            else:
                blocks_x_min = mpg.config.MC_WORLD_MAX_X
                blocks_y_min = mpg.config.MC_WORLD_MAX_Y
                blocks_z_min = mpg.config.MC_WORLD_MAX_Z
                blocks_x_max = mpg.config.MC_WORLD_MIN_X
                blocks_y_max = mpg.config.MC_WORLD_MIN_Y
                blocks_z_max = mpg.config.MC_WORLD_MIN_Z
                
            jump_x_min = min([jump.rel_start_block.abs_position[0], jump.rel_finish_block.abs_position[0], blocks_x_min])
            jump_y_min = min([jump.rel_start_block.abs_position[1], jump.rel_finish_block.abs_position[1], blocks_y_min])
            jump_z_min = min([jump.rel_start_block.abs_position[2], jump.rel_finish_block.abs_position[2], blocks_z_min])
            jump_x_max = max([jump.rel_start_block.abs_position[0], jump.rel_finish_block.abs_position[0], blocks_x_max])
            jump_y_max = max([jump.rel_start_block.abs_position[1], jump.rel_finish_block.abs_position[1], blocks_y_max])
            jump_z_max = max([jump.rel_start_block.abs_position[2], jump.rel_finish_block.abs_position[2], blocks_z_max])

            x_min = min(x_min, jump_x_min)
            y_min = min(y_min, jump_y_min)
            z_min = min(z_min, jump_z_min)
            x_max = max(x_max, jump_x_max)
            y_max = max(y_max, jump_y_max)
            z_max = max(z_max, jump_z_max)
        
        # Add margins because of the shortcut checker
        x_min = x_min - 6
        y_min = y_min - 3
        z_min = z_min - 6
        x_max = x_max + 6
        y_max = y_max + 7
        z_max = z_max + 6

        return ((x_min, x_max), (y_min, y_max), (z_min, z_max))
    
    def insert_jump(self, jump: JumpType):
        self.jumps.append(jump)
        self.volume = self.calculate_volume()
    
    def remove_jumps(self, start_index: int, end_index: int):
        del self.jumps[start_index:end_index]
