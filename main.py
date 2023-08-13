import config
import util
from classes import JumpType
from classes import Block
from jumptypes import list_of_jumptypes
from jumptypes import StartBlock
from jumptypes import FinishBlock
from jumptypes import CheckpointBlock
from typing import List
import numpy as np
from numpy.random import default_rng
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import math

list_of_placed_jumps: List[JumpType] = []
list_of_candidates: List[JumpType] = []
list_of_allowed_structure_types = config.AllowedStructureTypes
list_of_directions = ["Xpos", "Zneg", "Xneg", "Zpos"]

# Set seed for the RNG
if config.RandomSeed:

    rng_for_rng = default_rng()
    seed = rng_for_rng.integers(low=0, high=2**63-1)
    print(f"seed: {seed}")
    rng = default_rng(seed)
else:
    print(f"seed: {config.Seed}")
    rng = default_rng(config.Seed)


# Place Start Structure of the Parkour
current_block_position = config.StartPosition
current_forward_direction = config.StartForwardDirection
startblock_instance = deepcopy(StartBlock)
startblock_instance.set_absolut_coordinates(current_block_position, current_forward_direction)
list_of_placed_jumps.append(startblock_instance)





# Pre-filter allowed jumptypes
list_of_jumptypes_filtered = []
if config.UseAllBlocks:
    list_of_jumptypes_filtered = list_of_jumptypes
else:

    for jumptype in list_of_jumptypes:

            if jumptype.structure_type in list_of_allowed_structure_types:
                
                if jumptype.difficulty >= config.Difficulty - 0.2 and jumptype.difficulty <= config.Difficulty + 0.2:

                    if jumptype.flow >= config.Flow - 0.2 and jumptype.flow <= config.Flow + 0.2:

                        if not config.ParkourAscending and util.is_Ascending(jumptype):
                            continue

                        list_of_jumptypes_filtered.append(jumptype)


print(f"Number of filtered jumptypes: {len(list_of_jumptypes_filtered)}")

SlopesDirection = 0
SpiralTurnCounter = 0
CheckPointCounter = 0
try_again_counter = 0

# Search for candidates
print("[", end="")
for iteration in range(config.MaxParkourLength - 2):

    if iteration > config.MaxParkourLength - 2 - CheckPointCounter:
        break

    if iteration % config.MaxParkourLength//10 == 0:
        print("=", end="")
    
    # print(f"Iteration: {iteration+1}/{config.MaxParkourLength}")

    if config.CheckPointsEnabled and iteration % config.CheckPointsPeriod == 0 and iteration != 0:

        next_jump = deepcopy(CheckpointBlock)
        abs_position = util.compute_abs_coordinates_of_start_block(next_jump, current_block_position, current_forward_direction)
        next_jump.set_absolut_coordinates(abs_position, current_forward_direction)

        list_of_placed_jumps.append(next_jump)

        CheckPointCounter += 1

        # Set new absolute coordinates for next iteration
        current_block_position = next_jump.rel_finish_block.abs_position

        continue

    # Search for candidates to be placed
    for jumptype in list_of_jumptypes_filtered:

        jumptype_instance = deepcopy(jumptype)

        if util.can_be_placed(jumptype_instance, current_block_position, current_forward_direction, list_of_placed_jumps):

            list_of_candidates.append(jumptype_instance)
    

    # No placable JumpTypes found  TODO: define behaviour for different ParkourTypes
    if len(list_of_candidates) == 0:

        if try_again_counter >= 10:
            break
        else:
            try_again_counter += 1

            old_direction_index = list_of_directions.index(current_forward_direction)
            new_direction_index = (old_direction_index + 1) % 4
            current_forward_direction = list_of_directions[new_direction_index]
            continue
    else:
        try_again_counter = 0
        
    
    # Choose randomly from list of candidates
    random_index = rng.integers(low=0, high=len(list_of_candidates))
    next_jump = list_of_candidates[random_index]
    list_of_placed_jumps.append(next_jump)

    # Set new absolute coordinates for next iteration
    current_block_position = next_jump.rel_finish_block.abs_position

    # Clear list of candidates for next iteration
    list_of_candidates = []




    ################################################################
    # Direction changes according to the ParkourType set in config #
    ################################################################

    if config.ParkourType == "Random":
        # Choose possible other directions at random
        random_bit = rng.integers(low=0, high=2)
        old_direction_index = list_of_directions.index(current_forward_direction)

        if random_bit == 0:
            if old_direction_index == 0:
                new_direction_index = 3
            else:
                new_direction_index = old_direction_index - 1
        else:
            new_direction_index = (old_direction_index + 1) % 4

        current_forward_direction = list_of_directions[new_direction_index]

    elif config.ParkourType == "Straight":

        current_forward_direction = current_forward_direction  # Keep same direction
    
    elif config.ParkourType == "StraightCurves":

        if config.StraightCurvesSize < 1 or config.StraightCurvesSize > 10:
            raise Exception("Invalid input for StraightCurvesSize: must be between 1 and 10 (inclusive)")
        
        random_bit = rng.integers(low=0, high=config.StraightCurvesSize+1)

        # Only change direction with probability 1/(config.StraightCurvesSize+1)
        if random_bit == 1:

            old_direction_index = list_of_directions.index(current_forward_direction)
            
            if SlopesDirection == -1:
                SlopesDirection = 0
                new_direction_index = (old_direction_index + 1) % 4
            elif SlopesDirection == 0:
                random_bit = rng.integers(low=0, high=2)
                if random_bit == 0:
                    SlopesDirection = -1
                    new_direction_index = (old_direction_index - 1)
                else: 
                    SlopesDirection = 1
                    new_direction_index = (old_direction_index + 1) % 4
            elif SlopesDirection == 1:
                SlopesDirection = 0
                new_direction_index = (old_direction_index - 1)
            
            if new_direction_index < 0:
                new_direction_index = 3
        
            current_forward_direction = list_of_directions[new_direction_index]
        else:
            current_forward_direction = current_forward_direction

    elif config.ParkourType == "Spiral":

        if config.SpiralType == "Even":

            if config.EnforceParkourVolume:

                random_bit = rng.integers(low=0, high=2)   # TODO: adjust probability to have a spiral tight to bounds
            else:

                if SpiralTurnCounter >= config.SpiralTurnRate:
                    random_bit = 1
                    SpiralTurnCounter = 0
                else:
                    random_bit = 0
                    SpiralTurnCounter += 1
        else:
            h_bound = config.SpiralTurnProbability+1
            random_bit = rng.integers(low=0, high=h_bound)

        if random_bit == 1:

            old_direction_index = list_of_directions.index(current_forward_direction)

            if config.SpiralRotation == "clockwise":

                new_direction_index = (old_direction_index + 1) % 4
            else:
                new_direction_index = old_direction_index - 1

            if new_direction_index < 0:
                    new_direction_index = 3
            
            current_forward_direction = list_of_directions[new_direction_index]
        else:
            current_forward_direction = current_forward_direction


    

