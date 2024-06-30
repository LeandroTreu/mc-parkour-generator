"""
Copyright 2023-2024 Leandro Treu

This file is part of Minecraft Parkour Generator (MPG).

MPG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
MPG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with MPG. If not, see <https://www.gnu.org/licenses/>.
"""
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import config
import time
from tkinter import font
from tkinter import messagebox
import generator
import plotting
import datapack
from classes import JumpType, Block

class Gui():

    image_size = (800, 800)
    font_title = ("Segoe UI", 10, "bold")
    font_general = ("Segoe UI", 9, "normal")
    label_pad_y = 3

    def __init__(self) -> None:

        self.list_of_placed_jumps: list[JumpType] = []

        self.window = tk.Tk()
        self.window.title("Minecraft Parkour Generator")
        # TODO: create .ico file
        try:
            mpg_icon = Image.open("mpg_icon_256.png")
            # mpg_icon = mpg_icon.resize((50, 50))
            mpg_icon = ImageTk.PhotoImage(mpg_icon)
            self.window.iconphoto(False, mpg_icon) # type: ignore
        except:
            print("Info: mpg_icon.png not found")

        default_font = font.nametofont("TkDefaultFont")
        text_font = font.nametofont("TkTextFont")
        fixed_font = font.nametofont("TkFixedFont")
        # print(default_font.actual())
        # print(text_font.actual())
        # print(fixed_font.actual())
        default_font.configure(family=self.font_general[0], size=self.font_general[1], weight=self.font_general[2])
        text_font.configure(family=self.font_general[0], size=self.font_general[1], weight=self.font_general[2])
        fixed_font.configure(family=self.font_general[0], size=self.font_general[1], weight=self.font_general[2])
        
        self.create_menu()

        self.settings = config.import_config(gui_enabled=True)
        error_str = config.check_config(self.settings)
        if error_str != "":
            messagebox.showerror("Error in settings.json", error_str)
            self.settings = config.set_default_config()
            messagebox.showwarning("Settings Warning", "Reverted to default settings because of an Error")

        # Map settings to tkinter Variables
        self.variables = {}
        self.set_variables()

        self.settings_frame = ttk.Frame(master=self.window, relief="flat", borderwidth=5)
        self.settings_frame.pack(expand=False, side=tk.LEFT)

        # Image frame and label
        self.image_frame = ttk.Frame(master=self.window, relief="flat", borderwidth=5)
        self.image_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        try:
            if self.settings["plotFileType"] == "png":
                self.img = Image.open("parkour_plot.png")
            else:
                self.img = Image.open("parkour_plot.jpg")
            self.img = self.img.resize(self.image_size)
            self.img = ImageTk.PhotoImage(self.img)
            self.img_label = tk.Label(self.image_frame, image=self.img) # type: ignore
            self.img_label.pack(expand=True, fill=tk.BOTH)
        except:
            self.img_label = tk.Label(self.image_frame)
            self.img_label.pack(expand=True, fill=tk.BOTH)

        self.populate_settings_frame()
    
    def set_variables(self):
        for (name, value) in self.settings.items():

            if name == "parkourVolume":
                self.variables["parkourVolume_x1"] = tk.StringVar(master=self.window, value=value[0][0])
                self.variables["parkourVolume_x2"] = tk.StringVar(master=self.window, value=value[0][1])
                self.variables["parkourVolume_y1"] = tk.StringVar(master=self.window, value=value[1][0])
                self.variables["parkourVolume_y2"] = tk.StringVar(master=self.window, value=value[1][1])
                self.variables["parkourVolume_z1"] = tk.StringVar(master=self.window, value=value[2][0])
                self.variables["parkourVolume_z2"] = tk.StringVar(master=self.window, value=value[2][1])
            elif name == "startPosition":
                self.variables["startPosition_x"] = tk.StringVar(master=self.window, value=value[0])
                self.variables["startPosition_y"] = tk.StringVar(master=self.window, value=value[1])
                self.variables["startPosition_z"] = tk.StringVar(master=self.window, value=value[2])
            elif name == "allowedStructureTypes":
                if "SingleBlock" in value:
                    self.variables["allowedStructureTypes_sb"] = tk.BooleanVar(master=self.window, value=True)
                else:
                    self.variables["allowedStructureTypes_sb"] = tk.BooleanVar(master=self.window, value=False)
                if "TwoBlock" in value:
                    self.variables["allowedStructureTypes_tb"] = tk.BooleanVar(master=self.window, value=True)
                else:
                    self.variables["allowedStructureTypes_tb"] = tk.BooleanVar(master=self.window, value=False)
                if "FourBlock" in value:
                    self.variables["allowedStructureTypes_fb"] = tk.BooleanVar(master=self.window, value=True)
                else:
                    self.variables["allowedStructureTypes_fb"] = tk.BooleanVar(master=self.window, value=False)
            elif type(value) is bool:
                self.variables[name] = tk.BooleanVar(master=self.window, value=value)
            elif type(value) is str:
                self.variables[name] = tk.StringVar(master=self.window, value=value)
            elif type(value) is int:
                self.variables[name] = tk.StringVar(master=self.window, value=str(value))
            elif type(value) is float:
                self.variables[name] = tk.StringVar(master=self.window, value=str(value))
            else:
                self.variables[name] = tk.StringVar(master=self.window, value=str(value))

    def refresh_variables(self):
        for (name, value) in self.settings.items():

            if name == "parkourVolume":
                self.variables["parkourVolume_x1"].set(value[0][0])
                self.variables["parkourVolume_x2"].set(value[0][1])
                self.variables["parkourVolume_y1"].set(value[1][0])
                self.variables["parkourVolume_y2"].set(value[1][1])
                self.variables["parkourVolume_z1"].set(value[2][0])
                self.variables["parkourVolume_z2"].set(value[2][1])
            elif name == "startPosition":
                self.variables["startPosition_x"].set(value[0])
                self.variables["startPosition_y"].set(value[1])
                self.variables["startPosition_z"].set(value[2])
            elif name == "allowedStructureTypes":
                if "SingleBlock" in value:
                    self.variables["allowedStructureTypes_sb"].set(True)
                else:
                    self.variables["allowedStructureTypes_sb"].set(False)
                if "TwoBlock" in value:
                    self.variables["allowedStructureTypes_tb"].set(True)
                else:
                    self.variables["allowedStructureTypes_tb"].set(False)
                if "FourBlock" in value:
                    self.variables["allowedStructureTypes_fb"].set(True)
                else:
                    self.variables["allowedStructureTypes_fb"].set(False)
            elif type(value) is bool:
                self.variables[name].set(value)
            elif type(value) is str:
                self.variables[name].set(value)
            elif type(value) is int:
                self.variables[name].set(str(value))
            elif type(value) is float:
                self.variables[name].set(str(value))
            else:
                self.variables[name].set(str(value))

    def create_menu(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Settings", command=self.save_settings)
        file_menu.add_command(label="Reset Settings", command=self.reset_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)

    def populate_settings_frame(self):

        # Settings
        self.minecraft_version_l = ttk.Label(master=self.settings_frame, text="Minecraft Version:")
        self.minecraft_version = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["mcVersion"], values=config.MC_VERSIONS)

        self.enforce_cb = ttk.Checkbutton(master=self.settings_frame, text="Enforce Parkour Volume", variable=self.variables["enforceParkourVolume"], onvalue=True, offvalue=False, command=self.update_vis)
        self.fill_air_cb = ttk.Checkbutton(master=self.settings_frame, text="Fill Volume with Air", variable=self.variables["fillParkourVolumeWithAir"], onvalue=True, offvalue=False, state="disabled", command=self.update_vis)

        self.parkour_volume_label = ttk.Label(master=self.settings_frame, text="Parkour Volume:", state="disabled")
        self.parkour_volume_x1_l = ttk.Label(master=self.settings_frame, text="X:", state="disabled")
        self.parkour_volume_x2_l = ttk.Label(master=self.settings_frame, text="to", state="disabled")
        self.parkour_volume_y1_l = ttk.Label(master=self.settings_frame, text="Y:", state="disabled")
        self.parkour_volume_y2_l = ttk.Label(master=self.settings_frame, text="to", state="disabled")
        self.parkour_volume_z1_l = ttk.Label(master=self.settings_frame, text="Z:", state="disabled")
        self.parkour_volume_z2_l = ttk.Label(master=self.settings_frame, text="to", state="disabled")
        self.parkour_volume_x1 = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume_x1"], state="disabled", width=10)
        self.parkour_volume_x2 = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume_x2"], state="disabled", width=10)
        self.parkour_volume_y1 = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume_y1"], state="disabled", width=10)
        self.parkour_volume_y2 = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume_y2"], state="disabled", width=10)
        self.parkour_volume_z1 = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume_z1"], state="disabled", width=10)
        self.parkour_volume_z2 = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume_z2"], state="disabled", width=10)

        self.parkour_length_label = ttk.Label(master=self.settings_frame, text="Max Parkour Length:")
        self.parkour_length = ttk.Entry(master=self.settings_frame, textvariable=self.variables["maxParkourLength"], width=10)

        self.start_position_label = ttk.Label(master=self.settings_frame, text="Start Coordinates:")
        self.start_position_x_l = ttk.Label(master=self.settings_frame, text="X:")
        self.start_position_y_l = ttk.Label(master=self.settings_frame, text="Y:")
        self.start_position_z_l = ttk.Label(master=self.settings_frame, text="Z:")
        self.start_position_x = ttk.Entry(master=self.settings_frame, textvariable=self.variables["startPosition_x"], width=10)
        self.start_position_y = ttk.Entry(master=self.settings_frame, textvariable=self.variables["startPosition_y"], width=10)
        self.start_position_z = ttk.Entry(master=self.settings_frame, textvariable=self.variables["startPosition_z"], width=10)

        self.start_forward_dir_l = ttk.Label(master=self.settings_frame, text="Start Forward Direction:")
        self.start_forward_dir = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["startForwardDirection"], values=config.DIRECTIONS, width=10, state="readonly")

        self.block_type_l = ttk.Label(master=self.settings_frame, text="Parkour Block Type:")
        self.block_type = ttk.Entry(master=self.settings_frame, textvariable=self.variables["blockType"], width=25)

        self.random_seed = ttk.Checkbutton(master=self.settings_frame, text="Random Seed", variable=self.variables["randomSeed"], onvalue=True, offvalue=False, command=self.update_vis)
        self.seed = ttk.Entry(master=self.settings_frame, textvariable=self.variables["seed"], width=25)

        self.cp_enabled = ttk.Checkbutton(master=self.settings_frame, text="Checkpoints", variable=self.variables["checkpointsEnabled"], onvalue=True, offvalue=False, command=self.update_vis)
        self.cp_period_l = ttk.Label(master=self.settings_frame, text="Checkpoints Period:")
        self.cp_period = ttk.Entry(master=self.settings_frame, textvariable=self.variables["checkpointsPeriod"], width=10)

        self.use_all_blocks = ttk.Checkbutton(master=self.settings_frame, text="Use all JumpTypes", variable=self.variables["useAllBlocks"], onvalue=True, offvalue=False, command=self.update_vis)
        self.allowed_str_types_l = ttk.Label(master=self.settings_frame, text="Allowed JumpTypes:")
        self.t_one_block = ttk.Checkbutton(master=self.settings_frame, text="SingleBlock", variable=self.variables["allowedStructureTypes_sb"], onvalue=True, offvalue=False, command=self.update_vis)
        self.t_two_block = ttk.Checkbutton(master=self.settings_frame, text="TwoBlock", variable=self.variables["allowedStructureTypes_tb"], onvalue=True, offvalue=False, command=self.update_vis)
        self.t_four_block = ttk.Checkbutton(master=self.settings_frame, text="FourBlock", variable=self.variables["allowedStructureTypes_fb"], onvalue=True, offvalue=False, command=self.update_vis)

        self.difficulty_l = ttk.Label(master=self.settings_frame, text=f"Difficulty")
        self.difficulty = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["difficulty"], values=config.DIFFICULTIES)
        self.pace_l = ttk.Label(master=self.settings_frame, text=f"Pace")
        self.pace = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["pace"], values=config.PACE)

        self.parkour_type_l = ttk.Label(master=self.settings_frame, text="Parkour Type:")
        self.parkour_type = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["parkourType"], values=config.PARKOUR_TYPE_NAMES, width=10, state="readonly")
        self.parkour_type.bind("<<ComboboxSelected>>", self.update_vis) # type: ignore
        self.ascending = ttk.Checkbutton(master=self.settings_frame, text="Ascending Jumps", variable=self.variables["parkourAscending"], onvalue=True, offvalue=False, command=self.update_vis)
        self.descending = ttk.Checkbutton(master=self.settings_frame, text="Descending Jumps", variable=self.variables["parkourDescending"], onvalue=True, offvalue=False, command=self.update_vis)

        self.curves_size_l = ttk.Label(master=self.settings_frame, text=f"Curves Size: {(((self.settings["curvesSize"]*10)//1) / 10)}")
        self.curves_size = ttk.Scale(master=self.settings_frame, variable=self.variables["curvesSize"], from_=0.1, to=1.0, command=self.show_curves_size)

        self.spiral_rotation_l = ttk.Label(master=self.settings_frame, text="Spiral Rotation:")
        self.spiral_rotation = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["spiralRotation"], values=config.SPIRAL_ROTATIONS, width=10)
        self.spiral_type_l = ttk.Label(master=self.settings_frame, text="Spiral Type:")
        self.spiral_type = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["spiralType"], values=config.SPIRAL_TYPES, width=10)
        self.spiral_type.bind("<<ComboboxSelected>>", self.update_vis) # type: ignore
        self.spiral_turnrate_l = ttk.Label(master=self.settings_frame, text="Spiral Turn Rate:")
        self.spiral_turnrate = ttk.Entry(master=self.settings_frame, textvariable=self.variables["spiralTurnRate"], width=10)
        self.spiral_turn_prob_l = ttk.Label(master=self.settings_frame, text=f"Spiral Turn Probability: {(((self.settings["spiralTurnProbability"]*10)//1) / 10)}")
        self.spiral_turn_prob = ttk.Scale(master=self.settings_frame, variable=self.variables["spiralTurnProbability"], from_=0, to=1.0, command=self.show_spiral_prob)

        # File options
        self.plot_file_type_l = ttk.Label(master=self.settings_frame, text="Plot File Type:")
        self.plot_file_type = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["plotFileType"], values=config.PLOT_FILE_TYPES, width=10, state="readonly")
        self.plot_file_type.bind("<<ComboboxSelected>>", self.refresh_plot) # type: ignore
        self.plot_colorscheme_l = ttk.Label(master=self.settings_frame, text="Plot Colorscheme:")
        self.plot_colorscheme = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["plotColorScheme"], values=config.PLOT_COLORSCHEMES, width=10, state="readonly")
        self.plot_colorscheme.bind("<<ComboboxSelected>>", self.refresh_plot) # type: ignore
        self.plot_commandblocks = ttk.Checkbutton(master=self.settings_frame, text="Plot Commandblocks", variable=self.variables["plotCommandBlocks"], onvalue=True, offvalue=False, command=self.refresh_plot)
        self.write_datapack_files = ttk.Checkbutton(master=self.settings_frame, text="Write Datapack Files", variable=self.variables["writeDatapackFiles"], onvalue=True, offvalue=False, command=self.update_vis)

        self.mc_settings_l = ttk.Label(master=self.settings_frame, text="Minecraft Settings", font=self.font_title)
        self.mc_settings_l.grid(row=49, column=100, sticky="W", padx=0, pady=0)
        self.minecraft_version_l.grid(row=50, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.minecraft_version.grid(row=50, column=101, sticky="W", padx=0, pady=0)

        self.separator_mc = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_mc.grid(row=80, columns=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)

        self.settings_label = ttk.Label(master=self.settings_frame, text="Parkour Settings", font=self.font_title)
        self.settings_label.grid(row=101, column=100, sticky="W", padx=0, pady=0)

        self.enforce_cb.grid(row=110, column=100, sticky="W", padx=0, pady=0)
        self.fill_air_cb.grid(row=110, column=101, sticky="W", padx=0, pady=0)
        self.parkour_volume_label.grid(row=110, column=110, sticky="W", padx=0, pady=self.label_pad_y)
        self.parkour_volume_x1_l.grid(row=111, column=111, sticky="W", padx=0, pady=0)
        self.parkour_volume_x1.grid(row=111, column=112, sticky="W", padx=0, pady=0)
        self.parkour_volume_x2_l.grid(row=111, column=113, sticky="W", padx=0, pady=0)
        self.parkour_volume_x2.grid(row=111, column=114, sticky="W", padx=0, pady=0)
        self.parkour_volume_y1_l.grid(row=112, column=111, sticky="W", padx=0, pady=0)
        self.parkour_volume_y1.grid(row=112, column=112, sticky="W", padx=0, pady=0)
        self.parkour_volume_y2_l.grid(row=112, column=113, sticky="W", padx=0, pady=0)
        self.parkour_volume_y2.grid(row=112, column=114, sticky="W", padx=0, pady=0)
        self.parkour_volume_z1_l.grid(row=113, column=111, sticky="W", padx=0, pady=0)
        self.parkour_volume_z1.grid(row=113, column=112, sticky="W", padx=0, pady=0)
        self.parkour_volume_z2_l.grid(row=113, column=113, sticky="W", padx=0, pady=0)
        self.parkour_volume_z2.grid(row=113, column=114, sticky="W", padx=0, pady=0)
        self.parkour_length_label.grid(row=111, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.parkour_length.grid(row=111, column=101, sticky="W", padx=0, pady=0)
        self.start_position_label.grid(row=114, column=110, sticky="W", padx=0, pady=self.label_pad_y)
        self.start_position_x_l.grid(row=115, column=111, sticky="W", padx=0, pady=0)
        self.start_position_x.grid(row=115, column=112, sticky="W", padx=0, pady=0)
        self.start_position_y_l.grid(row=115, column=113, sticky="W", padx=0, pady=0)
        self.start_position_y.grid(row=115, column=114, sticky="W", padx=0, pady=0)
        self.start_position_z_l.grid(row=115, column=115, sticky="W", padx=0, pady=0)
        self.start_position_z.grid(row=115, column=116, sticky="W", padx=0, pady=0)
        self.start_forward_dir_l.grid(row=112, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.start_forward_dir.grid(row=112, column=101, sticky="W", padx=0, pady=0)
        self.block_type_l.grid(row=113, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.block_type.grid(row=113, column=101, sticky="W", padx=0, pady=0)
        self.random_seed.grid(row=114, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        # self.seed_label = ttk.Label(master=self.settings_frame, text="Seed:")
        # self.seed_label.grid(row=220, column=101, sticky="W", padx=0, pady=0)
        self.seed.grid(row=114, column=101, sticky="W", padx=0, pady=0)

        self.separator_cp = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_cp.grid(row=250, columns=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.cp_label = ttk.Label(master=self.settings_frame, text="Checkpoints", font=self.font_title)
        self.cp_label.grid(row=251, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.cp_enabled.grid(row=260, column=100, sticky="W", padx=0, pady=0)
        self.cp_period_l.grid(row=260, column=101, sticky="W", padx=0, pady=0)
        self.cp_period.grid(row=260, column=102, sticky="W", padx=0, pady=0)

        self.separator_str = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_str.grid(row=300, columns=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.jt_label = ttk.Label(master=self.settings_frame, text="Jump Types", font=self.font_title)
        self.jt_label.grid(row=301, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.use_all_blocks.grid(row=310, column=100, sticky="W", padx=0, pady=0)
        self.allowed_str_types_l.grid(row=310, column=101, sticky="W", padx=0, pady=0)
        self.t_one_block.grid(row=310, column=103, sticky="W", padx=0, pady=0)
        self.t_two_block.grid(row=311, column=103, sticky="W", padx=0, pady=0)
        self.t_four_block.grid(row=312, column=103, sticky="W", padx=0, pady=0)
        self.ascending.grid(row=310, column=102, sticky="W", padx=0, pady=self.label_pad_y)
        self.descending.grid(row=311, column=102, sticky="W", padx=0, pady=self.label_pad_y)

        self.difficulty_l.grid(row=410, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.difficulty.grid(row=411, column=100, sticky="W", padx=0, pady=0)
        self.pace_l.grid(row=410, column=101, sticky="W", padx=0, pady=0)
        self.pace.grid(row=411, column=101, sticky="W", padx=0, pady=0)

        self.separator_pktypes = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_pktypes.grid(row=500, column=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.pt_label = ttk.Label(master=self.settings_frame, text="Parkour Type", font=self.font_title)
        self.pt_label.grid(row=501, column=100, sticky="W", padx=0, pady=0)
        self.parkour_type_l.grid(row=510, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.parkour_type.grid(row=510, column=101, sticky="W", padx=0, pady=0)
        self.curves_size_l.grid(row=540, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.curves_size.grid(row=540, column=101, sticky="W", padx=0, pady=0)
        self.spiral_rotation_l.grid(row=550, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.spiral_rotation.grid(row=550, column=101, sticky="W", padx=0, pady=0)
        self.spiral_type_l.grid(row=560, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.spiral_type.grid(row=560, column=101, sticky="W", padx=0, pady=0)
        self.spiral_turnrate_l.grid(row=570, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.spiral_turnrate.grid(row=570, column=101, sticky="W", padx=0, pady=0)
        self.spiral_turn_prob_l.grid(row=580, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.spiral_turn_prob.grid(row=580, column=101, sticky="W", padx=0, pady=0)

        # File options
        self.separator_file_options = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_file_options.grid(row=600, column=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.file_options_label = ttk.Label(master=self.settings_frame, text="File Settings", font=self.font_title)
        self.file_options_label.grid(row=601, column=100, sticky="W", padx=0, pady=0)
        self.write_datapack_files.grid(row=602, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.plot_commandblocks.grid(row=602, column=101, sticky="W", padx=0, pady=0)
        self.plot_file_type_l.grid(row=610, column=100, sticky="W", padx=0, pady=self.label_pad_y)
        self.plot_file_type.grid(row=611, column=100, sticky="W", padx=0, pady=0)
        self.plot_colorscheme_l.grid(row=610, column=101, sticky="W", padx=0, pady=0)
        self.plot_colorscheme.grid(row=611, column=101, sticky="W", padx=0, pady=0)

        self.separator_generate = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_generate.grid(row=999, column=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)

        # Generate Frame
        self.generate_frame = ttk.Frame(master=self.settings_frame, relief="flat", borderwidth=5)
        self.generate_frame.grid(row=1000, column=100, columnspan=200, sticky="EW", padx=5, pady=5)

        # Generate Button
        self.generate_button = ttk.Button(master=self.generate_frame, text="Generate Parkour", padding=8, command=self.generate_parkour)
        self.generate_button.pack(fill=tk.BOTH, expand=False, side=tk.TOP)

        # Loading Bar
        self.loadingbar = ttk.Progressbar(master=self.generate_frame, value=0)
        self.loadingbar.pack(fill=tk.BOTH, expand=True, side=tk.TOP, padx=0, pady=5)

        # Task Info Labels
        self.task_info_label = ttk.Label(master=self.generate_frame, text="Generation: ... s    Datapack: ... s    Plot: ... s")
        self.task_info_label.pack(side=tk.TOP, padx=5, pady=5)
        self.jumps_placed_l = ttk.Label(master=self.generate_frame, text="JumpTypes used: ...    Jumps Placed: ...")
        self.jumps_placed_l.pack(side=tk.TOP, padx=5, pady=5)

        self.update_vis("")
    
    def update_vis(self, string=""):

        if self.variables["enforceParkourVolume"].get() is True:
            self.fill_air_cb["state"] = "normal"
            self.parkour_volume_label["state"] = "normal"
            self.parkour_volume_x1_l["state"] = "normal"
            self.parkour_volume_x1["state"] = "normal"
            self.parkour_volume_x2_l["state"] = "normal"
            self.parkour_volume_x2["state"] = "normal"
            self.parkour_volume_y1_l["state"] = "normal"
            self.parkour_volume_y1["state"] = "normal"
            self.parkour_volume_y2_l["state"] = "normal"
            self.parkour_volume_y2["state"] = "normal"
            self.parkour_volume_z1_l["state"] = "normal"
            self.parkour_volume_z1["state"] = "normal"
            self.parkour_volume_z2_l["state"] = "normal"
            self.parkour_volume_z2["state"] = "normal"
        else:
            self.fill_air_cb["state"] = "disabled"
            self.parkour_volume_label["state"] = "disabled"
            self.parkour_volume_x1_l["state"] = "disabled"
            self.parkour_volume_x1["state"] = "disabled"
            self.parkour_volume_x2_l["state"] = "disabled"
            self.parkour_volume_x2["state"] = "disabled"
            self.parkour_volume_y1_l["state"] = "disabled"
            self.parkour_volume_y1["state"] = "disabled"
            self.parkour_volume_y2_l["state"] = "disabled"
            self.parkour_volume_y2["state"] = "disabled"
            self.parkour_volume_z1_l["state"] = "disabled"
            self.parkour_volume_z1["state"] = "disabled"
            self.parkour_volume_z2_l["state"] = "disabled"
            self.parkour_volume_z2["state"] = "disabled"

        if self.variables["randomSeed"].get():
            self.seed["state"] = "disabled"
        else:
            self.seed["state"] = "normal"
        
        if self.variables["checkpointsEnabled"].get() is True:
            self.cp_period_l["state"] = "normal"
            self.cp_period["state"] = "normal"
        else:
            self.cp_period_l["state"] = "disabled"
            self.cp_period["state"] = "disabled"

        if self.variables["useAllBlocks"].get() is True:
            self.allowed_str_types_l["state"] = "disabled"
            self.t_one_block["state"] = "disabled"
            self.t_two_block["state"] = "disabled"
            self.t_four_block["state"] = "disabled"
            self.ascending["state"] = "disabled"
            self.descending["state"] = "disabled"
            self.difficulty_l["state"] = "disabled"
            self.difficulty["state"] = "disabled"
            self.pace_l["state"] = "disabled"
            self.pace["state"] = "disabled"
        else:
            self.allowed_str_types_l["state"] = "normal"
            self.t_one_block["state"] = "normal"
            self.t_two_block["state"] = "normal"
            self.t_four_block["state"] = "normal"
            self.ascending["state"] = "normal"
            self.descending["state"] = "normal"
            self.difficulty_l["state"] = "normal"
            self.difficulty["state"] = "normal"
            self.pace_l["state"] = "normal"
            self.pace["state"] = "normal"

        p_type = self.variables["parkourType"].get()
        if p_type == "Straight" or p_type == "Random":
            self.curves_size_l["state"] = "disabled"
            self.curves_size["state"] = "disabled"
            self.spiral_rotation_l["state"] = "disabled"
            self.spiral_rotation["state"] = "disabled"
            self.spiral_type_l["state"] = "disabled"
            self.spiral_type["state"] = "disabled"
            self.spiral_turnrate_l["state"] = "disabled"
            self.spiral_turnrate["state"] = "disabled"
            self.spiral_turn_prob_l["state"] = "disabled"
            self.spiral_turn_prob["state"] = "disabled"
        elif p_type == "Curves":
            self.curves_size_l["state"] = "normal"
            self.curves_size["state"] = "normal"
            self.spiral_rotation_l["state"] = "disabled"
            self.spiral_rotation["state"] = "disabled"
            self.spiral_type_l["state"] = "disabled"
            self.spiral_type["state"] = "disabled"
            self.spiral_turnrate_l["state"] = "disabled"
            self.spiral_turnrate["state"] = "disabled"
            self.spiral_turn_prob_l["state"] = "disabled"
            self.spiral_turn_prob["state"] = "disabled"
        elif p_type == "Spiral":
            self.curves_size_l["state"] = "disabled"
            self.curves_size["state"] = "disabled"
            self.spiral_rotation_l["state"] = "normal"
            self.spiral_rotation["state"] = "normal"
            self.spiral_type_l["state"] = "normal"
            self.spiral_type["state"] = "normal"
        
            sp_type = self.variables["spiralType"].get()
            if sp_type == "Even":
                self.spiral_turnrate_l["state"] = "normal"
                self.spiral_turnrate["state"] = "normal"
                self.spiral_turn_prob_l["state"] = "disabled"
                self.spiral_turn_prob["state"] = "disabled"
            else:
                self.spiral_turnrate_l["state"] = "disabled"
                self.spiral_turnrate["state"] = "disabled"
                self.spiral_turn_prob_l["state"] = "normal"
                self.spiral_turn_prob["state"] = "normal"


    
    def show_spiral_prob(self, string):
        string = ((float(string)*10)//1) / 10
        self.spiral_turn_prob_l["text"] = f"Spiral Turn Probability: {string}"
        
    def show_curves_size(self, string):
        string = ((float(string)*10)//1) / 10
        self.curves_size_l["text"] = f"Curves Size: {string}"

    def refresh_image(self):
        try:
            if self.settings["plotFileType"] == "png":
                self.img = Image.open("parkour_plot.png")
            else:
                self.img = Image.open("parkour_plot.jpg")
            self.img = self.img.resize(self.image_size)
            self.img = ImageTk.PhotoImage(self.img)
            self.img_label["image"] = self.img
            # Prevent GC
            self.img_label.image = self.img # type: ignore
        except:
            pass
    
    def refresh_plot(self, string: str = ""):

        if self.set_config() and len(self.list_of_placed_jumps) != 0:
            plotting.plot_parkour(list_of_placed_jumps=self.list_of_placed_jumps, 
                        parkour_volume=self.settings["parkourVolume"], 
                        enforce_parkour_volume=self.settings["enforceParkourVolume"], 
                        plot_command_blocks=self.settings["plotCommandBlocks"],
                        plot_color_scheme=self.settings["plotColorScheme"],
                        plot_file_type=self.settings["plotFileType"])
        
        self.refresh_image()
    
    def set_config(self) -> bool:

        v = self.variables
        for name, value in self.settings.items():

            if name == "parkourVolume":
                try:
                    self.settings[name] = [[
                                        int(v["parkourVolume_x1"].get()), 
                                        int(v["parkourVolume_x2"].get())
                                        ], 
                                        [
                                        int(v["parkourVolume_y1"].get()), 
                                        int(v["parkourVolume_y2"].get())
                                        ], 
                                        [
                                        int(v["parkourVolume_z1"].get()), 
                                        int(v["parkourVolume_z2"].get())
                                        ]]
                except:
                    messagebox.showerror("Settings Error", "parkourVolume: wrong input format. Only integers are allowed.")
                    return False

            elif name == "startPosition":
                try:
                    self.settings[name] = [int(v["startPosition_x"].get()), int(v["startPosition_y"].get()), int(v["startPosition_z"].get())]
                except:
                    messagebox.showerror("Settings Error", "startPosition: wrong input format. Only integers are allowed.")
                    return False

            elif name == "allowedStructureTypes":
                self.settings[name] = []
                if v["allowedStructureTypes_sb"].get():
                    self.settings[name].append("SingleBlock")
                if v["allowedStructureTypes_tb"].get():
                    self.settings[name].append("TwoBlock")
                if v["allowedStructureTypes_fb"].get():
                    self.settings[name].append("FourBlock")
            else:
                t = type(self.settings[name])
                if t is bool or t is str:
                    self.settings[name] = v[name].get()
                elif t is int:
                    try:
                        self.settings[name] = int(v[name].get())
                    except:
                        messagebox.showerror("Settings Error", f"{name}: wrong input format. Only integers are allowed.")
                        return False
                elif t is float:
                    try:
                        self.settings[name] = float(v[name].get())
                    except:
                        messagebox.showerror("Settings Error", f"{name}: wrong input format. Only floats are allowed.")
                        return False

        error_str = config.check_config(self.settings)
        if error_str != "":
            messagebox.showerror("Settings Error", error_str)
            return False
        else:
            return True
    
    def save_settings(self):
        if self.set_config():
            answer = messagebox.askyesno("Save Settings", "Save current parkour settings as default?")
            if answer is True:
                config.export_config(self.settings, gui_enabled=True)

    def reset_settings(self):
        answer = messagebox.askyesno("Reset Settings", "Reset to default settings?")
        if answer is True:
            self.settings = config.set_default_config()
            self.refresh_variables()

    def generate_parkour(self):

        self.generate_button["state"] = "disabled"

        if self.set_config():
            
            start_time = time.time()
            self.list_of_placed_jumps: list[JumpType] = []
            seed, nr_jumptypes_filtered, nr_total_jumptypes, self.list_of_placed_jumps = generator.generate_parkour(list_of_placed_jumps=self.list_of_placed_jumps, 
                                    random_seed=self.settings["randomSeed"], 
                                    seed=self.settings["seed"], 
                                    list_of_allowed_structure_types=self.settings["allowedStructureTypes"],
                                    parkour_start_position=self.settings["startPosition"],
                                    parkour_start_forward_direction=self.settings["startForwardDirection"],
                                    parkour_type=self.settings["parkourType"],
                                    spiral_rotation=self.settings["spiralRotation"],
                                    max_parkour_length=self.settings["maxParkourLength"],
                                    checkpoints_enabled=self.settings["checkpointsEnabled"],
                                    checkpoints_period=self.settings["checkpointsPeriod"],
                                    use_all_blocks=self.settings["useAllBlocks"],
                                    difficulty=self.settings["difficulty"],
                                    pace=self.settings["pace"],
                                    ascending=self.settings["parkourAscending"],
                                    descending=self.settings["parkourDescending"],
                                    curves_size=self.settings["curvesSize"],
                                    spiral_type=self.settings["spiralType"],
                                    spiral_turn_rate=self.settings["spiralTurnRate"],
                                    spiral_turn_prob=self.settings["spiralTurnProbability"],
                                    enforce_volume=self.settings["enforceParkourVolume"],
                                    parkour_volume=self.settings["parkourVolume"],
                                    gui_enabled=True,
                                    gui_loading_bar=self.loadingbar,
                                    gui_window=self.window,
                                    block_type=self.settings["blockType"])
            end_time = time.time()
            generation_time = round(end_time-start_time, 3)
            
            start_time = time.time()
            if self.settings["writeDatapackFiles"]:
                datapack.write_function_files(list_of_placed_jumps=self.list_of_placed_jumps, 
                                        parkour_volume=self.settings["parkourVolume"], 
                                        enforce_parkour_volume=self.settings["enforceParkourVolume"], 
                                        fill_volume_with_air=self.settings["fillParkourVolumeWithAir"],
                                        gui_enabled=True,
                                        minecraft_version=self.settings["mcVersion"])
            end_time = time.time()
            datapack_time = round(end_time-start_time, 3)

            start_time = time.time()
            plotting.plot_parkour(list_of_placed_jumps=self.list_of_placed_jumps, 
                        parkour_volume=self.settings["parkourVolume"], 
                        enforce_parkour_volume=self.settings["enforceParkourVolume"], 
                        plot_command_blocks=self.settings["plotCommandBlocks"],
                        plot_color_scheme=self.settings["plotColorScheme"],
                        plot_file_type=self.settings["plotFileType"])
            end_time = time.time()
            self.refresh_image()
            plot_time = round(end_time-start_time, 3)
            self.task_info_label["text"] = f"Generation: {generation_time}s    Datapack: {datapack_time}s    Plot: {plot_time}s"
            self.jumps_placed_l["text"] = f"JumpTypes used: {nr_jumptypes_filtered}/{nr_total_jumptypes}    Jumps placed: {len(self.list_of_placed_jumps)-3}/{self.settings["maxParkourLength"]}"

            self.variables["seed"].set(seed)
            # Update loading bar to 100%
            self.loadingbar["value"] = 100
            self.window.update_idletasks()

        self.generate_button["state"] = "normal"

    def run(self) -> None:
        self.window.mainloop()
