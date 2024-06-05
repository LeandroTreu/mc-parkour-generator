from classes import JumpType, Block
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def compute_abs_coordinates_of_start_block(jumptype: JumpType, absolut_pos_of_last_block: tuple[int, int, int], forward_direction: str):

    y = absolut_pos_of_last_block[1] + jumptype.rel_start_block.rel_position[1]

    if forward_direction == "Xpos":
        x = absolut_pos_of_last_block[0] + \
            jumptype.rel_start_block.rel_position[0]
        z = absolut_pos_of_last_block[2] + \
            jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Xneg":
        x = absolut_pos_of_last_block[0] - \
            jumptype.rel_start_block.rel_position[0]
        z = absolut_pos_of_last_block[2] - \
            jumptype.rel_start_block.rel_position[2]
    elif forward_direction == "Zpos":
        x = absolut_pos_of_last_block[0] + \
            jumptype.rel_start_block.rel_position[2]
        z = absolut_pos_of_last_block[2] + \
            jumptype.rel_start_block.rel_position[0]
    else:
        x = absolut_pos_of_last_block[0] - \
            jumptype.rel_start_block.rel_position[2]
        z = absolut_pos_of_last_block[2] - \
            jumptype.rel_start_block.rel_position[0]

    return (x, y, z)


def shortcut_possible_checker(old_X: int, old_Y: int, old_Z: int, new_X: int, new_Y: int, new_Z: int):

    # 3 y-levels below (against obstruction of earlier jumps)
    if old_Y == new_Y - 3 and (old_X <= new_X + 2 and old_X >= new_X - 2) and (old_Z <= new_Z + 2 and old_Z >= new_Z - 2):
        return True

    # 2 y-levels below (against obstruction of earlier jumps)
    if old_Y == new_Y - 2 and (old_X <= new_X + 2 and old_X >= new_X - 2) and (old_Z <= new_Z + 2 and old_Z >= new_Z - 2):
        return True

    # One y-level below
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


# Returns True only if the Block is in the config defined Parkour bounds, else False.
# Also considers the height of the player hitbox, leaving 4 blocks headroom below the maximum y value of the volume.
def in_bounds(block: Block, parkour_volume: list[tuple[int, int]]):

    # X coordinate
    if block.abs_position[0] >= parkour_volume[0][0] and block.abs_position[0] <= parkour_volume[0][1]:
        # Y coordinate
        if block.abs_position[1] >= parkour_volume[1][0] and block.abs_position[1] <= parkour_volume[1][1] - 4:
            # Z coordinate
            if block.abs_position[2] >= parkour_volume[2][0] and block.abs_position[2] <= parkour_volume[2][1]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def can_be_placed(jumptype: JumpType, 
                  current_block_position: tuple[int, int, int], 
                  current_forward_direction: str, 
                  list_of_placed_jumps: list[JumpType],
                  enforce_parkour_volume: bool,
                  parkour_volume: list[tuple[int, int]]):

    abs_position = compute_abs_coordinates_of_start_block(
        jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # Check if new Structure is in bounds of the parkour_volume
    if enforce_parkour_volume:
        if not in_bounds(jumptype.rel_start_block, parkour_volume):
            return False
        if not in_bounds(jumptype.rel_finish_block, parkour_volume):
            return False
        for block in jumptype.blocks:
            if not in_bounds(block, parkour_volume):
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


def is_Ascending(jumptype: JumpType) -> bool:

    # TODO: also for rel_finish_block of more complex structures
    if jumptype.rel_start_block.rel_position[1] > 0:
        return True

    return False


def write_function_files(list_of_placed_jumps: list[JumpType], 
                         parkour_volume: list[tuple[int, int]], 
                         enforce_parkour_volume: bool, 
                         fill_volume_with_air: bool) -> None:

    try:
        cwd = Path.cwd()
        datapack_dir = cwd / "parkour_generator_datapack/data/parkour_generator/functions"
        datapack_dir.mkdir(parents=True, exist_ok=True)

        generate_file = datapack_dir / "generate.mcfunction"
        remove_file = datapack_dir / "remove.mcfunction"
    except:
        raise Exception("Error writing files")

    # TODO: Write config file variables as a text header into the file
    # TODO: Command limit per function file is 65,536: gamerule maxCommandChainLength
    # TODO: Research gamerule commandModificationBlockLimit
    with open(generate_file, "w") as file:

        file.write(f"# Headerline\n")

        file.write(f"gamerule spawnRadius 0\n")

        world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
        file.write(f"setworldspawn {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")
        file.write(f"spawnpoint @a {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")
        file.write(f"tp @a {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")

        file.write(f"gamemode adventure @a\n")
        # file.write(f"effect give @a minecraft:saturation 3600 4\n") # TODO: infinite duration
        file.write(f"gamerule doImmediateRespawn true\n")
        file.write(f"gamerule fallDamage false\n")
        file.write(f"gamerule keepInventory true\n")
        file.write(f"gamerule commandBlockOutput false\n")

        # Fill parkour volume with air first if set in config
        if enforce_parkour_volume and fill_volume_with_air:
            volume = parkour_volume
            file.write(f"fill {volume[0][0]} {volume[1][0]} {volume[2][0]} {
                volume[0][1]} {volume[1][1]} {volume[2][1]} minecraft:air\n")

        # Place all jump structures
        for placed_jump in list_of_placed_jumps:

            x = placed_jump.rel_start_block.abs_position[0]
            y = placed_jump.rel_start_block.abs_position[1]
            z = placed_jump.rel_start_block.abs_position[2]

            writestr = f"fill {x} {y} {z} {x} {y} {z} {
                placed_jump.rel_start_block.name}\n"
            file.write(writestr)

            x = placed_jump.rel_finish_block.abs_position[0]
            y = placed_jump.rel_finish_block.abs_position[1]
            z = placed_jump.rel_finish_block.abs_position[2]

            writestr = f"fill {x} {y} {z} {x} {y} {z} {
                placed_jump.rel_finish_block.name}\n"
            file.write(writestr)

            for block in placed_jump.blocks:

                x = block.abs_position[0]
                y = block.abs_position[1]
                z = block.abs_position[2]

                writestr = f"fill {x} {y} {z} {x} {y} {z} {block.name}\n"
                file.write(writestr)

    # TODO: Text header for explanation
    with open(remove_file, "w") as file:

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


