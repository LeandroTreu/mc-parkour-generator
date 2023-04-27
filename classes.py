import config

class Block:

    def __init__(self, name: str, rel_position: tuple) -> None:
        
        self.name = name                    # Minecraft block name
        self.rel_position = rel_position    # Relative position to last jump block in parkour
        self.abs_position = (0, 0, 0)       # Absolute coordinates in the minecraft world
    
    def set_abs_position(self, abs_coordinates: tuple):

        self.abs_position = abs_coordinates

class JumpType:

    def __init__(self, name: str, structure_type: str, rel_start_block: Block, rel_finish_block: Block, blocks: list[Block], difficulty: float, flow: float) -> None:
        
        self.name = name                            # Name of the jump type
        self.structure_type = structure_type        # Name of the structure type
        self.rel_start_block = rel_start_block      # Start block of the JumpType: Its relative position is defined relative to the last jump block in the parkour
        self.rel_finish_block = rel_finish_block    # Finish block of the JumpType, defined relative to the start block of this JumpType
        self.blocks = blocks                        # List of all blocks in the structure, except the rel_start_block, defined relative to the start block of this JumpType
        
        self.difficulty = difficulty
        self.flow = flow
    
    def set_absolut_coordinates(self, abs_tuple: tuple, forward_direction: str):

        self.rel_start_block.set_abs_position(abs_tuple)

        for block in self.blocks:

            abs_coordinates = self.compute_abs_coordinates(self.rel_start_block.abs_position, block, forward_direction)
            block.set_abs_position(abs_coordinates)

        return
    
    def compute_abs_coordinates(self, abs_start_block: tuple, relative_block: Block, forward_direction: str):
        
        Y = abs_start_block[1] + relative_block.rel_position[1]

        if forward_direction == "Xpos":
            X = abs_start_block[0] + relative_block.rel_position[0]
            Z = abs_start_block[2] + relative_block.rel_position[2]
        elif forward_direction == "Xneg":
            X = abs_start_block[0] - relative_block.rel_position[0]
            Z = abs_start_block[2] - relative_block.rel_position[2]
        elif forward_direction == "Zpos":
            X = abs_start_block[0] + relative_block.rel_position[2]
            Z = abs_start_block[2] + relative_block.rel_position[0]
        elif forward_direction == "Zneg":
            X = abs_start_block[0] - relative_block.rel_position[2]
            Z = abs_start_block[2] - relative_block.rel_position[0]
        
        return (X, Y, Z)
        