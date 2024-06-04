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

from copy import deepcopy
from numpy.random import default_rng

DIRECTIONS = ["Xpos", "Zneg", "Xneg", "Zpos"]
slopesDirection = 0
spiralTurnCounter = 0

def place_control_command_blocks(command_blocks_instance: JumpType, dispenser_instance: JumpType, list_of_placed_jumps: list[JumpType]) -> None:

    world_spawn = list_of_placed_jumps[0].rel_start_block.abs_position
    # TODO: Smart positioning of the command blocks
    abs_position = (world_spawn[0]-10, world_spawn[1], world_spawn[2]-10)

    if config.StartForwardDirection == "Xpos":
        rotation_degree = 180
    elif config.StartForwardDirection == "Xneg":
        rotation_degree = 0
    elif config.StartForwardDirection == "Zpos":
        rotation_degree = 90
    elif config.StartForwardDirection == "Zneg":
        rotation_degree = -90

    command_block_1_string = 'minecraft:chain_command_block[facing=west]{Command:"' + f'fill {abs_position[0]+6} {abs_position[1]+1} {
        abs_position[2]} {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} minecraft:redstone_block replace' + '"}'
    command_block_2_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'fill {abs_position[0]+6} {
        abs_position[1]+1} {abs_position[2]} {abs_position[0]+6} {abs_position[1]+1} {abs_position[2]} minecraft:air replace' + '"}'
    command_block_3_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + \
        f'kill @e[type=minecraft:fishing_bobber]' + '"}'
    command_block_4_string = 'minecraft:repeating_command_block[facing=west]{Command:"' + f'execute at @e[type=minecraft:fishing_bobber] run tp @p {
        world_spawn[0]} {world_spawn[1]+1} {world_spawn[2]} {rotation_degree} 0' + '"}'

    blocks = [Block(command_block_1_string, (1, 0, 0)),
              Block(command_block_2_string, (2, 0, 0)),
              Block("minecraft:redstone_block", (1, 1, 0)), Block(
        "minecraft:redstone_block", (2, 1, 0)),
        Block(command_block_3_string, (4, 0, 0)),
        Block(command_block_4_string, (6, 0, 0)),
        Block("minecraft:redstone_block", (4, 1, 0)), Block(
        "minecraft:redstone_block", (6, 1, 0)),
    ]
    command_blocks_instance.blocks = blocks
    command_blocks_instance.set_absolut_coordinates(abs_position, "Xpos")

    # Place command block that gives the player a checkpoint teleporter
    dispenser_instance.set_absolut_coordinates(
        (world_spawn[0], world_spawn[1]+2, world_spawn[2]-2), config.StartForwardDirection)


def filter_jumptypes(list_of_allowed_structure_types) -> list[JumpType]:

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

    return list_of_jumptypes_filtered


def change_direction(current_forward_direction: str, rng: any) -> str:

    global slopesDirection
    global spiralTurnCounter

    if config.ParkourType == "Random":
        # Choose possible other directions at random
        random_bit = rng.integers(low=0, high=2)
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

    elif config.ParkourType == "Straight":
        return current_forward_direction  # Keep same direction

    elif config.ParkourType == "StraightCurves":

        # TODO: don't check this here
        if config.StraightCurvesSize < 1 or config.StraightCurvesSize > 10:
            raise Exception(
                "Invalid input for StraightCurvesSize: must be between 1 and 10 (inclusive)")

        random_bit = rng.integers(low=0, high=config.StraightCurvesSize+1)

        # Only change direction with probability 1/(config.StraightCurvesSize+1)
        if random_bit == 1:

            old_direction_index = DIRECTIONS.index(
                current_forward_direction)

            if slopesDirection == -1:
                slopesDirection = 0
                new_direction_index = (old_direction_index + 1) % 4
            elif slopesDirection == 0:
                random_bit = rng.integers(low=0, high=2)
                if random_bit == 0:
                    slopesDirection = -1
                    new_direction_index = (old_direction_index - 1)
                else:
                    slopesDirection = 1
                    new_direction_index = (old_direction_index + 1) % 4
            elif slopesDirection == 1:
                slopesDirection = 0
                new_direction_index = (old_direction_index - 1)

            if new_direction_index < 0:
                new_direction_index = 3

            return DIRECTIONS[new_direction_index]
        else:
            return current_forward_direction

    elif config.ParkourType == "Spiral":
        if config.SpiralType == "Even":
            if spiralTurnCounter >= config.SpiralTurnRate:
                random_bit = 1
                spiralTurnCounter = 0
            else:
                random_bit = 0
                spiralTurnCounter += 1
        else:
            h_bound = config.SpiralTurnProbability+1
            random_bit = rng.integers(low=0, high=h_bound)

        if random_bit == 1:

            old_direction_index = DIRECTIONS.index(
                current_forward_direction)

            if config.SpiralRotation == "clockwise":

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


def place_finish_structure(current_block_position: tuple, current_forward_direction: str, list_of_placed_jumps: list[JumpType]) -> None:

    # Place Finish Structure of the Parkour  TODO: Maybe try to place in bounds of Parkour Volume
    finishblock_instance = deepcopy(FinishBlock)

    if config.EnforceParkourVolume:
        if not util.can_be_placed(finishblock_instance, current_block_position, current_forward_direction, list_of_placed_jumps):

            for index in range(len(list_of_placed_jumps)):

                placed_jump = list_of_placed_jumps[len(
                    list_of_placed_jumps) - 2 - index]

                placed_jump_position = placed_jump.rel_finish_block.abs_position

                if util.can_be_placed(finishblock_instance, placed_jump_position, current_forward_direction, list_of_placed_jumps):

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


