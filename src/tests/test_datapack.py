import unittest
import config
from classes import JumpType
import generator
import datapack
from pathlib import Path

class TestDatapack(unittest.TestCase):

    def test_datapack(self):
        
        settings = config.import_config(Path("test_datapack_settings.json"), gui_enabled=False)
        error_str = config.check_config(settings)
        if error_str != "":
            raise Exception(error_str)

        list_of_placed_jumps: list[JumpType] = []

        # Generate Parkour
        seed, nr_jumptypes_filtered, nr_total_jumptypes, list_of_placed_jumps = generator.generate_parkour(list_of_placed_jumps=list_of_placed_jumps, 
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
                                pace=settings["pace"],
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

        # Write datapack files
        if settings["writeDatapackFiles"]:
            datapack.write_function_files(list_of_placed_jumps, 
                                    parkour_volume=settings["parkourVolume"], 
                                    enforce_parkour_volume=settings["enforceParkourVolume"], 
                                    fill_volume_with_air=settings["fillParkourVolumeWithAir"],
                                    gui_enabled=False,
                                    minecraft_version=settings["mcVersion"],
                                    settings_config=settings)


if __name__ == "__main__":
    unittest.main()