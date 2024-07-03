"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
import util
from classes import JumpType
from classes import Block
import jumptypes
import tkinter as tk
import tkinter.ttk as ttk
from copy import deepcopy
from numpy.random import Generator
from numpy.random import default_rng
from numpy import uint64
import config
import threading

def place_control_command_blocks(command_blocks_instance: JumpType, 
                                 dispenser_instance: JumpType,
                                 list_of_placed_jumps: list[JumpType],
                                 start_forward_direction: str,
                                 enforce_volume: bool,
                                 parkour_volume: list[tuple[int, int]]) -> None:

    world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
    
    if start_forward_direction == "Xpos" or start_forward_direction == "Xneg":
        abs_position = (world_spawn[0], world_spawn[1], world_spawn[2]-5)
        # Switch side, trying to place it inside the parkour volume
        if enforce_volume and (abs_position[2] > parkour_volume[2][1] or abs_position[2] < parkour_volume[2][0]):
            abs_position = (world_spawn[0], world_spawn[1], world_spawn[2]+5)
    else:
        abs_position = (world_spawn[0]-5, world_spawn[1], world_spawn[2])
        if enforce_volume and (abs_position[0] > parkour_volume[0][1] or abs_position[0] < parkour_volume[0][0]):
            abs_position = (world_spawn[0]+5, world_spawn[1], world_spawn[2])

    if start_forward_direction == "Xpos":
        rotation_degree = -90
        cb_facing_direction = "west"
    elif start_forward_direction == "Xneg":
        rotation_degree = 90
        cb_facing_direction = "east"
    elif start_forward_direction == "Zpos":
        rotation_degree = 0
        cb_facing_direction = "north"
    else:
        rotation_degree = -180
        cb_facing_direction = "south"

    blocks = [Block("command_block_1_string", (0, 0, 0)),
              Block("command_block_2_string", (1, 0, 0)),
              Block("minecraft:redstone_block", (0, 1, 0)), 
              Block("minecraft:redstone_block", (1, 1, 0)),
              Block("command_block_3_string", (0, 0, -1)),
              Block("command_block_4_string", (1, 0, -1)),
              Block("minecraft:redstone_block", (0, 1, -1)), 
              Block("minecraft:redstone_block", (1, 1, -1)),
    ]
    command_blocks_instance.blocks = blocks
    command_blocks_instance.set_absolut_coordinates(abs_position, start_forward_direction)

    for b in command_blocks_instance.blocks:
        if b.name == "command_block_1_string":
            t = command_blocks_instance.blocks[7]
            b.name = f"minecraft:chain_command_block[facing={cb_facing_direction}]" + "{Command:\"" + f"fill {t.abs_position[0]} {t.abs_position[1]} {
                t.abs_position[2]} {t.abs_position[0]} {t.abs_position[1]} {t.abs_position[2]} minecraft:redstone_block replace\"" + "}"
    
        if b.name == "command_block_2_string":
            t = command_blocks_instance.blocks[7]
            b.name = f"minecraft:repeating_command_block[facing={cb_facing_direction}]" + "{Command:\"" + f"fill {t.abs_position[0]} {
                t.abs_position[1]} {t.abs_position[2]} {t.abs_position[0]} {t.abs_position[1]} {t.abs_position[2]} minecraft:air replace\"" + "}"
    
        if b.name == "command_block_3_string":
            b.name = f"minecraft:repeating_command_block[facing={cb_facing_direction}]" + "{Command:\"" + \
                f"kill @e[type=minecraft:fishing_bobber]\"" + "}"

        if b.name == "command_block_4_string":
            b.name = f"minecraft:repeating_command_block[facing={cb_facing_direction}]" + "{Command:\"" + f"execute at @e[type=minecraft:fishing_bobber] run tp @p {
                world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]} {rotation_degree} 25\"" + "}"


    # Place command block that gives the player a checkpoint teleporter
    if start_forward_direction == "Xpos" or start_forward_direction == "Xneg":
        if enforce_volume and (world_spawn[2]-2 > parkour_volume[2][1] or world_spawn[2]-2 < parkour_volume[2][0]):
            dispenser_instance.set_absolut_coordinates(
                (world_spawn[0], world_spawn[1], world_spawn[2]+2), start_forward_direction)
        else:
            dispenser_instance.set_absolut_coordinates(
                (world_spawn[0], world_spawn[1], world_spawn[2]-2), start_forward_direction)
        button_facing_direction = "north"
    else:
        if enforce_volume and (world_spawn[0]-2 > parkour_volume[0][1] or world_spawn[0]-2 < parkour_volume[0][0]):
            dispenser_instance.set_absolut_coordinates(
                (world_spawn[0]+2, world_spawn[1], world_spawn[2]), start_forward_direction)
        else:
            dispenser_instance.set_absolut_coordinates(
                (world_spawn[0]-2, world_spawn[1], world_spawn[2]), start_forward_direction)
        button_facing_direction = "east"
    
    dispenser_instance.rel_finish_block.name = f"minecraft:stone_button[face=floor, facing={button_facing_direction}]"


