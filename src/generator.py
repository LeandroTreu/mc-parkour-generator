import util
from classes import JumpType
from classes import Block
import jumptypes
import tkinter as tk
import tkinter.ttk as ttk

from copy import deepcopy
from numpy.random import Generator
from numpy.random import default_rng
import numpy as np

DIRECTIONS = ["Xpos", "Zneg", "Xneg", "Zpos"]
curvesDirection = 0
spiralTurnCounter = 0


def place_control_command_blocks(command_blocks_instance: JumpType, dispenser_instance: JumpType, list_of_placed_jumps: list[JumpType], start_forward_direction: str) -> None:

    world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
    # TODO: Smart positioning of the command blocks
    abs_position = (world_spawn[0]-10, world_spawn[1], world_spawn[2]-10)

    if start_forward_direction == "Xpos":
        rotation_degree = -90
    elif start_forward_direction == "Xneg":
        rotation_degree = 90
    elif start_forward_direction == "Zpos":
        rotation_degree = 0
    else:
        rotation_degree = -180

    command_block_1_string = 'minecraft:chain_command_block[facing=west]{Command:"' + f'fill {abs_position[0]+6} {abs_position[1]+1} {
        abs_position[2]} {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} minecraft:redstone_block replace' + '"}'
    command_block_2_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'fill {abs_position[0]+6} {
        abs_position[1]+1} {abs_position[2]} {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} minecraft:air replace' + '"}'
    command_block_3_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + \
        f'kill @e[type=minecraft:fishing_bobber]' + '"}'
    command_block_4_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'execute at @e[type=minecraft:fishing_bobber] run tp @p {
        world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]} {rotation_degree} 25' + '"}'

    blocks = [Block(command_block_1_string, (1, 0, 0)),
              Block(command_block_2_string, (2, 0, 0)),
              Block("minecraft:redstone_block", (1, 1, 0)), 
              Block("minecraft:redstone_block", (2, 1, 0)),
              Block(command_block_3_string, (4, 0, 0)),
              Block(command_block_4_string, (6, 0, 0)),
              Block("minecraft:redstone_block", (4, 1, 0)), 
              Block("minecraft:redstone_block", (6, 1, 0)),
    ]
    command_blocks_instance.blocks = blocks
    command_blocks_instance.set_absolut_coordinates(abs_position, "Xpos")

    # Place command block that gives the player a checkpoint teleporter
    if (start_forward_direction == "Xpos" or start_forward_direction == "Xneg"):
        dispenser_instance.set_absolut_coordinates(
            (world_spawn[0], world_spawn[1], world_spawn[2]-2), start_forward_direction)
        button_facing_direction = "north"
    else:
        dispenser_instance.set_absolut_coordinates(
            (world_spawn[0]-2, world_spawn[1], world_spawn[2]), start_forward_direction)
        button_facing_direction = "east"
    
    dispenser_instance.rel_finish_block.name = f"minecraft:stone_button[face=floor, facing={button_facing_direction}]"


def filter_jumptypes(list_of_allowed_structure_types: list[str], use_all_blocks: bool, difficulty: float, flow: float, ascending: bool, block_type: str) -> list[JumpType]:

    list_of_jumptypes = jumptypes.init_jumptypes(block_type=block_type)
    list_of_jumptypes_filtered: list[JumpType] = []
    if use_all_blocks:
        list_of_jumptypes_filtered = list_of_jumptypes
    else:
        for jumptype in list_of_jumptypes:
            if jumptype.structure_type in list_of_allowed_structure_types:
                if jumptype.difficulty >= difficulty - 0.2 and jumptype.difficulty <= difficulty + 0.2:
                    if jumptype.flow >= flow - 0.2 and jumptype.flow <= flow + 0.2:
                        if not ascending and util.is_Ascending(jumptype):
                            continue
                        list_of_jumptypes_filtered.append(jumptype)

    return list_of_jumptypes_filtered