def plot_parkour(list_of_placed_jumps: list[JumpType], 
                 parkour_volume: list[tuple[int, int]], 
                 enforce_parkour_volume: bool, 
                 plot_command_blocks: bool,
                 plot_color_scheme: str,
                 plot_file_type: str) -> None:

    fig = plt.figure(figsize=(8, 8)) # type: ignore
    ax = fig.add_subplot(projection='3d') # type: ignore

    x_axis: list[int] = []
    y_axis: list[int] = []
    z_axis: list[int] = []

    non_connected_blocks: list[JumpType] = []
    for placed_jump in list_of_placed_jumps:
    
        if placed_jump.structure_type == "CommandControl":
            if plot_command_blocks:
                non_connected_blocks.append(placed_jump)
                continue
            else:
                continue

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

    # Plot line connecting the blocks
    line_color = "black"
    ax.plot(x_axis, y_axis, z_axis, # type: ignore
            linestyle="-", linewidth=0.5,
            c=line_color, marker="s", markersize=0)

    # Add non-connected blocks for the scatter plot
    for placed_jump in non_connected_blocks:

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
    
    # Plot the blocks
    ax.scatter(x_axis, y_axis, z_axis, c=z_axis, # type: ignore
               cmap=plot_color_scheme, marker="s", s=2, alpha=1) # type: ignore

    # Axis calculations
    if enforce_parkour_volume:
        x_min = parkour_volume[0][0]
        x_max = parkour_volume[0][1]
        y_min = parkour_volume[2][0]
        y_max = parkour_volume[2][1]
        z_min = parkour_volume[1][0]
        z_max = parkour_volume[1][1]
    else:
        x_list: list[int] = []
        y_list: list[int] = []
        z_list: list[int] = []

        for placed_jump in list_of_placed_jumps:
            x_list.append(placed_jump.rel_start_block.abs_position[0])
            # Here the y value is the minecraft z value
            y_list.append(placed_jump.rel_start_block.abs_position[2])
            # height == minecraft y value
            z_list.append(placed_jump.rel_start_block.abs_position[1])
            x_list.append(placed_jump.rel_finish_block.abs_position[0])
            # Here the y value is the minecraft z value
            y_list.append(placed_jump.rel_finish_block.abs_position[2])
            # height == minecraft y value
            z_list.append(placed_jump.rel_finish_block.abs_position[1])

            for block in placed_jump.blocks:
                x_list.append(block.abs_position[0])
                # Here the y value is the minecraft z value
                y_list.append(block.abs_position[2])
                # height == minecraft y value
                z_list.append(block.abs_position[1])

        x_min = min(x_list)
        x_max = max(x_list)
        y_min = min(y_list)
        y_max = max(y_list)
        z_min = min(z_list)
        z_max = max(z_list)

        x_max = ((x_max+10) // 10) * 10
        y_max = ((y_max+10) // 10) * 10
        z_max = ((z_max+10) // 10) * 10
        x_min = (x_min // 10) * 10
        y_min = (y_min // 10) * 10
        z_min = (z_min // 10) * 10

    max_axis_distance = max(x_max, y_max, z_max)
    min_axis_distance = min(x_min, y_min, z_min)
    stepsize = max(abs(max_axis_distance-min_axis_distance)//10, 10)
    stepsize = max((stepsize // 10) * 10, 10)

    ax.set_xticks(np.arange(x_min, # type: ignore
                    x_max+stepsize, stepsize))
    ax.set_yticks(np.arange(y_min, # type: ignore
                    y_max+stepsize, stepsize))
    ax.set_zticks(np.arange(z_min, # type: ignore
                    z_max+stepsize, stepsize))

    ax.set_box_aspect((abs(x_max-x_min), abs(y_max-y_min), abs(z_max-z_min))) # type: ignore
    plt.tick_params(labelsize=10) # type: ignore

    if plot_file_type == "jpg":
        plt.savefig("parkour_plot.jpg") # type: ignore
    else:
        plt.savefig("parkour_plot.png", dpi=300) # type: ignore
