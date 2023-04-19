import config

class JumpType:

    def __init__(self, name: str, rel_pos: tuple, blocks: list, volume: tuple, difficulty: float, flow: float) -> None:
        
        self.name = name
        self.rel_pos = rel_pos
        self.blocks = blocks
        self.volume = volume
        self.difficulty = difficulty
        self.flow = flow