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
        