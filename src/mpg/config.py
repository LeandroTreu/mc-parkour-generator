"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
from pathlib import Path
import json
from tkinter import messagebox
from typing import Any

# Constants
MPG_VERSION = "0.2.0"
MC_WORLD_MAX_X = 29999984
MC_WORLD_MIN_X = -29999984
MC_WORLD_MAX_Z = MC_WORLD_MAX_X
MC_WORLD_MIN_Z = MC_WORLD_MIN_X
MC_WORLD_MAX_Y = 319
MC_WORLD_MIN_Y = -64
MC_WORLD_MAX_Y_OLD = 255
MC_WORLD_MIN_Y_OLD = 0
MC_MAX_COMMANDCHAIN_LENGTH = 65536
MC_MAX_FILL_VOLUME = 32768
MC_MAX_FILL_VOLUME_CUBE_WIDTH = 32
MAX_PARKOUR_LENGTH = 10000
MAX_VOLUME = 10000 * MC_MAX_FILL_VOLUME
DIRECTIONS = ["Xpos", "Zneg", "Xneg", "Zpos"]
ALLOWED_STRUCTURE_TYPES_NAMES = ["SingleBlock", "TwoBlock", "FourBlock"]
PARKOUR_TYPE_NAMES = ["Straight", "Curves", "Spiral", "Random"]
PLOT_COLORSCHEMES = ["winter", "viridis", "plasma", "gray", "hot", "summer", "hsv", "copper"]
PLOT_FILE_TYPES = ["jpg", "png"]
MC_VERSIONS = ["1.21", "1.18 - 1.20.6", "1.13 - 1.17.1"]
SPIRAL_TYPES = ["Even", "Random"]
SPIRAL_ROTATIONS = ["counterclockwise", "clockwise"]
DIFFICULTIES = ["easy", "medium", "hard"]
PACE = ["slow", "medium", "fast"]
CLUSTER_SIZE = 8  # TODO: check if same parkour generated with different sizes, dynamic size depending on parkour type

def set_default_config() -> dict[str, Any]:

    config = {}
    config["allowedStructureTypes"] = ALLOWED_STRUCTURE_TYPES_NAMES
    config["blockType"] = "minecraft:quartz_block"
    config["checkpointsEnabled"] = True
    config["checkpointsPeriod"] = 10
    config["curvesSize"] = 0.5
    config["difficulty"] = "medium"
    config["enforceParkourVolume"] = False
    config["fillParkourVolumeWithAir"] = False
    config["maxParkourLength"] = 50
    config["mcVersion"] = "1.21"
    config["pace"] = "medium"
    config["parkourAscending"] = True
    config["parkourDescending"] = False
    config["parkourType"] = "Spiral"
    config["parkourVolume"] = [[0, 100], [100, 255], [0, 100]]
    config["plotColorScheme"] = "winter"
    config["plotCommandBlocks"] = True
    config["plotFileType"] = "jpg"
    config["randomSeed"] = True
    config["seed"] = 0
    config["spiralRotation"] = "counterclockwise"
    config["spiralTurnProbability"] = 0.2
    config["spiralTurnRate"] = 10
    config["spiralType"] = "Even"
    config["startForwardDirection"] = "Xpos"
    config["startPosition"] = [0, 150, 0]
    config["useAllBlocks"] = False
    config["writeDatapackFiles"] = True

    return config

def import_config(settings_file_path: Path, gui_enabled: bool) -> dict[str, Any]:
    
    config = set_default_config()

    # Import config from file
    try:
        with open(settings_file_path, "r", encoding="utf-8") as file:
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
        if not gui_enabled:
            print("settings.json file not found")
    
    return config

def export_config(settings_file_path: Path, config: dict[str, Any], gui_enabled: bool) -> None:

    try:
        with open(settings_file_path, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=1)
    except:
        if gui_enabled:
            messagebox.showerror("Error in settings.json", "Error opening settings.json")
        else:
            raise Exception("Error opening settings.json")