def change_direction(current_forward_direction: str,
                     rng: Generator, parkour_type: str,
                     curves_size: float,
                     spiral_type: str,
                     spiral_turn_rate: int,
                     spiral_turn_prob: float,
                     spiral_rotation: str) -> str:

    global curvesDirection
    global spiralTurnCounter

    if parkour_type == "Random":
        # Choose possible other directions at random
        random_bit = rng.integers(low=0, high=2) # type: ignore
        old_direction_index = DIRECTIONS.index(
            current_forward_direction)

        if random_bit == 0:
            if old_direction_index == 0:
                new_direction_index = 3
            else:
                new_direction_index = old_direction_index - 1
        else:
            new_direction_index = (old_direction_index + 1) % 4

        return DIRECTIONS[new_direction_index]

    elif parkour_type == "Straight":
        return current_forward_direction  # Keep same direction

    elif parkour_type == "Curves":

        curves_size = int((curves_size * 10) // 1)
        if curves_size < 1:
            curves_size = 1
        random_nr = rng.integers(low=0, high=curves_size) # type: ignore

        if random_nr == 0:

            old_direction_index = DIRECTIONS.index(
                current_forward_direction)

            if curvesDirection == -1:
                curvesDirection = 0
                new_direction_index = (old_direction_index + 1) % 4
            elif curvesDirection == 0:
                random_bit = rng.integers(low=0, high=2) # type: ignore
                if random_bit == 0:
                    curvesDirection = -1
                    new_direction_index = (old_direction_index - 1)
                else:
                    curvesDirection = 1
                    new_direction_index = (old_direction_index + 1) % 4
            else:
                curvesDirection = 0
                new_direction_index = (old_direction_index - 1)

            if new_direction_index < 0:
                new_direction_index = 3

            return DIRECTIONS[new_direction_index]
        else:
            return current_forward_direction

    elif parkour_type == "Spiral":
        if spiral_type == "Even":
            if spiralTurnCounter + 1 >= spiral_turn_rate:
                spiral_turn_prob = 100
                spiralTurnCounter = 0
            else:
                spiral_turn_prob = 0
                spiralTurnCounter += 1
        else:
            spiral_turn_prob = int(spiral_turn_prob * 100)
            if spiral_turn_prob > 100:
                spiral_turn_prob = 100
            if spiral_turn_prob < 0:
                spiral_turn_prob = 0

        random_nr = rng.integers(low=0, high=101) # type: ignore
        if random_nr <= spiral_turn_prob:

            old_direction_index = DIRECTIONS.index(
                current_forward_direction)

            if spiral_rotation == "clockwise":

                new_direction_index = (old_direction_index + 1) % 4
            else:
                new_direction_index = old_direction_index - 1

            if new_direction_index < 0:
                new_direction_index = 3

            return DIRECTIONS[new_direction_index]
        else:
            return current_forward_direction

    # Default case
    return current_forward_direction


def place_finish_structure(current_block_position: tuple[int, int, int], 
                           current_forward_direction: str, 
                           list_of_placed_jumps: list[JumpType], 
                           enforce_volume: bool,
                           parkour_volume: list[tuple[int, int]],
                           block_type: str) -> None:

    # Place Finish Structure of the Parkour
    # TODO: Maybe try to place in bounds of Parkour Volume
    # TODO: fix parkour length when backtracking happens
    finishblock_instance = jumptypes.init_finishblock(block_type)

    if enforce_volume:
        if not util.can_be_placed(finishblock_instance, current_block_position, current_forward_direction, list_of_placed_jumps, enforce_volume, parkour_volume):

            for index in range(len(list_of_placed_jumps)):

                placed_jump = list_of_placed_jumps[len(
                    list_of_placed_jumps) - 2 - index]

                placed_jump_position = placed_jump.rel_finish_block.abs_position

                if util.can_be_placed(finishblock_instance, placed_jump_position, current_forward_direction, list_of_placed_jumps, enforce_volume, parkour_volume):

                    list_of_placed_jumps = list_of_placed_jumps[0:len(
                        list_of_placed_jumps) - 2 - index + 1]
                    list_of_placed_jumps.append(finishblock_instance)

                    break
                else:
                    continue
        else:
            list_of_placed_jumps.append(finishblock_instance)
    else:
        abs_position = util.compute_abs_coordinates_of_start_block(
            finishblock_instance, current_block_position, current_forward_direction)
        finishblock_instance.set_absolut_coordinates(
            abs_position, current_forward_direction)
        list_of_placed_jumps.append(finishblock_instance)


# TODO: fix checkpoints never placed for Random parkour_type, because no space
def place_checkpoint(current_block_position: tuple[int, int, int],
                     current_forward_direction: str,
                     list_of_placed_jumps: list[JumpType],
                     command_blocks_instance: JumpType,
                     n_blocks_placed: int,
                     try_to_place_cp_here: int,
                     cp_period: int,
                     enforce_parkour_volume: bool,
                     parkour_volume: list[tuple[int, int]],
                     block_type: str) -> tuple[int, bool, int, tuple[int, int, int]]:

    continue_bool = False
    if try_to_place_cp_here == n_blocks_placed:
        checkpoint_instance = jumptypes.init_checkpointblock(block_type)

        if util.can_be_placed(checkpoint_instance, current_block_position, current_forward_direction, list_of_placed_jumps, enforce_parkour_volume, parkour_volume):

            c_block_abs = command_blocks_instance.rel_start_block.abs_position

            checkpoint_respawn = None
            for block in checkpoint_instance.blocks:
                if block.name == "minecraft:light_weighted_pressure_plate":
                    checkpoint_respawn = block.abs_position
            
            if checkpoint_respawn is None:
                raise Exception("Error: checkpoint_respawn not found")

            if current_forward_direction == "Xpos":
                rotation_degree = -90
            elif current_forward_direction == "Xneg":
                rotation_degree = 90
            elif current_forward_direction == "Zpos":
                rotation_degree = 0
            else:
                rotation_degree = -180

            checkpoint_command_string_recursive = 'minecraft:repeating_command_block[facing=west]{Command:\\"' + f'execute at @e[type=minecraft:fishing_bobber] run tp @p {
                checkpoint_respawn[0]} {checkpoint_respawn[1]} {checkpoint_respawn[2]} {rotation_degree} 25' + '\\"} destroy'
            checkpoint_command_string = 'minecraft:command_block{Command:"' + f'fill {c_block_abs[0]+6} {c_block_abs[1]} {
                c_block_abs[2]} {c_block_abs[0]+6} {c_block_abs[1]} {c_block_abs[2]} {checkpoint_command_string_recursive}' + '"}'

            for block in checkpoint_instance.blocks:
                if block.name == "minecraft:command_block":
                    block.name = checkpoint_command_string

            list_of_placed_jumps.append(checkpoint_instance)

            # Set new absolute coordinates for next iteration
            current_block_position = checkpoint_instance.rel_finish_block.abs_position

            try_to_place_cp_here = n_blocks_placed + cp_period
            n_blocks_placed += 1
            continue_bool = True
            return n_blocks_placed, continue_bool, try_to_place_cp_here, current_block_position
        else:
            try_to_place_cp_here = n_blocks_placed + 1
            return n_blocks_placed, continue_bool, try_to_place_cp_here, current_block_position
    else:
        return n_blocks_placed, continue_bool, try_to_place_cp_here, current_block_position


