# type: ignore
import config
import util
from classes import JumpType
import generator
import time
from numpy.random import default_rng
import tkinter as tk
import tkinter.ttk as ttk


def generate_parkour(config: dict[str, any], gui_enabled: bool, gui_loading_bar: ttk.Progressbar, gui_window: tk.Tk):

    list_of_placed_jumps: list[JumpType] = []

    # Set seed for the RNG
    if config["randomSeed"]:
        rng_for_rng = default_rng()
        seed = rng_for_rng.integers(low=0, high=2**63-1)
        print(f"seed: {seed}")
        rng = default_rng(seed)
    else:
        seed = int(config["seed"])
        print(f"seed: {seed}")
        rng = default_rng(seed)

    # Generate Parkour
    start_time_generation = time.time()
    generator.generate_parkour(list_of_placed_jumps, 
                               rng, 
                               list_of_allowed_structure_types=config["allowedStructureTypes"],
                               parkour_start_position=config["startPosition"],
                               parkour_start_forward_direction=config["startForwardDirection"],
                               parkour_type=config["parkourType"],
                               spiral_rotation=config["spiralRotation"],
                               max_parkour_length=config["maxParkourLength"],
                               checkpoints_enabled=config["checkpointsEnabled"],
                               checkpoints_period=config["checkpointsPeriod"],
                               use_all_blocks=config["useAllBlocks"],
                               difficulty=config["difficulty"],
                               flow=config["flow"],
                               ascending=config["parkourAscending"],
                               straight_curves_size=config["straightCurvesSize"],
                               spiral_type=config["spiralType"],
                               spiral_turn_rate=config["spiralTurnRate"],
                               spiral_turn_prob=config["spiralTurnProbability"],
                               enforce_volume=config["enforceParkourVolume"],
                               parkour_volume=config["parkourVolume"],
                               gui_enabled=gui_enabled,
                               gui_loading_bar=gui_loading_bar,
                               gui_window=gui_window)
    end_time_generation = time.time()

    print(f"Time taken: {
          round(end_time_generation-start_time_generation, 3)} s")

    # Write datapack files
    if config["writeDatapackFiles"]:
        util.write_function_files(list_of_placed_jumps, 
                                  parkour_volume=config["parkourVolume"], 
                                  enforce_parkour_volume=config["enforceParkourVolume"], 
                                  fill_volume_with_air=config["fillParkourVolumeWithAir"])

    # Plot parkour to a file
    util.plot_parkour(list_of_placed_jumps, 
                      parkour_volume=config["parkourVolume"], 
                      enforce_parkour_volume=config["enforceParkourVolume"], 
                      plot_command_blocks=config["plotCommandBlocks"],
                      plot_color_scheme=config["plotColorScheme"],
                      plot_file_type=config["plotFileType"])

