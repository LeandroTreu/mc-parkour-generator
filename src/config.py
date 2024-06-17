# type: ignore
from pathlib import Path
import json
from tkinter import messagebox

# Constants
MC_WORLD_MAX_X = 29999984
MC_WORLD_MIN_X = -29999984
MC_WORLD_MAX_Z = MC_WORLD_MAX_X
MC_WORLD_MIN_Z = MC_WORLD_MIN_X
MC_WORLD_MAX_Y = 320
MC_WORLD_MIN_Y = -64
MAX_PARKOUR_LENGTH = 10000

def set_default_config() -> dict[str, any]:

    config = {}
    config["parkourVolume"] = [[0, 100], [100, 300], [0, 100]]
    config["enforceParkourVolume"] = False
    config["fillParkourVolumeWithAir"] = False
    config["maxParkourLength"] = 50
    config["startPosition"] = [0, 150, 0]
    config["startForwardDirection"] = "Xpos"
    config["blockType"] = "minecraft:stone"
    config["randomSeed"] = True
    config["seed"] = 0
    config["checkpointsEnabled"] = True
    config["checkpointsPeriod"] = 10
    config["useAllBlocks"] = True
    config["allowedStructureTypes"] = ["SingleBlock", "TwoBlock"]
    config["difficulty"] = 0.3
    config["flow"] = 0.8
    config["parkourType"] = "Straight"
    config["parkourAscending"] = True
    config["curvesSize"] = 0.5
    config["spiralRotation"] = "counterclockwise"
    config["spiralType"] = "Even"
    config["spiralTurnRate"] = 10
    config["spiralTurnProbability"] = 0.5
    config["plotFileType"] = "jpg"
    config["plotColorScheme"] = "winter"
    config["plotCommandBlocks"] = True
    config["writeDatapackFiles"] = True

    return config

def import_config(gui_enabled: bool) -> dict[str, any]:
    
    config = set_default_config()

    # Import config from file
    settings_file = Path("settings.json")
    try:
        with open(settings_file, "r") as file:
            file_dict = dict(json.load(file))

        for name, value in file_dict.items():
            if name not in config.keys():
                error_str = f"\"{name}\" is not a valid setting"
                if gui_enabled:
                    messagebox.showerror("Error in settings.json", error_str)
                else:
                    raise Exception(error_str)
            else:
                config[name] = file_dict[name]
    except:
        print("settings.json file not found")
    
    return config

def export_config(config: dict[str, any], gui_enabled: bool) -> None:

    settings_file = Path("settings.json")
    try:
        with open(settings_file, "w") as file:
            json.dump(config, file, indent=1)
    except:
        if gui_enabled:
            messagebox.showerror("Error in settings.json", "Error opening settings.json")
        else:
            raise Exception("Error opening settings.json")