# Checks all config variables for type and range
# For parkourVolume it silently switches the coordinates such that e.g. x_min < x_max
def check_config(config: dict[str, Any]) -> str:

    error_string = ""

    mc_version = config["mcVersion"]
    if mc_version not in MC_VERSIONS:
        error_string += f"mcVersion: wrong input format. Allowed values are: {MC_VERSIONS}\n"
        return error_string

    try:
        x_min = int(config["parkourVolume"][0][0])
        x_max = int(config["parkourVolume"][0][1])
        y_min = int(config["parkourVolume"][1][0])
        y_max = int(config["parkourVolume"][1][1])
        z_min = int(config["parkourVolume"][2][0])
        z_max = int(config["parkourVolume"][2][1])
        if x_min > x_max:
            temp = x_min
            x_min = x_max
            x_max = temp
            config["parkourVolume"][0][0] = x_min
            config["parkourVolume"][0][1] = x_max
        if y_min > y_max: 
            temp = y_min
            y_min = y_max
            y_max = temp
            config["parkourVolume"][1][0] = y_min
            config["parkourVolume"][1][1] = y_max
        if z_min > z_max: 
            temp = z_min
            z_min = z_max
            z_max = temp
            config["parkourVolume"][2][0] = z_min
            config["parkourVolume"][2][1] = z_max
        for l in config["parkourVolume"]:
            for c in l:
                if c > MC_WORLD_MAX_X or c < MC_WORLD_MIN_X:
                    error_string += f"parkourVolume: coordinate {c} is not within the range [{MC_WORLD_MIN_X}, {MC_WORLD_MAX_X}]\n"
        mc_version = config["mcVersion"]
        if mc_version == "1.13 - 1.17.1" and (y_min < MC_WORLD_MIN_Y_OLD or y_max < MC_WORLD_MIN_Y_OLD):
            error_string += f"parkourVolume: minimum build height is Y: {MC_WORLD_MIN_Y_OLD}\n"
        if mc_version != "1.13 - 1.17.1" and (y_min < MC_WORLD_MIN_Y or y_max < MC_WORLD_MIN_Y):
            error_string += f"parkourVolume: minimum build height is Y: {MC_WORLD_MIN_Y}\n"

        if mc_version == "1.13 - 1.17.1" and (y_min > MC_WORLD_MAX_Y_OLD or y_max > MC_WORLD_MAX_Y_OLD):
            error_string += f"parkourVolume: maximum build height is Y: {MC_WORLD_MAX_Y_OLD}\n"
        if mc_version != "1.13 - 1.17.1" and (y_min > MC_WORLD_MAX_Y or y_max > MC_WORLD_MAX_Y):
            error_string += f"parkourVolume: maximum build height is Y: {MC_WORLD_MAX_Y}\n"
        
        x_len = abs(x_max - x_min)
        y_len = abs(y_max - y_min)
        z_len = abs(z_max - z_min)
        if x_len * y_len * z_len > MAX_VOLUME:
            error_string += f"parkourVolume: maximum volume size is {MAX_VOLUME}\n"
    except:
        error_string += f"parkourVolume: wrong input format. Only integers are allowed.\n"
        return error_string
    
    if type(config["enforceParkourVolume"]) is not bool:
        error_string += "enforceParkourVolume: wrong input format. Only true or false are allowed.\n"
        return error_string
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
        
        mc_version = config["mcVersion"]
        if mc_version == "1.13 - 1.17.1" and (y < MC_WORLD_MIN_Y_OLD or y > MC_WORLD_MAX_Y_OLD):
            error_string += f"startPosition: Y: {y} not in allowed range of [{MC_WORLD_MIN_Y_OLD}, {MC_WORLD_MAX_Y_OLD}]\n"
        if mc_version != "1.13 - 1.17.1" and (y < MC_WORLD_MIN_Y or y > MC_WORLD_MAX_Y):
            error_string += f"startPosition: Y: {y} not in allowed range of [{MC_WORLD_MIN_Y}, {MC_WORLD_MAX_Y}]\n"
        if config["enforceParkourVolume"] is True:
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
    if fd not in DIRECTIONS:
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
            if e not in ALLOWED_STRUCTURE_TYPES_NAMES:
                error_string += f"allowedStructureTypes: {e} is not a valid structure type. Allowed strings are: {ALLOWED_STRUCTURE_TYPES_NAMES}\n"
    except:
        error_string += "allowedStructureTypes: wrong input format. Needs to be a list of strings.\n"

    if config["difficulty"] not in DIFFICULTIES:
        error_string += f"difficulty: wrong input format. Allowed strings are: {DIFFICULTIES}\n"
    if config["pace"] not in PACE:
        error_string += f"pace: wrong input format. Allowed strings are: {PACE}\n"

    t = config["parkourType"]
    if t not in PARKOUR_TYPE_NAMES:
        error_string += f"parkourType: {t} is not a valid parkour type. Allowed strings are: {PARKOUR_TYPE_NAMES}\n"

    if type(config["parkourAscending"]) is not bool:
        error_string += "parkourAscending: wrong input format. Only true or false are allowed.\n"
    if type(config["parkourDescending"]) is not bool:
        error_string += "parkourDescending: wrong input format. Only true or false are allowed.\n"

    try:
        cs = float(config["curvesSize"])
        if cs < 0.1 or cs > 1.0:
            error_string += f"curvesSize: {cs} is not in the allowed range of [0.1, 1.0]\n"
    except:
        error_string += "curvesSize: wrong input format. Needs to be a floating point number.\n"

    r = config["spiralRotation"]
    if r not in SPIRAL_ROTATIONS:
        error_string += f"spiralRotation: wrong input format. Allowed values are: {SPIRAL_ROTATIONS}.\n"

    r = config["spiralType"]
    if r not in SPIRAL_TYPES:
        error_string += f"spiralType: wrong input format. Allowed values are: {SPIRAL_TYPES}.\n"

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

    if config["plotFileType"] not in PLOT_FILE_TYPES:
        error_string += f"plotFileType: wrong input format. Allowed values are: {PLOT_FILE_TYPES}.\n"

    c = config["plotColorScheme"]
    if c not in PLOT_COLORSCHEMES:
        error_string += f"plotColorScheme: {c} is not a valid colorscheme. Allowed values are: {PLOT_COLORSCHEMES}.\n"

    if type(config["plotCommandBlocks"]) is not bool:
        error_string += "plotCommandBlocks: wrong input format. Only true or false are allowed.\n"

    if type(config["writeDatapackFiles"]) is not bool:
        error_string += "writeDatapackFiles: wrong input format. Only true or false are allowed.\n"
    
    return error_string