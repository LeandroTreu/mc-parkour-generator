"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
from mpg.classes import JumpType, Block, Cluster
import mpg.config

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


def shortcut_possible_checker(old_X: int, old_Y: int, old_Z: int, new_X: int, new_Y: int, new_Z: int, check_below: bool, check_same_h: bool, check_above: bool):

    if check_below:            
        # 3 y-levels below (against obstruction of earlier jumps)
        if old_Y == new_Y - 3 and (old_X <= new_X + 3 and old_X >= new_X - 3) and (old_Z <= new_Z + 3 and old_Z >= new_Z - 3):
            return True

        # 2 y-levels below (against obstruction of earlier jumps)
        if old_Y == new_Y - 2 and (old_X <= new_X + 3 and old_X >= new_X - 3) and (old_Z <= new_Z + 3 and old_Z >= new_Z - 3):
            return True

        # One y-level below
        if old_Y == new_Y - 1 and (old_X <= new_X + 4 and old_X >= new_X - 4) and (old_Z <= new_Z + 4 and old_Z >= new_Z - 4):
            return True

    if check_same_h:
        # Same height
        if old_Y == new_Y and (old_X <= new_X + 5 and old_X >= new_X - 5) and (old_Z <= new_Z + 5 and old_Z >= new_Z - 5):
            return True

    if check_above:
        # One y-level up
        if old_Y == new_Y + 1 and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
            return True

        # Rest of the volume above the block in a 12x5x12 volume
        if (old_Y >= new_Y + 2 and old_Y <= new_Y + 7) and (old_X <= new_X + 6 and old_X >= new_X - 6) and (old_Z <= new_Z + 6 and old_Z >= new_Z - 6):
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

    if "command_block" in new_block.name:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=False, check_above=False):
            return True
    else:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=True, check_above=True):
            return True

    # Check for the rel finish block
    old_X = earlier_structure.rel_finish_block.abs_position[0]
    old_Y = earlier_structure.rel_finish_block.abs_position[1]
    old_Z = earlier_structure.rel_finish_block.abs_position[2]

    if "command_block" in new_block.name:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=False, check_above=False):
            return True
    else:
        if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=True, check_above=True):
            return True

    for block in earlier_structure.blocks:

        old_X = block.abs_position[0]
        old_Y = block.abs_position[1]
        old_Z = block.abs_position[2]

        if "command_block" in new_block.name:
            if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=False, check_above=False):
                return True
        else:
            if shortcut_possible_checker(old_X, old_Y, old_Z, new_X, new_Y, new_Z, check_below=True, check_same_h=True, check_above=True):
                return True

    return False


# Returns True only if the Block is inside the minecraft world bounds and the config defined Parkour bounds, else False.
# Also considers the height of the player hitbox, leaving 4 blocks headroom below the maximum y value of the volume.
def in_bounds(block: Block, parkour_volume: list[tuple[int, int]], enforce_parkour_volume: bool, mc_version: str):

    x = block.abs_position[0]
    y = block.abs_position[1]
    z = block.abs_position[2]

    if mc_version == "1.13 - 1.17.1":
        max_y = mpg.config.MC_WORLD_MAX_Y_OLD
        min_y = mpg.config.MC_WORLD_MIN_Y_OLD
    else:
        max_y = mpg.config.MC_WORLD_MAX_Y
        min_y = mpg.config.MC_WORLD_MIN_Y

    if x < mpg.config.MC_WORLD_MIN_X or x > mpg.config.MC_WORLD_MAX_X:
        return False
    if y < min_y or y > max_y:
        return False
    if z < mpg.config.MC_WORLD_MIN_Z or z > mpg.config.MC_WORLD_MAX_Z:
        return False

    if enforce_parkour_volume:
        if x < parkour_volume[0][0] or x > parkour_volume[0][1]:
            return False
        if y < parkour_volume[1][0] or y > parkour_volume[1][1] - 4:
            return False
        if z < parkour_volume[2][0] or z > parkour_volume[2][1]:
            return False

    return True

def near_jump(block: Block, earlier_jump: JumpType) -> bool:

    radius = 20
    x = block.abs_position[0]
    y = block.abs_position[1]
    z = block.abs_position[2]
    e_x = earlier_jump.rel_finish_block.abs_position[0]
    e_y = earlier_jump.rel_finish_block.abs_position[1]
    e_z = earlier_jump.rel_finish_block.abs_position[2]

    if abs(x - e_x) < radius and abs(y - e_y) < radius and abs(z - e_z) < radius:
        return True
    
    return False