def check_config(config: dict[str, any]) -> str:

    error_string = ""

    try:
        x_min = int(config["parkourVolume"][0][0])
        x_max = int(config["parkourVolume"][0][1])
        y_min = int(config["parkourVolume"][1][0])
        y_max = int(config["parkourVolume"][1][1])
        z_min = int(config["parkourVolume"][2][0])
        z_max = int(config["parkourVolume"][2][1])
        if x_min > x_max: 
            error_string += f"parkourVolume: {x_min} > {x_max}\n"
        if y_min > y_max: 
            error_string += f"parkourVolume: {y_min} > {y_max}\n"
        if z_min > z_max: 
            error_string += f"parkourVolume: {z_min} > {z_max}\n"
        for l in config["parkourVolume"]:
            for c in l:
                if c > MC_WORLD_MAX_X or c < MC_WORLD_MIN_X:
                    error_string += f"parkourVolume: coordinate {c} is not within the range [{MC_WORLD_MIN_X}, {MC_WORLD_MAX_X}]\n"
        if y_min < MC_WORLD_MIN_Y or y_max < MC_WORLD_MIN_Y:
            error_string += f"parkourVolume: minimum build height is Y: {MC_WORLD_MIN_Y}\n"
        if y_min > MC_WORLD_MAX_Y or y_max > MC_WORLD_MAX_Y:
            error_string += f"parkourVolume: maximum build height is Y: {MC_WORLD_MAX_Y}\n"
    except:
        error_string += f"parkourVolume: wrong input format. Only integers are allowed.\n"
        return error_string
    
    if type(config["enforceParkourVolume"]) is not bool:
        error_string += "enforceParkourVolume: wrong input format. Only true or false are allowed.\n"
    if type(config["fillParkourVolumeWithAir"]) is not bool:
        error_string += "fillParkourVolumeWithAir: wrong input format. Only true or false are allowed.\n"

    try:
        pl = int(config["maxParkourLength"]) 
        if pl < 0 or pl > MAX_PARKOUR_LENGTH:
            error_string += f"maxParkourLength: parkour length not in allowed range of [0, {MAX_PARKOUR_LENGTH}]\n"
    except:
        error_string += f"maxParkourLength: wrong input format. Only integers are allowed.\n"
        return error_string

    try:
        x = int(config["startPosition"][0]) 
        y = int(config["startPosition"][1]) 
        z = int(config["startPosition"][2]) 
        if x < MC_WORLD_MIN_X or x > MC_WORLD_MAX_X:
            error_string += f"startPosition: X: {x} not in allowed range of [{MC_WORLD_MIN_X}, {MC_WORLD_MAX_X}]\n"
        if z < MC_WORLD_MIN_Z or z > MC_WORLD_MAX_Z:
            error_string += f"startPosition: Z: {z} not in allowed range of [{MC_WORLD_MIN_Z}, {MC_WORLD_MAX_Z}]\n"
        if y < MC_WORLD_MIN_Y or y > MC_WORLD_MAX_Y:
            error_string += f"startPosition: Y: {y} not in allowed range of [{MC_WORLD_MIN_Y}, {MC_WORLD_MAX_Y}]\n"
        if type(config["enforceParkourVolume"]) is bool and config["enforceParkourVolume"] is True:
            if x > config["parkourVolume"][0][1] or x < config["parkourVolume"][0][0]:
                error_string += f"startPosition: X:{x} is not inside the parkour volume\n"
            if y > config["parkourVolume"][1][1] or y < config["parkourVolume"][1][0]:
                error_string += f"startPosition: Y:{y} is not inside the parkour volume\n"
            if z > config["parkourVolume"][2][1] or z < config["parkourVolume"][2][0]:
                error_string += f"startPosition: Z:{z} is not inside the parkour volume\n"
    except:
        error_string += f"startPosition: wrong input format. Only integers are allowed.\n"
        return error_string

    fd = config["startForwardDirection"]
    if fd != "Xpos" and fd != "Xneg" and fd != "Zpos" and fd != "Zneg":
        error_string += "startForwardDirection: wrong input format. Allowed values are: Xpos, Xneg, Zpos, Zneg.\n"

    if type(config["blockType"]) is not str:
        error_string += "blockType: wrong input format. Needs to be a valid minecraft block string, compatible with the /fill command.\n"

    if type(config["randomSeed"]) is not bool:
        error_string += "randomSeed: wrong input format. Only true or false are allowed.\n"

    try:
        seed = int(config["seed"])
        if seed < 0 or seed > (2**64)-1:
            error_string += f"seed: {seed} is not in the allowed range of [0, 2^64-1]\n"
    except:
        error_string += "seed: wrong input format. Only integers are allowed.\n"

    if type(config["checkpointsEnabled"]) is not bool:
        error_string += "checkpointsEnabled: wrong input format. Only true or false are allowed.\n"

    try:
        cpp = int(config["checkpointsPeriod"])
        if cpp < 1:
            error_string += "checkpointsPeriod: needs to be > 0\n"
    except:
        error_string += "checkpointsPeriod: wrong input format. Only integers are allowed.\n"

    if type(config["useAllBlocks"]) is not bool:
        error_string += "useAllBlocks: wrong input format. Only true or false are allowed.\n"
    
    try:
        for e in config["allowedStructureTypes"]:
            if e != "SingleBlock" and e != "TwoBlock":
                error_string += "allowedStructureTypes: allowed strings are: SingleBlock, TwoBlock\n"
    except:
        error_string += "allowedStructureTypes: wrong input format. Needs to be a list of strings.\n"

    try:
        d = float(config["difficulty"])
        if d < 0.0 or d > 1.0:
            error_string += f"difficulty: {d} is not in the allowed range of [0.0, 1.0]\n"
    except:
        error_string += "difficulty: wrong input format. Needs to be a floating point number.\n"

    try:
        f = float(config["flow"])
        if f < 0.0 or f > 1.0:
            error_string += f"flow: {f} is not in the allowed range of [0.0, 1.0]\n"
    except:
        error_string += "flow: wrong input format. Needs to be a floating point number.\n"

    t = config["parkourType"]
    if t != "Straight" and t != "Curves" and t != "Spiral" and t != "Random":
        error_string += "parkourType: wrong input format. Allowed values are: Straight, Curves, Spiral, Random.\n"

    if type(config["parkourAscending"]) is not bool:
        error_string += "parkourAscending: wrong input format. Only true or false are allowed.\n"

    try:
        cs = float(config["curvesSize"])
        if cs < 0.1 or cs > 1.0:
            error_string += f"curvesSize: {cs} is not in the allowed range of [0.1, 1.0]\n"
    except:
        error_string += "curvesSize: wrong input format. Needs to be a floating point number.\n"

    r = config["spiralRotation"]
    if r != "counterclockwise" and r != "clockwise":
        error_string += "spiralRotation: wrong input format. Allowed values are: counterclockwise and clockwise.\n"

    r = config["spiralType"]
    if r != "Even" and r != "Random":
        error_string += "spiralType: wrong input format. Allowed values are: Even and Random.\n"

    try:
        tr = int(config["spiralTurnRate"])
        if tr < 1:
            error_string += f"spiralTurnRate: must be > 0\n"
    except:
        error_string += "spiralTurnRate: wrong input format. Needs to be an integer number > 0.\n"

    try:
        tp = float(config["spiralTurnProbability"])
        if tp < 0.0 or tp > 1.0:
            error_string += f"spiralTurnProbability: must be in the allowed range of [0.0, 1.0]\n"
    except:
        error_string += "spiralTurnProbability: wrong input format. Needs to be a floating point number.\n"

    if config["plotFileType"] != "png" and config["plotFileType"] != "jpg":
        error_string += "plotFileType: wrong input format. Allowed values are: png and jpg.\n"

    c = config["plotColorScheme"]
    colorschemes = ["winter", "viridis", "plasma", "gray", "hot", "summer", "hsv", "copper"]
    if c not in colorschemes:
        error_string += f"plotColorScheme: wrong input format. Allowed values are: {colorschemes}.\n"

    if type(config["plotCommandBlocks"]) is not bool:
        error_string += "plotCommandBlocks: wrong input format. Only true or false are allowed.\n"

    if type(config["writeDatapackFiles"]) is not bool:
        error_string += "writeDatapackFiles: wrong input format. Only true or false are allowed.\n"
    

    return error_string