# Place Finish Structure of the Parkour  TODO: Maybe try to place in bounds of Parkour Volume
finishblock_instance = deepcopy(FinishBlock)
abs_position = util.compute_abs_coordinates_of_start_block(finishblock_instance, current_block_position, current_forward_direction)
finishblock_instance.set_absolut_coordinates(abs_position, current_forward_direction)
list_of_placed_jumps.append(finishblock_instance)
print(f"] {len(list_of_placed_jumps)}/{config.MaxParkourLength}")





################################################################
# Plotting                                                     #
################################################################

print("Filling 3D array")
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

x_axis = []
y_axis = []
z_axis = []

for index, placed_jump in enumerate(list_of_placed_jumps):

    # if index == 0:
    #     marker_color = "green"
    # elif index == len(list_of_placed_jumps) - 1:
    #     marker_color = "red"
    # else:
    #     marker_color = "black"
    
    # ax.scatter(placed_jump.rel_start_block.abs_position[0], placed_jump.rel_start_block.abs_position[2], placed_jump.rel_start_block.abs_position[1], c=[marker_color], marker="s", s=1)
    # ax.scatter(placed_jump.rel_finish_block.abs_position[0], placed_jump.rel_finish_block.abs_position[2], placed_jump.rel_finish_block.abs_position[1], c=[marker_color], marker="s", s=1)

    x_axis.append(placed_jump.rel_start_block.abs_position[0])
    y_axis.append(placed_jump.rel_start_block.abs_position[2])
    z_axis.append(placed_jump.rel_start_block.abs_position[1])

    x_axis.append(placed_jump.rel_finish_block.abs_position[0])
    y_axis.append(placed_jump.rel_finish_block.abs_position[2])
    z_axis.append(placed_jump.rel_finish_block.abs_position[1])

    

    for block in placed_jump.blocks:

        # ax.scatter(block.abs_position[0], block.abs_position[2], block.abs_position[1], c=[marker_color], marker="s", s=1)

        x_axis.append(block.abs_position[0])
        y_axis.append(block.abs_position[2])
        z_axis.append(block.abs_position[1])



print("Generating plot")

marker_color = "black"
ax.plot(x_axis, y_axis, z_axis, 
            linestyle="-", linewidth=0.5,
            c=marker_color, marker="s", markersize=1)

if config.EnforceParkourVolume:

    min_axis_distance = min(config.ParkourVolume[0][0], config.ParkourVolume[1][0], config.ParkourVolume[2][0])
    max_axis_distance = max(config.ParkourVolume[0][1], config.ParkourVolume[1][1], config.ParkourVolume[2][1])
    stepsize = max((abs(max_axis_distance - min_axis_distance)) // 10, 1)
    
    ax.set_xticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
    ax.set_yticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
    ax.set_zticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
else:

    

    x_list = []
    y_list = []
    z_list = []
    
    for placed_jump in list_of_placed_jumps:

        x_list.append(placed_jump.rel_start_block.abs_position[0])
        y_list.append(placed_jump.rel_start_block.abs_position[2])  # Here the y value (for height) is the minecraft z value
        z_list.append(placed_jump.rel_start_block.abs_position[1])

        x_list.append(placed_jump.rel_finish_block.abs_position[0])
        y_list.append(placed_jump.rel_finish_block.abs_position[2])  # Here the y value (for height) is the minecraft z value
        z_list.append(placed_jump.rel_finish_block.abs_position[1])
        

        for block in placed_jump.blocks:

            x_list.append(block.abs_position[0])
            y_list.append(block.abs_position[2])  # Here the y value (for height) is the minecraft z value
            z_list.append(block.abs_position[1])
    
    x_min = min(x_list)
    x_max = max(x_list)
    y_min = min(y_list)
    y_max = max(y_list)
    z_min = min(z_list)
    z_max = max(z_list)

    max_axis_distance = max(x_max, y_max, z_max)
    min_axis_distance = min(x_min, y_min, z_min)
    
    stepsize = max(abs(max_axis_distance-min_axis_distance)//10, 1)
    ax.set_xticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
    ax.set_yticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
    ax.set_zticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))



if config.PlotFileType == "jpg":

    plt.savefig("parkour_plot.jpg")
else:

    plt.savefig("parkour_plot.png", dpi=300)


    
    



