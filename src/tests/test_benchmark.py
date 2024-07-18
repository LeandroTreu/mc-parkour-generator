import unittest
import mpg.config
from mpg.classes import JumpType
import mpg.generator
import mpg.datapack
from pathlib import Path
import time

class TestDatapack(unittest.TestCase):

    def test_benchmark(self):

        directory_path = Path("tests")

        test_configs = ["test_benchmark_straight_1000_settings.json"]

        for test_config in test_configs:
            print(f"Running: {test_config}")
            
            settings = mpg.config.import_config((directory_path / test_config), gui_enabled=False)
            error_str = mpg.config.check_config(settings)
            if error_str != "":
                raise Exception(error_str)

            # Generate Parkour
            start_time = time.time()
            seed, nr_jumptypes_filtered, nr_total_jumptypes, list_of_placed_jumps = mpg.generator.generate_parkour(
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
            end_time = time.time()
            print(f"Time taken: {round(end_time-start_time, 3)} s")


if __name__ == "__main__":
    unittest.main()