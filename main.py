import config
import util
from classes import JumpType
from classes import Block
from jumptypes import list_of_jumptypes
from jumptypes import StartBlock
from jumptypes import FinishBlock
from jumptypes import CheckpointBlock
from jumptypes import CommandBlockControl
from jumptypes import DispenserCommandblock
from typing import List
import numpy as np
from numpy.random import default_rng
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import math
import time

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

# Place the control command blocks structure
if config.CheckPointsEnabled:
     
    world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
    abs_position = (world_spawn[0]-10, world_spawn[1], world_spawn[2]-10)  # TODO: Smart positioning of the command blocks


    if config.StartForwardDirection == "Xpos":
        rotation_degree = 180
    else if config.StartForwardDirection == "Xneg":
        rotation_degree = 0
    else if config.StartForwardDirection == "Zpos":
        rotation_degree = 90
    else if config.StartForwardDirection == "Zneg":
        rotation_degree = -90


    command_blocks_instance = deepcopy(CommandBlockControl)
    command_block_1_string = 'minecraft:chain_command_block[facing=west]{Command:"' + f'fill {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} minecraft:redstone_block replace' + '"}'
    command_block_2_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'fill {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} minecraft:air replace' + '"}'
    command_block_3_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'kill @e[type=minecraft:fishing_bobber]' + '"}'
    command_block_4_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'execute at @e[type=minecraft:fishing_bobber] run tp @p {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]} {rotation_degree} 0' + '"}'

    blocks=[Block(command_block_1_string, (1, 0, 0)), 
            Block(command_block_2_string, (2, 0, 0)),
            Block("minecraft:redstone_block", (1, 1, 0)), Block("minecraft:redstone_block", (2, 1, 0)), 
            Block(command_block_3_string, (4, 0, 0)), 
            Block(command_block_4_string, (6, 0, 0)),
            Block("minecraft:redstone_block", (4, 1, 0)), Block("minecraft:redstone_block", (6, 1, 0)),
    ]
    command_blocks_instance.blocks = blocks
    command_blocks_instance.set_absolut_coordinates(abs_position, "Xpos")

    list_of_placed_jumps.append(command_blocks_instance)

    # Place command block that gives the player a checkpoint teleporter
    # TODO: Position according to config.StartForwardDirection
    dispenser_instance = deepcopy(DispenserCommandblock)
    dispenser_instance.set_absolut_coordinates((world_spawn[0], world_spawn[1]+2, world_spawn[2]-2), config.StartForwardDirection)
    list_of_placed_jumps.append(dispenser_instance)




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
tryToPlaceCheckpointHere = config.CheckPointsPeriod

