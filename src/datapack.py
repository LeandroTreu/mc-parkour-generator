from classes import JumpType, Block
from pathlib import Path

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