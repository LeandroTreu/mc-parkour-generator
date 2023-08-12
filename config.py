from classes import Block, JumpType

ParkourVolume = (200, 200, 200)
EnforceParkourVolume = True
FillParkourVolumeWithAirFirst = True  # Only works when EnforceParkourVolume is set to True
MaxParkourLength = 100

CheckPointsEnabled = False
CheckPointsPeriod = 5  # After 5 normal jumptypes follows one checkpoint

UseAllBlocks = True  # Set to False for the below settings to take effect. Set to True to use all JumpTypes for generation.
AllowedStructureTypes = ["SingleBlock"]
Difficulty = 0.3  # Choose parkour difficulty in range [0.0, 1.0]. 0.0 - very easy, 1.0 - very hard
Flow = 0.8        # Choose how fast/flowing/fluent the parkour is to traverse in range [0.0, 1.0]. 0.0 - slow/ahlting, 1.0 - fast/fluent

ParkourType = "StraightSlopes"  # UpwardSpiral, StraightAscending, Straight, StraightSlopes, Random
StraightSlopesSize = 5  # Values: 1 - 10, Changes how frequently the parkour direction changes: 1 - very often, 10 - rarely
SpiralRotation = "counterclockwise"  # clockwise, counterclockwise
SpiralType = "Even"  # Random, Even
SpiralTurnRate = 5  # After how many jumps the Spiral will change direction. Only works with SpiralType = "Even"
SpiralTurnProbability = 5  # Values: 1 - high prob, 10 - low prob. Probability for changing direction for SpiralType = "Random"

BlockType = "minecraft:bedrock"

StartPosition = (0, 0, 0)
StartForwardDirection = "Xpos"

StartBlock = JumpType(name="Parkour Start Structure", structure_type="Start", 
                      rel_start_block=Block(BlockType, (0, 0, 0)), 
                      rel_finish_block=Block(BlockType, (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (-1, 0, 1)), Block(BlockType, (-1, 0, -1)), 
                              Block(BlockType, (-1, 0, 0))],
                      difficulty=0.0, 
                      flow=1.0)
FinishBlock = JumpType(name="Parkour Finish Structure", structure_type="Finish", 
                      rel_start_block=Block(BlockType, (0, 0, 0)), 
                      rel_finish_block=Block(BlockType, (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (-1, 0, 1)), Block(BlockType, (-1, 0, -1)), 
                              Block(BlockType, (-1, 0, 0))],
                      difficulty=0.0, 
                      flow=1.0)
FinishBlock = JumpType(name="Parkour Checkpoint Structure", structure_type="Checkpoint", 
                      rel_start_block=Block(BlockType, (2, 0, 0)), 
                      rel_finish_block=Block(BlockType, (2, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, 0)), Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (2, 0, 1)), Block(BlockType, (2, 0, -1)), 
                              ],
                      difficulty=0.0, 
                      flow=1.0)


Stages = 1



PlotFileType = "jpg"  # "jpg" or "png"




# TODO: Check all config values types and ranges
if StraightSlopesSize < 1 or StraightSlopesSize > 10:
            raise Exception("Invalid input for StraightSlopesSize: must be between 1 and 10 (inclusive)")