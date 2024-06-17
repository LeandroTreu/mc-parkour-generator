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

    def __init__(self, name: str, structure_type: str, rel_start_block: Block, rel_finish_block: Block, blocks: list[Block], difficulty: float, flow: float) -> None:
        
        self.name = name                            # Name of the jump type
        self.structure_type = structure_type        # Name of the structure type
        self.rel_start_block = rel_start_block      # Start block of the JumpType: Its relative position is defined relative to the last jump block in the parkour
        self.rel_finish_block = rel_finish_block    # Finish block of the JumpType, defined relative to the start block of this JumpType
        self.blocks = blocks                        # List of all remaining blocks in the structure (excluding the rel_start_block and the rel_finish_block) defined relative to the start block of this JumpType
        
        self.difficulty = difficulty
        self.flow = flow
    
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
        