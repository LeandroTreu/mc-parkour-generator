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
        
        self.name = name
        self.structure_type = structure_type
        self.rel_start_block = rel_start_block
        self.rel_finish_block = rel_finish_block
        self.blocks = blocks
        
        self.difficulty = difficulty
        self.flow = flow
    
    def set_absolut_coordinates(self, abs_tuple: tuple):

        self.rel_start_block.set_abs_position(abs_tuple)

        for block in self.blocks:

            abs_coordinates = self.compute_abs_coordinates(self.rel_start_block.abs_position, block)
            block.set_abs_position(abs_coordinates)

        return
    
    def compute_abs_coordinates(self, abs_start_block: tuple, relative_block: Block):
        pass
        