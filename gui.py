# type: ignore
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import config
import time
import main
from tkinter import font

class Gui():

    image_size = (1000, 1000)
    font_title = ("Segoe UI", 11, "bold")
    font_general = ("Segoe UI", 10, "normal")

    def __init__(self, settings: dict[any]) -> None:

        self.settings = settings

        self.window = tk.Tk()
        self.window.title("MC Parkour Generator")
        self.create_menu()

        default_font = font.nametofont("TkDefaultFont")
        text_font = font.nametofont("TkTextFont")
        fixed_font = font.nametofont("TkFixedFont")
        # print(default_font.actual())
        # print(text_font.actual())
        # print(fixed_font.actual())
        default_font.configure(family=self.font_general[0], size=self.font_general[1], weight=self.font_general[2])
        text_font.configure(family=self.font_general[0], size=self.font_general[1], weight=self.font_general[2])
        fixed_font.configure(family=self.font_general[0], size=self.font_general[1], weight=self.font_general[2])

        # Map settings to tkinter Variables
        self.variables = {}
        for (name, value) in self.settings.items():
            if type(value) is bool:
                self.variables[name] = tk.BooleanVar(master=self.window, value=self.settings[name])
            elif type(value) is str:
                self.variables[name] = tk.StringVar(master=self.window, value=self.settings[name])
            elif type(value) is int:
                self.variables[name] = tk.IntVar(master=self.window, value=self.settings[name])
            elif type(value) is float:
                self.variables[name] = tk.DoubleVar(master=self.window, value=self.settings[name])
            else:
                self.variables[name] = tk.StringVar(master=self.window, value=str(self.settings[name]))


        self.settings_frame = ttk.Frame(master=self.window, relief="flat", borderwidth=5)
        self.settings_frame.pack(expand=False, side=tk.LEFT)

        # Image frame and label
        self.image_frame = ttk.Frame(master=self.window, relief="flat", borderwidth=5)
        self.image_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        self.img = Image.open("parkour_plot.png")
        self.img = self.img.resize(self.image_size)
        self.img = ImageTk.PhotoImage(self.img)
        self.img_label = tk.Label(self.image_frame, image=self.img)
        self.img_label.pack(expand=True, fill=tk.BOTH)

        self.populate_settings_frame()

    def create_menu(self):

        menubar = tk.Menu(self.window)
        settings_menu = tk.Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label="Settings", menu=settings_menu) 
        settings_menu.add_command(label="Save", command=None) 
        settings_menu.add_separator() 
        settings_menu.add_command(label="Exit", command=self.window.destroy) 
        self.window.config(menu=menubar) 

    def populate_settings_frame(self):

        # Settings
        self.enforce_cb = ttk.Checkbutton(master=self.settings_frame, text="Enforce Parkour Volume", variable=self.variables["enforceParkourVolume"], onvalue=True, offvalue=False, command=self.cb_toggle)
        self.fill_air_cb = ttk.Checkbutton(master=self.settings_frame, text="Fill Volume with Air", variable=self.variables["fillParkourVolumeWithAir"], onvalue=True, offvalue=False, state="disabled")

        self.parkour_volume_label = ttk.Label(master=self.settings_frame, text="Parkour Volume:", state="disabled")
        self.parkour_volume = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume"], state="disabled")

        self.parkour_length_label = ttk.Label(master=self.settings_frame, text="Max Parkour Length:")
        self.parkour_length = ttk.Entry(master=self.settings_frame, textvariable=self.variables["maxParkourLength"], width=10, justify="right")

        self.start_position_label = ttk.Label(master=self.settings_frame, text="Start Coordinates:")
        self.start_position = ttk.Entry(master=self.settings_frame, textvariable=self.variables["startPosition"])

        self.start_forward_dir_l = ttk.Label(master=self.settings_frame, text="Start Forward Direction:")
        self.start_forward_dir = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["startForwardDirection"], values=["Xpos", "Xneg", "Zpos", "Zneg"], width=7)

        self.block_type_l = ttk.Label(master=self.settings_frame, text="Parkour Block Type:")
        self.block_type = ttk.Entry(master=self.settings_frame, textvariable=self.variables["blockType"])

        self.random_seed = ttk.Checkbutton(master=self.settings_frame, text="Random Seed", variable=self.variables["randomSeed"], onvalue=True, offvalue=False, command=None)
        self.seed = ttk.Entry(master=self.settings_frame, textvariable=self.variables["seed"], justify="right")

        self.cp_enabled = ttk.Checkbutton(master=self.settings_frame, text="Checkpoints", variable=self.variables["checkpointsEnabled"], onvalue=True, offvalue=False, command=None)
        self.cp_period_l = ttk.Label(master=self.settings_frame, text="Checkpoints Period:")
        self.cp_period = ttk.Entry(master=self.settings_frame, textvariable=self.variables["checkpointsPeriod"], justify="right", width=10)

        self.use_all_blocks = ttk.Checkbutton(master=self.settings_frame, text="Use all JumpTypes", variable=self.variables["useAllBlocks"], onvalue=True, offvalue=False, command=None)
        self.allowed_str_types_l = ttk.Label(master=self.settings_frame, text="Allowed JumpTypes:")
        self.t_one_block = ttk.Checkbutton(master=self.settings_frame, text="OneBlock", variable=self.variables["useAllBlocks"], onvalue=True, offvalue=False, command=None)
        self.t_two_block = ttk.Checkbutton(master=self.settings_frame, text="TwoBlock", variable=self.variables["useAllBlocks"], onvalue=True, offvalue=False, command=None)

        self.difficulty_l = ttk.Label(master=self.settings_frame, text=f"Difficulty: {self.variables["difficulty"].get()}")
        self.difficulty = ttk.Scale(master=self.settings_frame, variable=self.variables["difficulty"], from_=0, to=1.0, command=self.show_difficulty)
        self.flow_l = ttk.Label(master=self.settings_frame, text=f"Flow: {self.variables["flow"].get()}")
        self.flow = ttk.Scale(master=self.settings_frame, variable=self.variables["flow"], from_=0, to=1.0, command=self.show_flow)

        self.parkour_type_l = ttk.Label(master=self.settings_frame, text="Parkour Type:")
        self.parkour_type = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["parkourType"], values=["Straight", "Random", "Curves", "Spiral"], width=10)
        self.ascending = ttk.Checkbutton(master=self.settings_frame, text="Parkour Ascending", variable=self.variables["parkourAscending"], onvalue=True, offvalue=False, command=None)

        self.curves_size_l = ttk.Label(master=self.settings_frame, text="Curves Size:")
        self.curves_size = ttk.Entry(master=self.settings_frame, textvariable=self.variables["straightCurvesSize"], width=10, justify="right")

        self.spiral_rotation_l = ttk.Label(master=self.settings_frame, text="Spiral Rotation:")
        self.spiral_rotation = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["spiralRotation"], values=["counterclockwise", "clockwise"], width=15)
        self.spiral_type_l = ttk.Label(master=self.settings_frame, text="Spiral Type:")
        self.spiral_type = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["spiralType"], values=["Even", "Random"], width=10)
        self.spiral_turnrate_l = ttk.Label(master=self.settings_frame, text="Spiral Turn Rate:")
        self.spiral_turnrate = ttk.Entry(master=self.settings_frame, textvariable=self.variables["spiralTurnRate"], width=10, justify="right")
        self.spiral_turn_prob_l = ttk.Label(master=self.settings_frame, text=f"Spiral Turn Probability: {self.variables["spiralTurnProbability"].get()}")
        self.spiral_turn_prob = ttk.Scale(master=self.settings_frame, variable=self.variables["spiralTurnProbability"], from_=0, to=1.0, command=self.show_spiral_prob)

        # File options
        self.plot_file_type_l = ttk.Label(master=self.settings_frame, text="Plot File Type")
        self.plot_file_type = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["plotFileType"], values=["png", "jpg"], width=7)
        self.plot_colorscheme_l = ttk.Label(master=self.settings_frame, text="Plot Colorscheme")
        self.plot_colorscheme = ttk.Combobox(master=self.settings_frame, textvariable=self.variables["plotColorScheme"], values=["winter", "viridis", "plasma", "grey", "hot", "summer", "hsv", "copper"], width=10)
        self.plot_commandblocks = ttk.Checkbutton(master=self.settings_frame, text="Plot Commandblocks", variable=self.variables["plotCommandBlocks"], onvalue=True, offvalue=False, command=None)
        self.write_datapack_files = ttk.Checkbutton(master=self.settings_frame, text="Write Datapack Files", variable=self.variables["writeDatapackFiles"], onvalue=True, offvalue=False, command=None)


        self.settings_label = ttk.Label(master=self.settings_frame, text="Parkour Settings", font=self.font_title)
        self.settings_label.grid(row=101, column=100, sticky="W", padx=0, pady=0)

        self.enforce_cb.grid(row=110, column=100, sticky="W", padx=0, pady=0)
        self.fill_air_cb.grid(row=110, column=101, sticky="W", padx=0, pady=0)
        self.parkour_volume_label.grid(row=120, column=101, sticky="W", padx=0, pady=0)
        self.parkour_volume.grid(row=120, column=102, sticky="W", padx=0, pady=0)
        self.parkour_length_label.grid(row=140, column=100, sticky="W", padx=0, pady=0)
        self.parkour_length.grid(row=140, column=101, sticky="W", padx=0, pady=0)
        self.start_position_label.grid(row=160, column=100, sticky="W", padx=0, pady=0)
        self.start_position.grid(row=160, column=101, sticky="W", padx=0, pady=0)
        self.start_forward_dir_l.grid(row=180, column=100, sticky="W", padx=0, pady=0)
        self.start_forward_dir.grid(row=180, column=101, sticky="W", padx=0, pady=0)
        self.block_type_l.grid(row=200, column=100, sticky="W", padx=0, pady=0)
        self.block_type.grid(row=200, column=101, sticky="W", padx=0, pady=0)
        self.random_seed.grid(row=220, column=100, sticky="W", padx=0, pady=0)
        # self.seed_label = ttk.Label(master=self.settings_frame, text="Seed:")
        # self.seed_label.grid(row=220, column=101, sticky="W", padx=0, pady=0)
        self.seed.grid(row=220, column=101, sticky="W", padx=0, pady=0)

        self.separator_cp = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_cp.grid(row=250, columns=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.cp_label = ttk.Label(master=self.settings_frame, text="Checkpoints", font=self.font_title)
        self.cp_label.grid(row=251, column=100, sticky="W", padx=0, pady=0)
        self.cp_enabled.grid(row=260, column=100, sticky="W", padx=0, pady=0)
        self.cp_period_l.grid(row=260, column=101, sticky="W", padx=0, pady=0)
        self.cp_period.grid(row=260, column=102, sticky="W", padx=0, pady=0)

        self.separator_str = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_str.grid(row=300, columns=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.jt_label = ttk.Label(master=self.settings_frame, text="Jump Types", font=self.font_title)
        self.jt_label.grid(row=301, column=100, sticky="W", padx=0, pady=0)
        self.use_all_blocks.grid(row=310, column=100, sticky="W", padx=0, pady=0)
        self.allowed_str_types_l.grid(row=310, column=101, sticky="W", padx=0, pady=0)
        self.t_one_block.grid(row=310, column=102, sticky="W", padx=0, pady=0)
        self.t_two_block.grid(row=311, column=102, sticky="W", padx=0, pady=0)

        self.separator_df = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_df.grid(row=400, column=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.d_and_f_label = ttk.Label(master=self.settings_frame, text="Difficulty and Flow", font=self.font_title)
        self.d_and_f_label.grid(row=401, column=100, sticky="W", padx=0, pady=0)
        self.difficulty_l.grid(row=410, column=100, sticky="W", padx=0, pady=0)
        self.difficulty.grid(row=411, column=100, sticky="W", padx=0, pady=0)
        self.flow_l.grid(row=410, column=101, sticky="W", padx=0, pady=0)
        self.flow.grid(row=411, column=101, sticky="W", padx=0, pady=0)

        self.separator_pktypes = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_pktypes.grid(row=500, column=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.pt_label = ttk.Label(master=self.settings_frame, text="Parkour Type", font=self.font_title)
        self.pt_label.grid(row=501, column=100, sticky="W", padx=0, pady=0)
        self.ascending.grid(row=502, column=100, sticky="W", padx=0, pady=0)
        self.parkour_type_l.grid(row=510, column=100, sticky="W", padx=0, pady=0)
        self.parkour_type.grid(row=510, column=101, sticky="W", padx=0, pady=0)
        self.curves_size_l.grid(row=540, column=101, sticky="W", padx=0, pady=0)
        self.curves_size.grid(row=540, column=102, sticky="W", padx=0, pady=0)
        self.spiral_rotation_l.grid(row=550, column=101, sticky="W", padx=0, pady=0)
        self.spiral_rotation.grid(row=550, column=102, sticky="W", padx=0, pady=0)
        self.spiral_type_l.grid(row=560, column=101, sticky="W", padx=0, pady=0)
        self.spiral_type.grid(row=560, column=102, sticky="W", padx=0, pady=0)
        self.spiral_turnrate_l.grid(row=570, column=101, sticky="W", padx=0, pady=0)
        self.spiral_turnrate.grid(row=570, column=102, sticky="W", padx=0, pady=0)
        self.spiral_turn_prob_l.grid(row=580, column=101, sticky="W", padx=0, pady=0)
        self.spiral_turn_prob.grid(row=580, column=102, sticky="W", padx=0, pady=0)

        # File options
        self.separator_file_options = ttk.Separator(master=self.settings_frame, orient="horizontal")
        self.separator_file_options.grid(row=600, column=100, columnspan=1000, sticky="EW", padx=0, pady=10, ipadx=0, ipady=0)
        self.file_options_label = ttk.Label(master=self.settings_frame, text="File Settings", font=self.font_title)
        self.file_options_label.grid(row=601, column=100, sticky="W", padx=0, pady=0)
        self.write_datapack_files.grid(row=602, column=100, sticky="W", padx=0, pady=0)
        self.plot_commandblocks.grid(row=602, column=101, sticky="W", padx=0, pady=0)
        self.plot_file_type_l.grid(row=610, column=100, sticky="W", padx=0, pady=0)
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
        self.loadingbar.pack(fill=tk.BOTH, expand=True, side=tk.TOP, padx=5, pady=5)

        # Task Info
        self.task_info_label = ttk.Label(master=self.generate_frame, text="Task Info")
        self.task_info_label.pack(side=tk.TOP, padx=5, pady=5)
    
    def cb_toggle(self):
        if self.variables["enforceParkourVolume"].get() is True:
            self.fill_air_cb["state"] = "normal"
            self.parkour_volume_label["state"] = "normal"
            self.parkour_volume["state"] = "normal"
        else:
            self.fill_air_cb["state"] = "disabled"
            self.parkour_volume_label["state"] = "disabled"
            self.parkour_volume["state"] = "disabled"
    
    def show_difficulty(self, string):
        string = round(float(string), 1)
        self.difficulty_l["text"] = f"Difficulty: {string}"

    def show_flow(self, string):
        string = round(float(string), 1)
        self.flow_l["text"] = f"Flow: {string}"

    def show_spiral_prob(self, string):
        string = round(float(string), 1)
        self.spiral_turn_prob_l["text"] = f"Spiral Turn Probability: {string}"
        
    def refresh_image(self):
        self.img = Image.open("parkour_plot.png")
        self.img = self.img.resize(self.image_size)
        self.img = ImageTk.PhotoImage(self.img)
        self.img_label["image"] = self.img
        # Prevent GC
        self.img_label.image = self.img

    def generate_parkour(self):

        main.generate_parkour(self.settings, True, self.loadingbar, self.window)
        self.refresh_image()
        # Update loading bar to 100%
        self.loadingbar["value"] = 100
        self.window.update_idletasks()

    def run(self) -> None:
        self.window.mainloop()


if __name__ == "__main__":

    settings = config.import_config()
    use_gui = True

    if use_gui:
        gui = Gui(settings)
        gui.run()
    else:
        main.generate_parkour(settings, False, None, None)