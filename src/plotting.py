from classes import JumpType, Block
import matplotlib.pyplot as plt
import numpy as np

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
            if not plot_command_blocks and "command_block" in block.name:
                continue
            if "pressure_plate" in block.name:
                continue
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

    # max_axis_distance = max(x_max, y_max, z_max)
    # min_axis_distance = min(x_min, y_min, z_min)
    # stepsize = max(abs(max_axis_distance-min_axis_distance)//10, 10)
    # stepsize = max((stepsize // 10) * 10, 10)

    # ax.set_xticks(np.arange(x_min, # type: ignore
    #                 x_max+stepsize, stepsize))
    # ax.set_yticks(np.arange(y_min, # type: ignore
    #                 y_max+stepsize, stepsize))
    # ax.set_zticks(np.arange(z_min, # type: ignore
    #                 z_max+stepsize, stepsize))

    ax.set_xticks([x_min, x_max])
    ax.set_yticks([y_min, y_max])
    ax.set_zticks([z_min, z_max]) # type: ignore

    ax.set_box_aspect((abs(x_max-x_min), abs(y_max-y_min), abs(z_max-z_min))) # type: ignore
    plt.tick_params(labelsize=10) # type: ignore
    ax.set_xlabel("X", labelpad=10)
    ax.set_ylabel("Z", labelpad=10)
    ax.set_zlabel("Y", labelpad=10) # type: ignore

    if plot_file_type == "jpg":
        plt.savefig("parkour_plot.jpg", dpi=150) # type: ignore
    else:
        plt.savefig("parkour_plot.png", dpi=150) # type: ignore
    
    plt.close(fig)