def place_checkpoint(current_block_position: tuple, 
                     current_forward_direction: str, 
                     list_of_placed_jumps: list[JumpType], 
                     command_blocks_instance: JumpType, 
                     n_blocks_placed: int, 
                     tryToPlaceCheckpointHere: int) -> tuple[int, bool, int]:

    continue_bool = False
    if tryToPlaceCheckpointHere == n_blocks_placed:
        checkpoint_instance = deepcopy(CheckpointBlock)

        if util.can_be_placed(checkpoint_instance, current_block_position, current_forward_direction, list_of_placed_jumps):

            c_block_abs = command_blocks_instance.rel_start_block.abs_position

            for block in checkpoint_instance.blocks:
                if block.name == "minecraft:light_weighted_pressure_plate":
                    checkpoint_respawn = block.abs_position

            if current_forward_direction == "Xpos":
                rotation_degree = 180
            elif current_forward_direction == "Xneg":
                rotation_degree = 0
            elif current_forward_direction == "Zpos":
                rotation_degree = 90
            elif current_forward_direction == "Zneg":
                rotation_degree = -90

            # TODO: Fix syntax error when trying to place this recursive command
            checkpoint_command_string_recursive = 'minecraft:repeating_command_block[facing=west]{Command:\\"' + f'execute at @e[type=minecraft:fishing_bobber] run tp @p {
                checkpoint_respawn[0]} {checkpoint_respawn[1]} {checkpoint_respawn[2]} {rotation_degree} 0' + '\\"} destroy'
            checkpoint_command_string = 'minecraft:command_block{Command:"' + f'fill {c_block_abs[0]+6} {c_block_abs[1]} {
                c_block_abs[2]} {c_block_abs[0]+6} {c_block_abs[1]} {c_block_abs[2]} {checkpoint_command_string_recursive}' + '"}'

            for block in checkpoint_instance.blocks:
                if block.name == "minecraft:command_block":
                    block.name = checkpoint_command_string

            list_of_placed_jumps.append(checkpoint_instance)

            # Set new absolute coordinates for next iteration
            current_block_position = checkpoint_instance.rel_finish_block.abs_position

            tryToPlaceCheckpointHere = n_blocks_placed + config.CheckPointsPeriod
            n_blocks_placed += 1
            continue_bool = True
            return n_blocks_placed, continue_bool, tryToPlaceCheckpointHere
        else:
            tryToPlaceCheckpointHere = n_blocks_placed + 1
            return n_blocks_placed, continue_bool, tryToPlaceCheckpointHere
    else:
        return n_blocks_placed, continue_bool, tryToPlaceCheckpointHere


def generate_parkour(list_of_placed_jumps: list[JumpType], rng: any, list_of_allowed_structure_types: list[str]) -> None:

    # Place Start Structure of the Parkour
    current_block_position = config.StartPosition
    current_forward_direction = config.StartForwardDirection

    startblock_instance = deepcopy(StartBlock)
    startblock_instance.set_absolut_coordinates(
        current_block_position, current_forward_direction)
    list_of_placed_jumps.append(startblock_instance)

    # Create command block control structure
    command_blocks_instance = deepcopy(CommandBlockControl)
    dispenser_instance = deepcopy(DispenserCommandblock)

    if config.CheckPointsEnabled:
        place_control_command_blocks(
            command_blocks_instance, dispenser_instance, list_of_placed_jumps)

    # Pre-filter allowed jumptypes
    list_of_jumptypes_filtered = filter_jumptypes(
        list_of_allowed_structure_types)

    print(f"Number of filtered jumptypes: {len(list_of_jumptypes_filtered)}")

    try_again_counter = 0
    tryToPlaceCheckpointHere = config.CheckPointsPeriod

    # Search for candidates
    list_of_candidates: list[JumpType] = []
    n_blocks_placed = 0
    print("[", end="")
    # Max parkour length minus Start and Finish structures
    while n_blocks_placed < config.MaxParkourLength - 2:

        # Loading bar print
        if n_blocks_placed % max(config.MaxParkourLength//10, 1) == 0:
            print("=", end="", flush=True)

        if config.CheckPointsEnabled:
            # TODO: check variable updates, simplify
            n_blocks_placed, continue_bool, tryToPlaceCheckpointHere = place_checkpoint(current_block_position, current_forward_direction,
                                                           list_of_placed_jumps, command_blocks_instance, n_blocks_placed, tryToPlaceCheckpointHere)

            if continue_bool:
                continue

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

                old_direction_index = DIRECTIONS.index(
                    current_forward_direction)

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

                current_forward_direction = DIRECTIONS[new_direction_index]
                continue
        else:
            try_again_counter = 0

        # Choose randomly from list of candidates
        random_index: int = rng.integers(low=0, high=len(list_of_candidates))
        next_jump = list_of_candidates[random_index]
        list_of_placed_jumps.append(next_jump)

        # Set new absolute coordinates for next iteration
        current_block_position = next_jump.rel_finish_block.abs_position

        # Clear list of candidates for next iteration
        list_of_candidates = []

        # Change direction for next iteration
        current_forward_direction = change_direction(
            current_forward_direction, rng)

        n_blocks_placed += 1

    place_finish_structure(current_block_position,
                           current_forward_direction, list_of_placed_jumps)

    print(f"] {len(list_of_placed_jumps)}/{config.MaxParkourLength}")

    # Place the Control and Dispenser structures
    if config.CheckPointsEnabled:
        list_of_placed_jumps.append(command_blocks_instance)
        list_of_placed_jumps.append(dispenser_instance)

    return