# ParkourVolume: list[tuple[int, int]] = [(-350, -210), (36, 100), (-190, -50)]  # Absolute X, Y, Z coordinate ranges in the minecraft world.
# EnforceParkourVolume = False                  # If True then the parkour will generate only inside the above defined Parkour Volume. If False it will generate to arbitrary coordinates, depending on the start block.
# FillParkourVolumeWithAirFirst = True         # Only works when EnforceParkourVolume is set to True
# MaxParkourLength = 50                       # Maximum length of the parkour including the Start, Checkpoint and Finish structures.
# StartPosition = (-340, 67, -188)                    # Absolute X, Y, Z coordinates in the minecraft world. Must be within the ParkourVolume defined above if EnforceParkourVolume is set to True. The startblock structure is 3x3 blocks so set this to (1, 0, 1) for the start to be within the volume.
# StartForwardDirection = "Xneg"               # Sets the initial forward direction of the parkour for the first jump. Values: {Xpos, Xneg, Zpos, Zneg}
# BlockType = "minecraft:stone"              # Sets the default minecraft block type for all parkour structures, except for special structures like ladders and ice.

# RandomSeed = True                            # Set True for a randomised seed. Set False for a set seed, defined below.
# Seed = 98360346                              # Sets a seed for the random number generetor throughout the parkour generation.

# CheckPointsEnabled = True                    # If True then a checkpoint structure will be placed periodically with the defined CheckPointsPeriod below.
# CheckPointsPeriod = 10                       # After this many normal jumptypes, one checkpoint is placed. If not possible the checkpoint is placed as soon as possible later in the parkour.

# UseAllBlocks = True                                      # Set to False for the below settings to take effect. Set to True to use all JumpTypes for generation.
# AllowedStructureTypes = ["SingleBlock", "TwoBlock"]
# Difficulty = 0.3                                         # Choose parkour difficulty in range [0.0, 1.0]. 0.0 - very easy, 1.0 - very hard
# Flow = 0.8                                               # Choose how fast/flowing/fluent the parkour is to traverse in range [0.0, 1.0]. 0.0 - slow/halting, 1.0 - fast/fluent


# ParkourType = "Random"    # Spiral, Straight, Curves, Random
# ParkourAscending = True   # Set to True if the parkour should have an upwards elevation change. Set to False for the parkour to stay on the same height/y-level.

# curvesSize = 0.5    # Values: [0.1, 1.0], Changes the size of the curves: 0.1 - small, 1.0 - big

# SpiralRotation = "counterclockwise"  # clockwise, counterclockwise
# SpiralType = "Even"                  # Random, Even
# SpiralTurnRate = 30                  # After how many jumps the Spiral will change direction. Only works with SpiralType = "Even"
# SpiralTurnProbability = 0.5          # Probability for changing direction for SpiralType = "Random"


# PlotFileType = "png"      # "jpg" or "png"
# PlotColorMap = "winter"   # viridis, plasma, gray, hot, summer, winter, hsv, copper
# PlotCommandBlocks = True

# FileWrite = True         # Set to True to write the minecraft datapack files as soon as the parkour is generated (overwrites with the new parkour every time). Set to False to not write the files.


