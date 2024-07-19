"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
import mpg.config
import mpg.generator
import time
import mpg.gui
import mpg.plotting
import mpg.datapack
from pathlib import Path

if __name__ == "__main__":

    # TODO: Better CLI support
    use_gui = True

    if use_gui:
        print(f"Minecraft Parkour Generator (MPG) - Version {mpg.config.MPG_VERSION}\n")

        try:
            gui = mpg.gui.Gui()
            gui.run()
        except Exception as err:
            print(f"Error: {err}")

        key_press = input("\nYou can close this window now.")
    else:
        settings = mpg.config.import_config(Path("settings.json"), gui_enabled=False)
        error_str = mpg.config.check_config(settings)
        if error_str != "":
            raise Exception(error_str)

        # Generate Parkour
        start_time_generation = time.time()
        seed, nr_jumptypes_filtered, nr_total_jumptypes, list_of_placed_jumps, list_of_clusters = mpg.generator.generate_parkour(
                                random_seed=settings["randomSeed"], 
                                seed=settings["seed"], 
                                dict_of_allowed_structure_types=settings["allowedStructureTypes"],
                                parkour_start_position=settings["startPosition"],
                                parkour_start_forward_direction=settings["startForwardDirection"],
                                parkour_type=settings["parkourType"],
                                spiral_rotation=settings["spiralRotation"],
                                max_parkour_length=settings["maxParkourLength"],
                                checkpoints_enabled=settings["checkpointsEnabled"],
                                checkpoints_period=settings["checkpointsPeriod"],
                                use_all_blocks=settings["useAllBlocks"],
                                ascending=settings["parkourAscending"],
                                descending=settings["parkourDescending"],
                                curves_size=settings["curvesSize"],
                                spiral_type=settings["spiralType"],
                                spiral_turn_rate=settings["spiralTurnRate"],
                                spiral_turn_prob=settings["spiralTurnProbability"],
                                enforce_volume=settings["enforceParkourVolume"],
                                parkour_volume=settings["parkourVolume"],
                                gui_enabled=False,
                                gui_loading_bar=None,
                                gui_window=None,
                                block_type=settings["blockType"],
                                t_stop_event=None,
                                mc_version=settings["mcVersion"])
        end_time_generation = time.time()
        print(f"seed: {seed}")
        print(f"Generation time: {round(end_time_generation-start_time_generation, 3)} s")

        # Write datapack files
        start_time = time.time()
        if settings["writeDatapackFiles"]:
            mpg.datapack.write_function_files(list_of_placed_jumps, 
                                    parkour_volume=settings["parkourVolume"], 
                                    enforce_parkour_volume=settings["enforceParkourVolume"], 
                                    fill_volume_with_air=settings["fillParkourVolumeWithAir"],
                                    gui_enabled=False,
                                    minecraft_version=settings["mcVersion"],
                                    settings_config=settings,
                                    directory_path=Path.cwd())
        end_time = time.time()
        print(f"Datapack time: {round(end_time-start_time, 3)} s")

        # Plot parkour to a file
        start_time = time.time()
        mpg.plotting.plot_parkour(list_of_placed_jumps, 
                        parkour_volume=settings["parkourVolume"], 
                        enforce_parkour_volume=settings["enforceParkourVolume"], 
                        plot_command_blocks=settings["plotCommandBlocks"],
                        plot_color_scheme=settings["plotColorScheme"],
                        plot_file_type=settings["plotFileType"],
                        checkpoints_enabled=settings["checkpointsEnabled"],
                        list_of_clusters=list_of_clusters,
                        draw_clusters=False)
        end_time = time.time()
        print(f"Plot time: {round(end_time-start_time, 3)} s")