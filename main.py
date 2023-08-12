import config
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
# TODO: randomise seed
rng = default_rng(283457)

def compute_abs_coordinates_of_start_block(jumptype: JumpType, absolut_pos_of_last_block, forward_direction):

    Y = absolut_pos_of_last_block[1] + jumptype.rel_start_block.rel_position[1]

    if forward_direction == "Xpos":
        X = absolut_pos_of_last_block[0] + jumptype.rel_start_block.rel_position[0]
        Z = absolut_pos_of_last_block[2] + jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Xneg":
        X = absolut_pos_of_last_block[0] - jumptype.rel_start_block.rel_position[0]
        Z = absolut_pos_of_last_block[2] - jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Zpos":
        X = absolut_pos_of_last_block[0] + jumptype.rel_start_block.rel_position[2]
        Z = absolut_pos_of_last_block[2] + jumptype.rel_start_block.rel_position[0]
    elif forward_direction == "Zneg":
        X = absolut_pos_of_last_block[0] - jumptype.rel_start_block.rel_position[2]
        Z = absolut_pos_of_last_block[2] - jumptype.rel_start_block.rel_position[0]
    
    return (X, Y, Z)


def shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):

     # First zone, one y-level below
        if old_Y == new_Y - 1 and (old_X <= new_X + 2 and old_X >= new_X - 2) and (old_Z <= new_Z + 2 and old_Z >= new_Z - 2):
            return True
        
        # Same height
        if old_Y == new_Y and (old_X <= new_X + 4 and old_X >= new_X - 4) and (old_Z <= new_Z + 4 and old_Z >= new_Z - 4):
            return True

        # One y-level up
        if old_Y == new_Y + 1 and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
            return True

        # Rest of the volume above the block in a 16x10x16 volume
        if (old_Y <= new_Y + 12 and old_Y >= new_Y + 2) and (old_X <= new_X + 8 and old_X >= new_X - 8) and (old_Z <= new_Z + 8 and old_Z >= new_Z - 8):
            return True

def shortcut_possible(new_block: Block, earlier_structure: JumpType):

    new_block_abs = new_block.abs_position

    new_X = new_block_abs[0]
    new_Y = new_block_abs[1]
    new_Z = new_block_abs[2]

    # Check for the rel start block
    old_X = earlier_structure.rel_start_block.abs_position[0]
    old_Y = earlier_structure.rel_start_block.abs_position[1]
    old_Z = earlier_structure.rel_start_block.abs_position[2]

    if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):
        return True
    
    # Check for the rel finish block
    old_X = earlier_structure.rel_finish_block.abs_position[0]
    old_Y = earlier_structure.rel_finish_block.abs_position[1]
    old_Z = earlier_structure.rel_finish_block.abs_position[2]

    if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):
        return True

    for block in earlier_structure.blocks:

        old_X = block.abs_position[0]
        old_Y = block.abs_position[1]
        old_Z = block.abs_position[2]

        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z):
            return True
    
    return False

# Returns True only if the Block is in the config defined Parkour bounds, else False
def in_bounds(block: Block):
    
    # X coordinate
    if block.abs_position[0] >= config.ParkourVolume[0][0] and block.abs_position[0] <= config.ParkourVolume[0][1]:
        # Y coordinate
        if block.abs_position[1] >= config.ParkourVolume[1][0] and block.abs_position[1] <= config.ParkourVolume[1][1]:
            # Z coordinate
            if block.abs_position[2] >= config.ParkourVolume[2][0] and block.abs_position[2] <= config.ParkourVolume[2][1]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def can_be_placed(jumptype: JumpType, current_block_position: tuple, current_forward_direction: str):

    abs_position = compute_abs_coordinates_of_start_block(jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # Check if new Structure is in bounds of the config.ParkourVolume

    if config.EnforceParkourVolume:

        if not in_bounds(jumptype.rel_start_block):
            return False
        if not in_bounds(jumptype.rel_finish_block):
            return False
        for block in jumptype.blocks:

            if not in_bounds(block):
                return False


    # For start and finish blocks
    for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:

            if shortcut_possible(jumptype.rel_start_block, earlier_jump):
                
                return False
            if shortcut_possible(jumptype.rel_finish_block, earlier_jump):
                
                return False
    
    # For rest of the structure
    for block in jumptype.blocks:
        for earlier_jump in list_of_placed_jumps[:len(list_of_placed_jumps)-1]:

            if shortcut_possible(block, earlier_jump):
                
                return False

        
    return True


# Place Start Structure of the Parkour
current_block_position = config.StartPosition
current_forward_direction = config.StartForwardDirection
startblock_instance = deepcopy(StartBlock)
startblock_instance.set_absolut_coordinates(current_block_position, current_forward_direction)
# print(startblock_instance)
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

                        list_of_jumptypes_filtered.append(jumptype)


print(f"Number of filtered jumptypes: {len(list_of_jumptypes_filtered)}")

SlopesDirection = 0
SpiralTurnCounter = 0
try_again_counter = 0
# Search for candidates
for iteration in range(config.MaxParkourLength):

    print(f"Iteration: {iteration+1}/{config.MaxParkourLength}")

    for jumptype in list_of_jumptypes_filtered:

        jumptype_instance = deepcopy(jumptype)

        if can_be_placed(jumptype_instance, current_block_position, current_forward_direction):

            list_of_candidates.append(jumptype_instance)
    

    # No placable JumpTypes found  TODO: define behaviour for different ParkourTypes
    if len(list_of_candidates) == 0:

        if try_again_counter >= 4:
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
    # print(random_index)
    next_jump = list_of_candidates[random_index]

    list_of_placed_jumps.append(next_jump)

    # Set new absolute coordinates for next iteration
    current_block_position = next_jump.rel_finish_block.abs_position


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

    elif config.ParkourType == "Straight" or config.ParkourType == "StraightAscending":

        current_forward_direction = current_forward_direction  # Keep same direction
    
    elif config.ParkourType == "StraightSlopes":

        if config.StraightSlopesSize < 1 or config.StraightSlopesSize > 10:
            raise Exception("Invalid input for StraightSlopesSize: must be between 1 and 10 (inclusive)")
        
        random_bit = rng.integers(low=0, high=config.StraightSlopesSize+1)

        # Only change direction with probability 1/(config.StraightSlopesSize+1)
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

    elif config.ParkourType == "UpwardSpiral":

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


    # Clear list of candidates for next iteration
    list_of_candidates = []

# Place Finish Structure of the Parkour  TODO: Maybe try to place in bounds of Parkour Volume
finishblock_instance = deepcopy(FinishBlock)
finishblock_instance.set_absolut_coordinates(current_block_position, current_forward_direction)
list_of_placed_jumps.append(finishblock_instance)

    
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


    
    



