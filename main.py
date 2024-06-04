import config
import util
from classes import JumpType
import generator
import time
from numpy.random import default_rng

if __name__ == "__main__":

    list_of_placed_jumps: list[JumpType] = []

    # Set seed for the RNG
    if config.RandomSeed:
        rng_for_rng = default_rng()
        seed = rng_for_rng.integers(low=0, high=2**63-1)
        print(f"seed: {seed}")
        rng = default_rng(seed)
    else:
        print(f"seed: {config.Seed}")
        rng = default_rng(config.Seed)

    # Generate Parkour
    start_time_generation = time.time()
    generator.generate_parkour(list_of_placed_jumps, 
                               rng, 
                               list_of_allowed_structure_types=config.AllowedStructureTypes,
                               parkour_start_position=config.StartPosition,
                               parkour_start_forward_direction=config.StartForwardDirection,
                               parkour_type=config.ParkourType,
                               spiral_rotation=config.SpiralRotation,
                               max_parkour_length=config.MaxParkourLength,
                               checkpoints_enabled=config.CheckPointsEnabled,
                               checkpoints_period=config.CheckPointsPeriod,
                               use_all_blocks=config.UseAllBlocks,
                               difficulty=config.Difficulty,
                               flow=config.Flow,
                               ascending=config.ParkourAscending,
                               straight_curves_size=config.StraightCurvesSize,
                               spiral_type=config.SpiralType,
                               spiral_turn_rate=config.SpiralTurnRate,
                               spiral_turn_prob=config.SpiralTurnProbability,
                               enforce_volume=config.EnforceParkourVolume)
    end_time_generation = time.time()

    print(f"Time taken: {
          round(end_time_generation-start_time_generation, 3)} s")

    # Write datapack files
    if config.FileWrite:
        util.write_function_files(list_of_placed_jumps)

    # Plot parkour to a file
    util.plot_parkour(list_of_placed_jumps)

    print("Done.")