def filter_jumptypes(list_of_allowed_structure_types: list[str], use_all_blocks: bool, difficulty: str, pace: str, ascending: bool, descending: bool, block_type: str) -> tuple[list[JumpType], int , int]:

    list_of_jumptypes = jumptypes.init_jumptypes(block_type=block_type)
    list_of_jumptypes_filtered: list[JumpType] = []
    if use_all_blocks:
        list_of_jumptypes_filtered = list_of_jumptypes
    else:
        for jumptype in list_of_jumptypes:
            if jumptype.structure_type in list_of_allowed_structure_types:
                if (pace == "fast" and jumptype.pace in ["fast", "medium"]) or (pace == "medium" and jumptype.pace in ["medium", "slow"]) or (pace == "slow" and jumptype.pace == "slow"):
                    if difficulty == "hard" or (difficulty == "medium" and (jumptype.difficulty in ["easy", "medium"])) or (difficulty == "easy" and jumptype.difficulty == "easy"):
                        if not ascending and util.is_ascending(jumptype):
                            continue
                        if not descending and util.is_descending(jumptype):
                            continue
                        list_of_jumptypes_filtered.append(jumptype)

    return list_of_jumptypes_filtered, len(list_of_jumptypes_filtered), len(list_of_jumptypes)


def change_direction(current_forward_direction: str,
                     rng: Generator, parkour_type: str,
                     curves_size: float,
                     curves_direction: int,
                     spiral_type: str,
                     spiral_turn_rate: int,
                     spiral_turn_prob: float,
                     spiral_rotation: str,
                     spiral_turn_counter: int) -> tuple[str, int, int]:

    if parkour_type == "Random":
        # Choose possible other directions at random
        random_bit = rng.integers(low=0, high=2) # type: ignore
        old_direction_index = config.DIRECTIONS.index(
            current_forward_direction)

        if random_bit == 0:
            if old_direction_index == 0:
                new_direction_index = 3
            else:
                new_direction_index = old_direction_index - 1
        else:
            new_direction_index = (old_direction_index + 1) % 4

        return config.DIRECTIONS[new_direction_index], curves_direction, spiral_turn_counter

    elif parkour_type == "Straight":
        return current_forward_direction, curves_direction, spiral_turn_counter  # Keep same direction

    elif parkour_type == "Curves":

        curves_size = int((curves_size * 10) // 1)
        if curves_size < 1:
            curves_size = 1
        random_nr = rng.integers(low=0, high=curves_size) # type: ignore

        if random_nr == 0:

            old_direction_index = config.DIRECTIONS.index(
                current_forward_direction)

            if curves_direction == -1:
                curves_direction = 0
                new_direction_index = (old_direction_index + 1) % 4
            elif curves_direction == 0:
                random_bit = rng.integers(low=0, high=2) # type: ignore
                if random_bit == 0:
                    curves_direction = -1
                    new_direction_index = (old_direction_index - 1)
                else:
                    curves_direction = 1
                    new_direction_index = (old_direction_index + 1) % 4
            else:
                curves_direction = 0
                new_direction_index = (old_direction_index - 1)

            if new_direction_index < 0:
                new_direction_index = 3

            return config.DIRECTIONS[new_direction_index], curves_direction, spiral_turn_counter
        else:
            return current_forward_direction, curves_direction, spiral_turn_counter

    elif parkour_type == "Spiral":
        if spiral_type == "Even":
            if spiral_turn_counter + 1 >= spiral_turn_rate:
                spiral_turn_prob = 100
                spiral_turn_counter = 0
            else:
                spiral_turn_prob = 0
                spiral_turn_counter += 1
        else:
            spiral_turn_prob = int(spiral_turn_prob * 100)
            if spiral_turn_prob > 100:
                spiral_turn_prob = 100
            if spiral_turn_prob < 0:
                spiral_turn_prob = 0

        random_nr = rng.integers(low=0, high=101) # type: ignore
        if random_nr <= spiral_turn_prob:

            old_direction_index = config.DIRECTIONS.index(
                current_forward_direction)

            if spiral_rotation == "clockwise":

                new_direction_index = (old_direction_index + 1) % 4
            else:
                new_direction_index = old_direction_index - 1

            if new_direction_index < 0:
                new_direction_index = 3

            return config.DIRECTIONS[new_direction_index], curves_direction, spiral_turn_counter
        else:
            return current_forward_direction, curves_direction, spiral_turn_counter

    # Default case
    return current_forward_direction, curves_direction, spiral_turn_counter

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
                     difficulty: str,
                     pace: str,
                     ascending: bool,
                     descending: bool,
                     curves_size: float,
                     spiral_type: str,
                     spiral_turn_rate: int,
                     spiral_turn_prob: float,
                     enforce_volume: bool,
                     parkour_volume: list[tuple[int, int]],
                     gui_enabled: bool,
                     gui_loading_bar: ttk.Progressbar | None,
                     gui_window: tk.Tk | None,
                     block_type: str,
                     t_stop_event: threading.Event | None) -> tuple[int, int, int, list[JumpType]]:

    best_parkour_generated: list[JumpType] = []

    # Set seed for the RNG
    if random_seed:
        rng_for_rng = default_rng()
        seed = rng_for_rng.integers(low=0, high=(2**64), dtype=uint64)
    rng = default_rng(seed)

    current_block_position = parkour_start_position
    current_forward_direction = parkour_start_forward_direction

    # Place Start Structure of the Parkour
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
            parkour_start_forward_direction,
            enforce_volume=enforce_volume,
            parkour_volume=parkour_volume)

    # Pre-filter allowed jumptypes
    list_of_jumptypes_filtered, nr_jumptypes_filtered, nr_total_jumptypes = filter_jumptypes(
        list_of_allowed_structure_types,
        use_all_blocks,
        difficulty,
        pace,
        ascending,
        descending,
        block_type)

    if not gui_enabled:
        print(f"Number of filtered jumptypes: {len(list_of_jumptypes_filtered)}")

    y_level_balance = 0
    curves_direction = 0
    spiral_turn_counter = 0
    try_again_counter = 0
    backtrack_counter = 0
    try_again_limit = 10
    backtrack_limit = 1000

    backtrack_depth = 1
    jump_to_fix = -1

    if not gui_enabled:
        print("[", end="")
    
    while len(list_of_placed_jumps) < max_parkour_length + 1:
        
        if t_stop_event != None and t_stop_event.is_set():
            return seed, nr_jumptypes_filtered, nr_total_jumptypes, []

        # Loading bar print
        if len(list_of_placed_jumps) % max(max_parkour_length//100, 1) == 0:
            if gui_enabled and gui_loading_bar != None and gui_window != None:
                # Leave 5% for other gui tasks
                real_percentage = len(list_of_placed_jumps) / max(max_parkour_length, 1)
                bar_value = min(95*real_percentage, 95)
                gui_loading_bar["value"] = bar_value
                gui_window.update_idletasks()
            else:
                print("=", end="", flush=True)
        
        if len(list_of_placed_jumps) == 1:
            y_level_balance = 0
            curves_direction = 0
            spiral_turn_counter = 0
            try_again_counter = 0

            current_block_position = parkour_start_position
            current_forward_direction = parkour_start_forward_direction

        no_placeable_jumps_found = True
        if len(list_of_placed_jumps) == max_parkour_length:
            # Place Finish Structure of the Parkour
            finishblock_instance = jumptypes.init_finishblock(block_type)
            if util.can_be_placed(finishblock_instance, current_block_position, current_forward_direction, list_of_placed_jumps, enforce_volume, parkour_volume):
                list_of_placed_jumps.append(finishblock_instance)
                no_placeable_jumps_found = False
            else:
                no_placeable_jumps_found = True
        elif checkpoints_enabled and len(list_of_placed_jumps) % checkpoints_period == 0:
            no_placeable_jumps_found = True
            checkpoint_instances = jumptypes.init_checkpointblocks(block_type)

            for cp_instance in checkpoint_instances:
                if util.can_be_placed(cp_instance, current_block_position, current_forward_direction, list_of_placed_jumps, enforce_volume, parkour_volume):

                    c_block_abs = command_blocks_instance.blocks[5].abs_position

                    checkpoint_respawn = None
                    for block in cp_instance.blocks:
                        if block.name == "minecraft:stone_pressure_plate":
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
                    checkpoint_command_string = 'minecraft:command_block{Command:"' + f'fill {c_block_abs[0]} {c_block_abs[1]} {
                        c_block_abs[2]} {c_block_abs[0]} {c_block_abs[1]} {c_block_abs[2]} {checkpoint_command_string_recursive}' + '"}'

                    for block in cp_instance.blocks:
                        if block.name == "minecraft:command_block":
                            block.name = checkpoint_command_string

                    list_of_placed_jumps.append(cp_instance)
                    no_placeable_jumps_found = False
                    break
        else:
            list_of_candidates = deepcopy(list_of_jumptypes_filtered)
            no_placeable_jumps_found = True
            while len(list_of_candidates) > 0:

                # Choose randomly from list of allowed jumptypes
                random_index = rng.integers(low=0, high=len(list_of_candidates)) # type: ignore
                candidate_instance = deepcopy(list_of_candidates[random_index])

                # Keep a balanced y-level when both ascending and descending JumpTypes are set
                candidate_y_change = candidate_instance.rel_start_block.rel_position[1] + candidate_instance.rel_finish_block.rel_position[1]
                if ascending and descending:
                    if (y_level_balance > 0 and candidate_y_change > 0) or (y_level_balance < 0 and candidate_y_change < 0):
                        random_nr = rng.integers(low=0, high=abs(y_level_balance)+1)
                        if random_nr != 0:
                            list_of_candidates.pop(random_index)
                            continue
                
                # Check if can be placed
                if util.can_be_placed(candidate_instance, current_block_position, current_forward_direction, list_of_placed_jumps, enforce_volume, parkour_volume):
                    list_of_placed_jumps.append(candidate_instance)
                    y_level_balance += candidate_y_change
                    no_placeable_jumps_found = False
                    break
                else:
                    list_of_candidates.pop(random_index)
                    continue

        # No placable JumpTypes found
        if no_placeable_jumps_found:
            if try_again_counter > try_again_limit or backtrack_counter > backtrack_limit:
                if not gui_enabled:
                    print("WARNING: too many backtrack attempts")
                break
            else:
                backtrack_counter += 1
                if jump_to_fix == len(list_of_placed_jumps):
                    backtrack_depth = min(backtrack_depth*2, 32)
                    try_again_counter += 1
                else:
                    jump_to_fix = len(list_of_placed_jumps)
                    backtrack_depth = max(backtrack_depth//2, 1)
                    try_again_counter = 0

                bt_len = max(len(list_of_placed_jumps) - backtrack_depth, 1)

                # If checkpoints are enabled, backtrack to the last checkpoint
                if try_again_counter < try_again_limit // 2:
                    for i_cp, replaced_jump in enumerate(list_of_placed_jumps[bt_len:len(list_of_placed_jumps)]):
                        if replaced_jump.structure_type == "Checkpoint":
                            checkpoint_distance = max(len(list_of_placed_jumps) - bt_len - i_cp - 1, 1)
                            backtrack_depth = min(backtrack_depth, checkpoint_distance)

                bt_len = max(len(list_of_placed_jumps) - backtrack_depth, 1)

                list_of_placed_jumps = list_of_placed_jumps[0:bt_len]

        # Set new absolute coordinates for next iteration
        current_block_position = list_of_placed_jumps[-1].rel_finish_block.abs_position

        # Change direction for next iteration
        current_forward_direction, \
        curves_direction, \
        spiral_turn_counter = change_direction( current_forward_direction, 
                                                rng, 
                                                parkour_type, 
                                                curves_size, 
                                                curves_direction,
                                                spiral_type, 
                                                spiral_turn_rate, 
                                                spiral_turn_prob, 
                                                spiral_rotation,
                                                spiral_turn_counter)
        
        if len(list_of_placed_jumps) > len(best_parkour_generated):
            best_parkour_generated = deepcopy(list_of_placed_jumps)

    if not gui_enabled:
        print(f"] {len(best_parkour_generated)-1}/{max_parkour_length}")

    # Place command control blocks last so they are not treated as part of the parkour
    if checkpoints_enabled:
        best_parkour_generated.append(command_blocks_instance)
        best_parkour_generated.append(dispenser_instance)

    return seed, nr_jumptypes_filtered, nr_total_jumptypes, best_parkour_generated
