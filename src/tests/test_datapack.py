import unittest
import mpg.config
from mpg.classes import JumpType
import mpg.generator
import mpg.datapack
from pathlib import Path

class TestDatapack(unittest.TestCase):

    def test_datapack(self):

        directory_path = Path("tests")

        test_dpacks = ["test_dpack_1_21", "test_dpack_1_18", "test_dpack_1_13"]

        for test_dpack in test_dpacks:
            print(f"Testing: {test_dpack}")
            
            settings_file_name = test_dpack + "_settings.json"
            settings = mpg.config.import_config((directory_path / settings_file_name), gui_enabled=False)
            error_str = mpg.config.check_config(settings)
            if error_str != "":
                raise Exception(error_str)

            # Generate Parkour
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

            # Write datapack files
            if settings["writeDatapackFiles"]:
                mpg.datapack.write_function_files(list_of_placed_jumps, 
                                        parkour_volume=settings["parkourVolume"], 
                                        enforce_parkour_volume=settings["enforceParkourVolume"], 
                                        fill_volume_with_air=settings["fillParkourVolumeWithAir"],
                                        gui_enabled=False,
                                        minecraft_version=settings["mcVersion"],
                                        settings_config=settings,
                                        directory_path=directory_path)
            
            # Compare created datapack with expected datapack
            test_dpack_path = directory_path / test_dpack
            generated_dpack_path = directory_path / "parkour_generator_datapack"

            if settings["mcVersion"] == "1.21":
                test_generate_file = test_dpack_path / "data/parkour_generator/function/generate.mcfunction"
                test_remove_file = test_dpack_path/ "data/parkour_generator/function/remove.mcfunction"
                generated_generate_file = generated_dpack_path / "data/parkour_generator/function/generate.mcfunction"
                generated_remove_file = generated_dpack_path / "data/parkour_generator/function/remove.mcfunction"
            else:
                test_generate_file = test_dpack_path / "data/parkour_generator/functions/generate.mcfunction"
                test_remove_file = test_dpack_path / "data/parkour_generator/functions/remove.mcfunction"
                generated_generate_file = generated_dpack_path / "data/parkour_generator/functions/generate.mcfunction"
                generated_remove_file = generated_dpack_path / "data/parkour_generator/functions/remove.mcfunction"

            test_meta_file = test_dpack_path / "pack.mcmeta"
            generated_meta_file = generated_dpack_path / "pack.mcmeta"

            def compare_files(file_A: Path, file_B: Path):

                lines_A = []
                with open(file_A, "r", encoding="utf-8") as file:
                    for line in file:
                        lines_A.append(line)
                lines_B = []
                with open(file_B, "r", encoding="utf-8") as file:
                    for line in file:
                        lines_B.append(line)

                self.assertEqual(len(lines_A), len(lines_B), msg=f"Testcase: {test_dpack}")
                for i in range(len(lines_A)):
                    self.assertEqual(lines_A[i], lines_B[i], msg=f"Testcase: {test_dpack}")
            
            # Compare meta files
            compare_files(test_meta_file, generated_meta_file)

            # Compare generate.mcfunction files
            compare_files(test_generate_file, generated_generate_file)
            
            # Compare remove.mcfunction files
            compare_files(test_remove_file, generated_remove_file)
        


if __name__ == "__main__":
    unittest.main()