

ParkourVolume = [(0, 50), (0, 50), (0, 50)]  # Absolute X, Y, Z coordinate ranges in the minecraft world.
EnforceParkourVolume = False
FillParkourVolumeWithAirFirst = True  # Only works when EnforceParkourVolume is set to True
MaxParkourLength = 50

CheckPointsEnabled = False
CheckPointsPeriod = 5  # After 5 normal jumptypes follows one checkpoint

UseAllBlocks = True  # Set to False for the below settings to take effect. Set to True to use all JumpTypes for generation.
AllowedStructureTypes = ["SingleBlock"]
Difficulty = 0.3  # Choose parkour difficulty in range [0.0, 1.0]. 0.0 - very easy, 1.0 - very hard
Flow = 0.8        # Choose how fast/flowing/fluent the parkour is to traverse in range [0.0, 1.0]. 0.0 - slow/ahlting, 1.0 - fast/fluent


ParkourType = "Random"  # Spiral, Straight, StraightSlopes, Random  TODO: implement all types
ParkourAscending = True         # Set to True if the parkour should have an upwards elevation change. Set to False for the parkour to stay on the same height/y-level.

StraightSlopesSize = 1  # Values: 1 - 10, Changes how frequently the parkour direction changes: 1 - very often, 10 - rarely

SpiralRotation = "counterclockwise"  # clockwise, counterclockwise
SpiralType = "Even"  # Random, Even
SpiralTurnRate = 5  # After how many jumps the Spiral will change direction. Only works with SpiralType = "Even"
SpiralTurnProbability = 10  # Values: 1 - high prob, 10 - low prob. Probability for changing direction for SpiralType = "Random"


BlockType = "minecraft:bedrock"

StartPosition = (0, 0, 0)  # Absolute X, Y, Z coordinates in the minecraft world. Must be within the ParkourVolume defined above if EnforceParkourVolume is set to True.
StartForwardDirection = "Xpos"


Stages = 1



PlotFileType = "png"  # "jpg" or "png"




# TODO: Check all config values types and ranges
if StraightSlopesSize < 1 or StraightSlopesSize > 10:
            raise Exception("Invalid input for StraightSlopesSize: must be between 1 and 10 (inclusive)")