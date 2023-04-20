import config

class JumpType:

    def __init__(self, name: str, structure_type: str, rel_start: tuple, rel_finish: tuple, blocks: list, difficulty: float, flow: float) -> None:
        
        self.name = name
        self.structure_type = structure_type
        self.rel_start = rel_start
        self.rel_finish = rel_finish
        self.blocks = blocks
        
        self.difficulty = difficulty
        self.flow = flow

        self.absolute_coordinates_of_start_block = (0, 0, 0)
    
    def set_absolut_coordinates(self, abs_tuple: tuple):

        self.absolute_coordinates_of_start_block = abs_tuple

        for block in self.blocks:

            abs_coordinates = self.compute_abs_coordinates(self.absolute_coordinates_of_start_block, block)
            block.append(abs_coordinates)

        return
    
    def compute_abs_coordinates(self, start_block, relative_block):
        pass
        