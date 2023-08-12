import config
from classes import JumpType
from classes import Block
from jumptypes import list_of_jumptypes
from typing import List
import numpy as np
from numpy.random import default_rng
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import math

list_of_placed_jumps: List[JumpType] = []
list_of_candidates: List[JumpType] = []
list_of_allowed_structure_types = ["SingleBlock"]
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

def shortcut_possible(new_block: Block, earlier_structure: JumpType):

    new_block_abs = new_block.abs_position

    for block in earlier_structure.blocks:

        old_X = block.abs_position[0]
        old_Y = block.abs_position[1]
        old_Z = block.abs_position[2]

        new_X = new_block_abs[0]
        new_Y = new_block_abs[1]
        new_Z = new_block_abs[2]

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
    
    return False

def can_be_placed(jumptype: JumpType, current_block_position: tuple, current_forward_direction: str):

    abs_position = compute_abs_coordinates_of_start_block(jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # TODO: Check if new Structure is in bounds of the config.ParkourVolume
    x_upper_bound = config.StartPosition[0]+config.ParkourVolume[0]
    y_upper_bound = config.StartPosition[1]+config.ParkourVolume[1]
    z_upper_bound = config.StartPosition[2]+config.ParkourVolume[2]
    
    if jumptype.rel_start_block.abs_position[0] >= config.StartPosition[0] and jumptype.rel_start_block.abs_position[0] <= x_upper_bound:
        if jumptype.rel_start_block.abs_position[1] >= config.StartPosition[1] and jumptype.rel_start_block.abs_position[1] <= y_upper_bound:
            if jumptype.rel_start_block.abs_position[2] >= config.StartPosition[2] and jumptype.rel_start_block.abs_position[2] <= z_upper_bound:
                pass
            else:
                return False
        else:
            return False
    else:
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
StartBlock = deepcopy(config.StartBlock)
StartBlock.set_absolut_coordinates(current_block_position, current_forward_direction)
list_of_placed_jumps.append(StartBlock)


# Pre-filter allowed jumptypes
list_of_jumptypes_filtered = []
for jumptype in list_of_jumptypes:

        if jumptype.structure_type in list_of_allowed_structure_types:
            
            if jumptype.difficulty >= config.Difficulty - 0.2 and jumptype.difficulty <= config.Difficulty + 0.2:

                if jumptype.flow >= config.Flow - 0.2 and jumptype.flow <= config.Flow + 0.2:

                    list_of_jumptypes_filtered.append(jumptype)

SlopesDirection = 0
SpiralTurnCounter = 0
# Search for candidates
for iteration in range(config.MaxParkourLength):

    for jumptype in list_of_jumptypes_filtered:

        jumptype_instance = deepcopy(jumptype)

        if can_be_placed(jumptype_instance, current_block_position, current_forward_direction):

            list_of_candidates.append(jumptype_instance)
    
    # for j in list_of_candidates:
    #     print(j.name)
    
    # Choose randomly from list of candidates
    random_index = rng.integers(low=0, high=len(list_of_candidates))
    # print(random_index)
    next_jump = list_of_candidates[random_index]

    list_of_placed_jumps.append(next_jump)

    # Set new absolute coordinates for next iteration
    current_block_position = next_jump.rel_finish_block.abs_position

    # TODO: Set new forward direction for next iteration

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

# Place Finish Structure of the Parkour
FinishBlock = deepcopy(config.FinishBlock)
FinishBlock.set_absolut_coordinates(current_block_position, current_forward_direction)
list_of_placed_jumps.append(FinishBlock)

    
print("Filling 3D array")
if config.EnforceParkourVolume:

    array_3d = np.zeros(config.ParkourVolume, dtype=int)
else:

    furthest_block = (0, 0, 0)
    longest_distance = 0
    first_jump = list_of_placed_jumps[0]
    origin = (first_jump.rel_start_block.abs_position)
    # print(origin)
    for placed_jump in list_of_placed_jumps:

        x = placed_jump.rel_start_block.abs_position[0]
        y = placed_jump.rel_start_block.abs_position[1]
        z = placed_jump.rel_start_block.abs_position[2]

        distance = math.sqrt((x-origin[0])**2 + (y-origin[1]**2) + (z-origin[2])**2)

        if distance > longest_distance:
            distance = longest_distance
            furthest_block = (x, y, z)

        x = placed_jump.rel_finish_block.abs_position[0]
        y = placed_jump.rel_finish_block.abs_position[1]
        z = placed_jump.rel_finish_block.abs_position[2]

        distance = math.sqrt((x-origin[0])**2 + (y-origin[1]**2) + (z-origin[2])**2)

        if distance > longest_distance:
            distance = longest_distance
            furthest_block = (x, y, z)
        

        for block in placed_jump.blocks:

            x = block.abs_position[0]
            y = block.abs_position[1]
            z = block.abs_position[2]

            distance = math.sqrt((x-origin[0])**2 + (y-origin[1]**2) + (z-origin[2])**2)

            if distance > longest_distance:
                distance = longest_distance
                furthest_block = (x, y, z)
    
    max_axis_distance = max(furthest_block) + 10
    # print(max_axis_distance)
    array_3d = np.zeros((max_axis_distance, max_axis_distance, max_axis_distance), dtype=int)



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for placed_jump in list_of_placed_jumps:
    print(placed_jump)

    # print(placed_jump.rel_start_block.abs_position)
    # print(placed_jump.rel_finish_block.abs_position)
    
    # array_3d[placed_jump.rel_start_block.abs_position[0]][placed_jump.rel_start_block.abs_position[2]][placed_jump.rel_start_block.abs_position[1]] = 1
    # array_3d[placed_jump.rel_finish_block.abs_position[0]][placed_jump.rel_finish_block.abs_position[2]][placed_jump.rel_finish_block.abs_position[1]] = 1
    
    ax.scatter(placed_jump.rel_start_block.abs_position[0], placed_jump.rel_start_block.abs_position[2], placed_jump.rel_start_block.abs_position[1], c=["black"], marker="s")
    ax.scatter(placed_jump.rel_finish_block.abs_position[0], placed_jump.rel_finish_block.abs_position[2], placed_jump.rel_finish_block.abs_position[1], c=["black"], marker="s")

    for block in placed_jump.blocks:

        # array_3d[block.abs_position[0]][block.abs_position[2]][block.abs_position[1]] = 1

        ax.scatter(block.abs_position[0], block.abs_position[2], block.abs_position[1], c=["black"], marker="s")







print("Generating plot")
ax.set_xticks(np.arange(0, max_axis_distance, max_axis_distance//10))
ax.set_yticks(np.arange(0, max_axis_distance, max_axis_distance//10))
ax.set_zticks(np.arange(0, max_axis_distance, max_axis_distance//10))

if config.PlotFileType == "jpg":

    plt.savefig("parkour_plot.jpg")
else:

    plt.savefig("parkour_plot.png")


    
    