# Search for candidates
start_time_generation = time.time()
print("[", end="")
iteration = 0
while iteration < config.MaxParkourLength - 2:

    if iteration % max(config.MaxParkourLength//10, 1) == 0:
        print("=", end="", flush=True)
    
    # print(f"Iteration: {iteration+1}/{config.MaxParkourLength}")


    if config.CheckPointsEnabled:
        
        if tryToPlaceCheckpointHere == iteration:

            # print(tryToPlaceCheckpointHere)

            checkpoint_instance = deepcopy(CheckpointBlock)

            if util.can_be_placed(checkpoint_instance, current_block_position, current_forward_direction, list_of_placed_jumps):

                # print("placed", tryToPlaceCheckpointHere)

                c_block_abs = command_blocks_instance.rel_start_block.abs_position
                
                for block in checkpoint_instance.blocks:
                    if block.name == "minecraft:light_weighted_pressure_plate"
                        checkpoint_respawn = block.abs_position
                
                if current_forward_direction == "Xpos":
                    rotation_degree = 180
                else if current_forward_direction == "Xneg":
                    rotation_degree = 0
                else if current_forward_direction == "Zpos":
                    rotation_degree = 90
                else if current_forward_direction == "Zneg":
                    rotation_degree = -90
    
                checkpoint_command_string_recursive = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'execute at @e[type=minecraft:fishing_bobber] run tp @p {checkpoint_respawn[0]} {checkpoint_respawn[1]} {checkpoint_respawn[2]} {rotation_degree} 0' + '"}' 
                checkpoint_command_string = 'minecraft:command_block{Command:"' + f'fill {c_block_abs[0]+6} {c_block_abs[1]} {c_block_abs[2]} {c_block_abs[0]+6} {c_block_abs[1]} {c_block_abs[2]} {checkpoint_command_string_recursive} destroy' + '"}' 
                
                for block in checkpoint_instance.blocks:
                    if block.name == "minecraft:command_block":
                        block.name = checkpoint_command_string
                  

                list_of_placed_jumps.append(checkpoint_instance)
                CheckPointCounter += 1

                # Set new absolute coordinates for next iteration
                current_block_position = checkpoint_instance.rel_finish_block.abs_position

                tryToPlaceCheckpointHere = iteration + config.CheckPointsPeriod

                iteration += 1
                continue
            else:
                tryToPlaceCheckpointHere = iteration + 1

    # Search for candidates to be placed
    for jumptype in list_of_jumptypes_filtered:

        jumptype_instance = deepcopy(jumptype)

        if util.can_be_placed(jumptype_instance, current_block_position, current_forward_direction, list_of_placed_jumps):

            list_of_candidates.append(jumptype_instance)
    

    # No placable JumpTypes found
    if len(list_of_candidates) == 0:

        if try_again_counter >= 10:
            break
        else:
            try_again_counter += 1

            old_direction_index = list_of_directions.index(current_forward_direction)

            if config.ParkourType == "Random":

                new_direction_index = (old_direction_index + 1) % 4
            elif config.ParkourType == "Straight":

                new_direction_index = old_direction_index
            elif config.ParkourType == "StraightCurves":

                new_direction_index = (old_direction_index + 1) % 4
            elif config.ParkourType == "Spiral":

                if config.SpiralRotation == "clockwise":

                    new_direction_index = (old_direction_index + 1) % 4
                else:
                    new_direction_index = old_direction_index - 1

                if new_direction_index < 0:
                    new_direction_index = 3
            
            current_forward_direction = list_of_directions[new_direction_index]

            # print("trying again")
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

    iteration += 1


    

# Place Finish Structure of the Parkour  TODO: Maybe try to place in bounds of Parkour Volume
finishblock_instance = deepcopy(FinishBlock)
abs_position = util.compute_abs_coordinates_of_start_block(finishblock_instance, current_block_position, current_forward_direction)
finishblock_instance.set_absolut_coordinates(abs_position, current_forward_direction)
list_of_placed_jumps.append(finishblock_instance)

# Adjust for the control structure and the dispenser
if config.CheckPointsEnabled:
    
    print(f"] {len(list_of_placed_jumps)-2}/{config.MaxParkourLength}")
else:
    
    print(f"] {len(list_of_placed_jumps)}/{config.MaxParkourLength}")


end_time_generation = time.time()
print(f"Time taken: {round(end_time_generation-start_time_generation, 3)} s")


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

    x_axis.append(placed_jump.rel_start_block.abs_position[0])
    y_axis.append(placed_jump.rel_start_block.abs_position[2])
    z_axis.append(placed_jump.rel_start_block.abs_position[1])

    x_axis.append(placed_jump.rel_finish_block.abs_position[0])
    y_axis.append(placed_jump.rel_finish_block.abs_position[2])
    z_axis.append(placed_jump.rel_finish_block.abs_position[1])

    

    for block in placed_jump.blocks:

        x_axis.append(block.abs_position[0])
        y_axis.append(block.abs_position[2])
        z_axis.append(block.abs_position[1])



print("Generating plot")

line_color = "black"
ax.plot(x_axis, y_axis, z_axis, 
            linestyle="-", linewidth=0.5,
            c=line_color, marker="s", markersize=0)

ax.scatter(x_axis, y_axis, z_axis, c=z_axis, cmap=config.PlotColorMap, marker="s", s=2, alpha=1)

if config.EnforceParkourVolume:

    min_axis_distance = min(config.ParkourVolume[0][0], config.ParkourVolume[1][0], config.ParkourVolume[2][0])
    max_axis_distance = max(config.ParkourVolume[0][1], config.ParkourVolume[1][1], config.ParkourVolume[2][1])
    stepsize = max((abs(max_axis_distance - min_axis_distance)) // 10, 1)
    
    ax.set_xticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
    ax.set_yticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
    ax.set_zticks(np.arange(min_axis_distance, max_axis_distance+1, stepsize))
else:

    # TODO: fix axis generation

    x_list = []
    y_list = []
    z_list = []
    
    for placed_jump in list_of_placed_jumps:

        x_list.append(placed_jump.rel_start_block.abs_position[0])
        y_list.append(placed_jump.rel_start_block.abs_position[2])  # Here the y value is the minecraft z value
        z_list.append(placed_jump.rel_start_block.abs_position[1])  # height == minecraft y value

        x_list.append(placed_jump.rel_finish_block.abs_position[0])
        y_list.append(placed_jump.rel_finish_block.abs_position[2])  # Here the y value is the minecraft z value
        z_list.append(placed_jump.rel_finish_block.abs_position[1])  # height == minecraft y value
        

        for block in placed_jump.blocks:

            x_list.append(block.abs_position[0])
            y_list.append(block.abs_position[2])  # Here the y value is the minecraft z value
            z_list.append(block.abs_position[1])  # height == minecraft y value
    
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




################################################################
# Write file                                                   #
################################################################

if config.FileWrite:

    print("Writing files...")

    # TODO: Write config file variables as a text header into the file
    # TODO: Command limit per function file is 65,536: gamerule maxCommandChainLength
    # TODO: Research gamerule commandModificationBlockLimit
    with open("parkour_generator_datapack/data/parkour_generator/functions/generate.mcfunction", "w") as file:

        file.write(f"# Headerline\n")

        file.write(f"gamerule spawnRadius 0\n")

        world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
        file.write(f"setworldspawn {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")
        file.write(f"spawnpoint @a {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")
        file.write(f"tp @a {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")

        file.write(f"gamemode adventure @a\n")
        file.write(f"effect give @a minecraft:saturation 3600 4\n")
        file.write(f"gamerule doImmediateRespawn true\n")
        file.write(f"gamerule fallDamage false\n")
        file.write(f"gamerule keepInventory true\n")


        # Fill parkour volume with air first if set in config
        if config.EnforceParkourVolume and config.FillParkourVolumeWithAirFirst:

            volume = config.ParkourVolume
            file.write(f"fill {volume[0][0]} {volume[1][0]} {volume[2][0]} {volume[0][1]} {volume[1][1]} {volume[2][1]} minecraft:air\n")

        # Place all jump structures
        for placed_jump in list_of_placed_jumps:

            x = placed_jump.rel_start_block.abs_position[0]
            y = placed_jump.rel_start_block.abs_position[1]
            z = placed_jump.rel_start_block.abs_position[2]

            writestr = f"fill {x} {y} {z} {x} {y} {z} {placed_jump.rel_start_block.name}\n"
            file.write(writestr)

            x = placed_jump.rel_finish_block.abs_position[0]
            y = placed_jump.rel_finish_block.abs_position[1]
            z = placed_jump.rel_finish_block.abs_position[2]

            writestr = f"fill {x} {y} {z} {x} {y} {z} {placed_jump.rel_finish_block.name}\n"
            file.write(writestr)

            

            for block in placed_jump.blocks:

                x = block.abs_position[0]
                y = block.abs_position[1]
                z = block.abs_position[2]

                writestr = f"fill {x} {y} {z} {x} {y} {z} {block.name}\n"
                file.write(writestr)


    # TODO: Text header for explanation
    with open("parkour_generator_datapack/data/parkour_generator/functions/remove.mcfunction", "w") as file:

        file.write(f"# Headerline\n")

        for placed_jump in list_of_placed_jumps:

            x = placed_jump.rel_start_block.abs_position[0]
            y = placed_jump.rel_start_block.abs_position[1]
            z = placed_jump.rel_start_block.abs_position[2]

            writestr = f"fill {x} {y} {z} {x} {y} {z} minecraft:air\n"
            file.write(writestr)

            x = placed_jump.rel_finish_block.abs_position[0]
            y = placed_jump.rel_finish_block.abs_position[1]
            z = placed_jump.rel_finish_block.abs_position[2]

            writestr = f"fill {x} {y} {z} {x} {y} {z} minecraft:air\n"
            file.write(writestr)

            

            for block in placed_jump.blocks:

                x = block.abs_position[0]
                y = block.abs_position[1]
                z = block.abs_position[2]

                writestr = f"fill {x} {y} {z} {x} {y} {z} minecraft:air\n"
                file.write(writestr)

print("Done.")

    