def can_be_placed(jumptype: JumpType, 
                  current_block_position: tuple[int, int, int], 
                  current_forward_direction: str, 
                  list_of_placed_jumps: list[JumpType],
                  enforce_parkour_volume: bool,
                  parkour_volume: list[tuple[int, int]],
                  mc_version: str,
                  list_of_clusters: list[Cluster]):

    abs_position = compute_abs_coordinates_of_start_block(
        jumptype, current_block_position, current_forward_direction)

    jumptype.set_absolut_coordinates(abs_position, current_forward_direction)

    # Check if new Structure is in bounds of the minecraft world and parkour volume (if enforced)
    if not in_bounds(jumptype.rel_start_block, parkour_volume, enforce_parkour_volume, mc_version):
        return False
    if not in_bounds(jumptype.rel_finish_block, parkour_volume, enforce_parkour_volume, mc_version):
        return False
    for block in jumptype.blocks:
        if not in_bounds(block, parkour_volume, enforce_parkour_volume, mc_version):
            return False
    
    # Check if shortcut possible
    use_clusters = True
    if use_clusters:
        for cluster_index, cluster in enumerate(list_of_clusters):
            if intersects_cluster_volume(jumptype, cluster):
                for earlier_jump_index, earlier_jump in enumerate(cluster.jumps):

                    # Don't check the last placed jump
                    if (cluster_index == len(list_of_clusters) - 1) and (earlier_jump_index == len(cluster.jumps) - 1):
                        continue

                    # If start block not near earlier jump then no detailed checks necessary
                    if not near_jump(jumptype.rel_start_block, earlier_jump):
                        continue

                    if shortcut_possible(jumptype.rel_start_block, earlier_jump):
                        return False
                    if shortcut_possible(jumptype.rel_finish_block, earlier_jump):
                        return False
                    for block in jumptype.blocks:
                        if shortcut_possible(block, earlier_jump):
                            return False
    else:
        # Old version without clusters for debug
        for earlier_jump in list_of_placed_jumps[0:len(list_of_placed_jumps)-1]:

            # If start block not near earlier jump the no detailed checks necessary
            if not near_jump(jumptype.rel_start_block, earlier_jump):
                continue

            if shortcut_possible(jumptype.rel_start_block, earlier_jump):
                return False
            if shortcut_possible(jumptype.rel_finish_block, earlier_jump):
                return False
            for block in jumptype.blocks:
                if shortcut_possible(block, earlier_jump):
                    return False

    return True


def is_ascending(jumptype: JumpType) -> bool:

    if jumptype.rel_start_block.rel_position[1] + jumptype.rel_finish_block.rel_position[1] > 0:
        return True

    return False

def is_descending(jumptype: JumpType) -> bool:

    if jumptype.rel_start_block.rel_position[1] + jumptype.rel_finish_block.rel_position[1] < 0:
        return True

    return False

def append_to_clusters(jump: JumpType, list_of_clusters: list[Cluster]) -> list[Cluster]:

    if len(list_of_clusters) == 0:
        list_of_clusters = [Cluster(jump)]
    else:
        newest_cluster = list_of_clusters[-1]
        if len(newest_cluster.jumps) >= mpg.config.CLUSTER_SIZE:
            list_of_clusters.append(Cluster(jump))
        else:
            newest_cluster.append_jump(jump)
    
    return list_of_clusters

def pop_from_clusters(n_jumps_to_remove: int, list_of_clusters: list[Cluster]) -> list[Cluster]:

    if n_jumps_to_remove <= 0:
        return list_of_clusters
    
    cluster_size = mpg.config.CLUSTER_SIZE
    if len(list_of_clusters) * cluster_size <= n_jumps_to_remove:
        list_of_clusters = []
        return list_of_clusters
    else:
        for i in range(len(list_of_clusters)):
            index = len(list_of_clusters) - 1 - i
            newest_cluster = list_of_clusters[index]

            start = max(0, len(newest_cluster.jumps) - n_jumps_to_remove)
            end = len(newest_cluster.jumps)
            newest_cluster.remove_jumps(start, end)
            n_jumps_to_remove = n_jumps_to_remove - (end - start)

            if n_jumps_to_remove <= 0:
                break
        
        new_list_of_clusters = []
        for cluster in list_of_clusters:
            if len(cluster.jumps) > 0:
                new_list_of_clusters.append(cluster)
        
        return new_list_of_clusters

def intersects_cluster_volume(jump: JumpType, cluster: Cluster) -> bool:

    blocks_to_check = [jump.rel_start_block, jump.rel_finish_block]
    blocks_to_check.extend(jump.blocks)

    for block in blocks_to_check:
        if ((cluster.volume[0][0] <= block.abs_position[0] <= cluster.volume[0][1]) and
            (cluster.volume[1][0] <= block.abs_position[1] <= cluster.volume[1][1]) and
            (cluster.volume[2][0] <= block.abs_position[2] <= cluster.volume[2][1])):
            return True

    return False