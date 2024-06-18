from classes import JumpType, Block
from pathlib import Path
import config
import numpy as np

# 413 x 51 x 127 = 2,675,001
def split_volume(volume: list[tuple[int, int]]) -> list[str]:

    cube_width = config.MC_MAX_FILL_VOLUME_CUBE_WIDTH
    commands = []

    v_x_min = volume[0][0]
    v_y_min = volume[1][0]
    v_z_min = volume[2][0]
    v_x_max = volume[0][1]
    v_y_max = volume[1][1]
    v_z_max = volume[2][1]

    v_x_len = v_x_max - v_x_min
    v_y_len = v_y_max - v_y_min
    v_z_len = v_z_max - v_z_min

    n_x_fill = int(np.ceil(v_x_len / cube_width))
    n_y_fill = int(np.ceil(v_y_len / cube_width))
    n_z_fill = int(np.ceil(v_z_len / cube_width))
    if n_x_fill <= 0: n_x_fill = 1
    if n_y_fill <= 0: n_y_fill = 1
    if n_z_fill <= 0: n_z_fill = 1
    for i in range(n_x_fill):
        x_min = v_x_min + i * cube_width
        x_max = x_min + cube_width
        if x_max > v_x_max: x_max = v_x_max
        for j in range(n_y_fill):
            y_min = v_y_min + j * cube_width
            y_max = y_min + cube_width
            if y_max > v_y_max: y_max = v_y_max
            for k in range(n_z_fill):
                z_min = v_z_min + k * cube_width
                z_max = z_min + cube_width
                if z_max > v_z_max: z_max = v_z_max
                commands.append(f"fill {x_min} {y_min} {z_min} {x_max} {y_max} {z_max} minecraft:air\n")
    
    return commands

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
    # TODO: Command limit per function file is 65,536: gamerule maxCommandChainLength: set to 2,147,483,648 lag? --> create multiple function files
    with open(generate_file, "w") as file:

        file.write(f"# Headerline\n")

        file.write(f"gamerule spawnRadius 0\n")

        world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
        file.write(f"setworldspawn {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")
        file.write(f"spawnpoint @a {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")
        file.write(f"tp @a {world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]}\n")

        file.write(f"gamemode adventure @a\n")
        file.write(f"effect give @a minecraft:saturation 1000000 4 true\n")
        file.write(f"gamerule doImmediateRespawn true\n")  # TODO: only 1.15+
        file.write(f"gamerule fallDamage false\n")  # TODO: only 1.15+
        file.write(f"gamerule keepInventory true\n")
        file.write(f"gamerule commandBlockOutput false\n")

        # Fill parkour volume with air first if set in config
        if enforce_parkour_volume and fill_volume_with_air:
            fill_commands = split_volume(parkour_volume)  # TODO: check correctness ingame
            for line in fill_commands:
                file.write(line)

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