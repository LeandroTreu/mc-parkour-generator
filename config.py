# type: ignore
from pathlib import Path
import json

def import_config() -> dict[str, any]:
    
    # Set default config
    config = {}
    config["parkourVolume"] = [[0, 10], [0, 10], [0, 10]]
    config["enforceParkourVolume"] = False
    config["fillParkourVolumeWithAir"] = True
    config["maxParkourLength"] = 10
    config["startPosition"] = [0, 0, 0]
    config["startForwardDirection"] = "Xpos"
    config["blockType"] = "minecraft:stone"
    config["randomSeed"] = True
    config["seed"] = 0
    config["checkpointsEnabled"] = False
    config["checkpointsPeriod"] = 10
    config["useAllBlocks"] = True
    config["allowedStructureTypes"] = ["SingleBlock", "TwoBlock"]
    config["difficulty"] = 0.3
    config["flow"] = 0.8
    config["parkourType"] = "Straight"
    config["parkourAscending"] = True
    config["straightCurvesSize"] = 10
    config["spiralRotation"] = "counterclockwise"
    config["spiralType"] = "Even"
    config["spiralTurnRate"] = 10
    config["spiralTurnProbability"] = 2
    config["plotFileType"] = "png"
    config["plotColorScheme"] = "winter"
    config["plotCommandBlocks"] = True
    config["writeDatapackFiles"] = True

    # Import config from file
    settings_file = Path("settings.json")
    with open(settings_file, "r") as file:
        file_dict = dict(json.load(file))
    
    for name, value in file_dict.items():
        if name not in config.keys():
            raise Exception(f"\"{name}\" is not a valid setting")
        else:
            config[name] = file_dict[name]
    
    error_str = check_config(config)
    if error_str != "":
        raise Exception(error_str)

    return config

def check_config(config: dict[str, any]) -> str:

    error_string = ""

    if config["straightCurvesSize"] < 1 or config["straightCurvesSize"] > 10:
        error_string += "Invalid input for \"StraightCurvesSize\": must be between 1 and 10 (inclusive)\n"
    
    return error_string




ParkourVolume: list[tuple[int, int]] = [(-350, -210), (36, 100), (-190, -50)]  # Absolute X, Y, Z coordinate ranges in the minecraft world. TODO: add check for minecraft build height
EnforceParkourVolume = False                  # If True then the parkour will generate only inside the above defined Parkour Volume. If False it will generate to arbitrary coordinates, depending on the start block.
FillParkourVolumeWithAirFirst = True         # Only works when EnforceParkourVolume is set to True
MaxParkourLength = 50                       # Maximum length of the parkour including the Start, Checkpoint and Finish structures.
StartPosition = (-340, 67, -188)                    # Absolute X, Y, Z coordinates in the minecraft world. Must be within the ParkourVolume defined above if EnforceParkourVolume is set to True. The startblock structure is 3x3 blocks so set this to (1, 0, 1) for the start to be within the volume.
StartForwardDirection = "Xneg"               # Sets the initial forward direction of the parkour for the first jump. Values: {Xpos, Xneg, Zpos, Zneg}
BlockType = "minecraft:stone"              # Sets the default minecraft block type for all parkour structures, except for special structures like ladders and ice.

RandomSeed = True                            # Set True for a randomised seed. Set False for a set seed, defined below.
Seed = 98360346                              # Sets a seed for the random number generetor throughout the parkour generation. Value range: [0, 2**63-1]

CheckPointsEnabled = True                    # If True then a checkpoint structure will be placed periodically with the defined CheckPointsPeriod below.
CheckPointsPeriod = 10                       # After this many normal jumptypes, one checkpoint is placed. If not possible the checkpoint is placed as soon as possible later in the parkour.

UseAllBlocks = True                                      # Set to False for the below settings to take effect. Set to True to use all JumpTypes for generation.
AllowedStructureTypes = ["SingleBlock", "TwoBlock"]
Difficulty = 0.3                                         # Choose parkour difficulty in range [0.0, 1.0]. 0.0 - very easy, 1.0 - very hard
Flow = 0.8                                               # Choose how fast/flowing/fluent the parkour is to traverse in range [0.0, 1.0]. 0.0 - slow/halting, 1.0 - fast/fluent


ParkourType = "Random"    # Spiral, Straight, StraightCurves, Random
ParkourAscending = True   # Set to True if the parkour should have an upwards elevation change. Set to False for the parkour to stay on the same height/y-level.

StraightCurvesSize = 5    # Values: 1 - 10, Changes how frequently the parkour direction changes: 1 - very often, 10 - rarely

SpiralRotation = "counterclockwise"  # clockwise, counterclockwise
SpiralType = "Even"                  # Random, Even
SpiralTurnRate = 30                  # After how many jumps the Spiral will change direction. Only works with SpiralType = "Even"
SpiralTurnProbability = 2           # Values: 1 - high prob, 10 - low prob. Probability for changing direction for SpiralType = "Random"


PlotFileType = "png"      # "jpg" or "png"
PlotColorMap = "winter"   # viridis, plasma, gray, hot, summer, winter, hsv, copper
PlotCommandBlocks = True

FileWrite = True         # Set to True to write the minecraft datapack files as soon as the parkour is generated (overwrites with the new parkour every time). Set to False to not write the files.


