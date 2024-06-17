# type: ignore
import config
from classes import JumpType
import generator
import time
import gui
import plotting
import datapack

if __name__ == "__main__":

    use_gui = True

    if use_gui:
        gui = gui.Gui()
        gui.run()
    else:
        settings = config.import_config(gui_enabled=False)
        error_str = config.check_config(settings)
        if error_str != "":
            raise Exception(error_str)

        list_of_placed_jumps: list[JumpType] = []

        # Generate Parkour
        start_time_generation = time.time()
        seed = generator.generate_parkour(list_of_placed_jumps=list_of_placed_jumps, 
                                random_seed=settings["randomSeed"], 
                                seed=settings["seed"], 
                                list_of_allowed_structure_types=settings["allowedStructureTypes"],
                                parkour_start_position=settings["startPosition"],
                                parkour_start_forward_direction=settings["startForwardDirection"],
                                parkour_type=settings["parkourType"],
                                spiral_rotation=settings["spiralRotation"],
                                max_parkour_length=settings["maxParkourLength"],
                                checkpoints_enabled=settings["checkpointsEnabled"],
                                checkpoints_period=settings["checkpointsPeriod"],
                                use_all_blocks=settings["useAllBlocks"],
                                difficulty=settings["difficulty"],
                                flow=settings["flow"],
                                ascending=settings["parkourAscending"],
                                curves_size=settings["curvesSize"],
                                spiral_type=settings["spiralType"],
                                spiral_turn_rate=settings["spiralTurnRate"],
                                spiral_turn_prob=settings["spiralTurnProbability"],
                                enforce_volume=settings["enforceParkourVolume"],
                                parkour_volume=settings["parkourVolume"],
                                gui_enabled=False,
                                gui_loading_bar=None,
                                gui_window=None,
                                block_type=settings["blockType"])
        end_time_generation = time.time()
        print(f"seed: {seed}")
        print(f"Generation time: {round(end_time_generation-start_time_generation, 3)} s")

        # Write datapack files
        start_time = time.time()
        if settings["writeDatapackFiles"]:
            datapack.write_function_files(list_of_placed_jumps, 
                                    parkour_volume=settings["parkourVolume"], 
                                    enforce_parkour_volume=settings["enforceParkourVolume"], 
                                    fill_volume_with_air=settings["fillParkourVolumeWithAir"])
        end_time = time.time()
        print(f"Datapack time: {round(end_time-start_time, 3)} s")

        # Plot parkour to a file
        start_time = time.time()
        plotting.plot_parkour(list_of_placed_jumps, 
                        parkour_volume=settings["parkourVolume"], 
                        enforce_parkour_volume=settings["enforceParkourVolume"], 
                        plot_command_blocks=settings["plotCommandBlocks"],
                        plot_color_scheme=settings["plotColorScheme"],
                        plot_file_type=settings["plotFileType"])
        end_time = time.time()
        print(f"Plot time: {round(end_time-start_time, 3)} s")