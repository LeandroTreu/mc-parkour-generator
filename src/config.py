# type: ignore
from pathlib import Path
import json
from tkinter import messagebox

# Constants
MC_WORLD_MAX_X = 29999984
MC_WORLD_MIN_X = -29999984
MC_WORLD_MAX_Z = MC_WORLD_MAX_X
MC_WORLD_MIN_Z = MC_WORLD_MIN_X
MC_WORLD_MAX_Y = 320  # TODO: Minecraft versions differences
MC_WORLD_MIN_Y = -64
MC_MAX_COMMANDCHAIN_LENGTH = 65536
MC_MAX_FILL_VOLUME = 32768
MC_MAX_FILL_VOLUME_CUBE_WIDTH = 32
MAX_PARKOUR_LENGTH = 10000
MAX_VOLUME = 10000 * MC_MAX_FILL_VOLUME

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
        with open(settings_file, "r", encoding="utf-8") as file:
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
        with open(settings_file, "w", encoding="utf-8") as file:
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
        
        x_len = x_max - x_min
        y_len = y_max - y_min
        z_len = z_max - z_min
        if x_len * y_len * z_len > MAX_VOLUME:
            error_string += f"parkourVolume: maximum volume size is {MAX_VOLUME}\n"
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