def generate_parkour(list_of_placed_jumps: list[JumpType],
                     random_seed: bool,
                     seed: int,
                     list_of_allowed_structure_types: list[str],
                     parkour_start_position: tuple[int, int, int],
                     parkour_start_forward_direction: str,
                     parkour_type: str,
                     spiral_rotation: str,
                     max_parkour_length: int,
                     checkpoints_enabled: bool,
                     checkpoints_period: int,
                     use_all_blocks: bool,
                     difficulty: float,
                     flow: float,
                     ascending: bool,
                     curves_size: float,
                     spiral_type: str,
                     spiral_turn_rate: int,
                     spiral_turn_prob: float,
                     enforce_volume: bool,
                     parkour_volume: list[tuple[int, int]],
                     gui_enabled: bool,
                     gui_loading_bar: ttk.Progressbar,
                     gui_window: tk.Tk,
                     block_type: str) -> int:

    # Set seed for the RNG
    if random_seed:
        rng_for_rng = default_rng()
        seed = rng_for_rng.integers(low=0, high=(2**64), dtype=np.uint64)
    rng = default_rng(seed)

    # Place Start Structure of the Parkour
    current_block_position = parkour_start_position
    current_forward_direction = parkour_start_forward_direction

    startblock_instance = jumptypes.init_startblock(block_type)
    startblock_instance.set_absolut_coordinates(current_block_position, current_forward_direction)
    list_of_placed_jumps.append(startblock_instance)

    # Place the Control and Dispenser structures
    command_blocks_instance = jumptypes.init_commandcontrol(block_type)
    dispenser_instance = jumptypes.init_dispenser(block_type)
    if checkpoints_enabled:
        place_control_command_blocks(
            command_blocks_instance, 
            dispenser_instance, 
            list_of_placed_jumps, 
            parkour_start_forward_direction)

    # Pre-filter allowed jumptypes
    list_of_jumptypes_filtered = filter_jumptypes(
        list_of_allowed_structure_types,
        use_all_blocks,
        difficulty,
        flow,
        ascending,
        block_type)

    print(f"Number of filtered jumptypes: {len(list_of_jumptypes_filtered)}")

    try_again_counter = 0
    try_to_place_cp_here = checkpoints_period

    list_of_candidates: list[JumpType] = []
    n_blocks_placed = 0
    print("[", end="")
    # Max parkour length minus Start and Finish structures
    while n_blocks_placed < max_parkour_length - 2:

        # Loading bar print
        if n_blocks_placed % max(max_parkour_length//10, 1) == 0:
            print("=", end="", flush=True)

            if gui_enabled:
                gui_loading_bar["value"] = 100 * (n_blocks_placed / max(max_parkour_length, 1))
                gui_window.update_idletasks()

        if checkpoints_enabled:
            n_blocks_placed, continue_bool, try_to_place_cp_here, current_block_position = place_checkpoint(current_block_position, 
                                                                                                            current_forward_direction,
                                                                                                            list_of_placed_jumps, 
                                                                                                            command_blocks_instance, 
                                                                                                            n_blocks_placed, 
                                                                                                            try_to_place_cp_here, 
                                                                                                            checkpoints_period,
                                                                                                            enforce_volume,
                                                                                                            parkour_volume,
                                                                                                            block_type)

            if continue_bool:
                continue

        list_of_candidates = deepcopy(list_of_jumptypes_filtered)
        no_placeable_jumps_found = True
        while len(list_of_candidates) > 0:

            # Choose randomly from list of allowed jumptypes
            random_index: int = rng.integers(low=0, high=len(list_of_candidates)) # type: ignore
            candidate_instance = deepcopy(list_of_candidates[random_index])
            if util.can_be_placed(candidate_instance, current_block_position, current_forward_direction, list_of_placed_jumps, enforce_volume, parkour_volume):
                list_of_placed_jumps.append(candidate_instance)
                no_placeable_jumps_found = False
                break
            else:
                list_of_candidates.pop(random_index)
                continue
            
        # No placable JumpTypes found
        if no_placeable_jumps_found:
            if try_again_counter >= 4:
                break
            else:
                try_again_counter += 1

                old_direction_index = DIRECTIONS.index(
                    current_forward_direction)

                if parkour_type == "Random":
                    new_direction_index = (old_direction_index + 1) % 4
                elif parkour_type == "Straight":
                    new_direction_index = old_direction_index
                elif parkour_type == "Curves":
                    new_direction_index = (old_direction_index + 1) % 4
                elif parkour_type == "Spiral":
                    if spiral_rotation == "clockwise":
                        new_direction_index = (old_direction_index + 1) % 4
                    else:
                        new_direction_index = old_direction_index - 1
                    if new_direction_index < 0:
                        new_direction_index = 3
                else:
                    new_direction_index = old_direction_index

                current_forward_direction = DIRECTIONS[new_direction_index]
                continue
        else:
            try_again_counter = 0


        # Set new absolute coordinates for next iteration
        current_block_position = list_of_placed_jumps[-1].rel_finish_block.abs_position

        # Change direction for next iteration
        current_forward_direction = change_direction(current_forward_direction, 
                                                     rng, 
                                                     parkour_type, 
                                                     curves_size, 
                                                     spiral_type, 
                                                     spiral_turn_rate, 
                                                     spiral_turn_prob, 
                                                     spiral_rotation)

        n_blocks_placed += 1

    place_finish_structure(current_block_position,
                           current_forward_direction,
                           list_of_placed_jumps,
                           enforce_volume,
                           parkour_volume,
                           block_type)

    print(f"] {len(list_of_placed_jumps)}/{max_parkour_length}")

    # Place command control blocks last so they don't interfere with the block placing checks
    if checkpoints_enabled:
        list_of_placed_jumps.append(command_blocks_instance)
        list_of_placed_jumps.append(dispenser_instance)

    return seed
