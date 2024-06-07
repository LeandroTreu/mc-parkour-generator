# type: ignore
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import config
import time
import main

class Gui():

    image_size = (1000, 1000)

    def __init__(self, settings: dict[any]) -> None:

        self.settings = settings

        self.window = tk.Tk()
        self.window.title("MC Parkour Generator")
        self.create_menu()

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
        self.settings_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

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
        file = tk.Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label='File', menu=file) 
        file.add_command(label='New File', command=None) 
        file.add_command(label='Open...', command=None) 
        file.add_command(label='Save', command=None) 
        file.add_separator() 
        file.add_command(label='Exit', command=self.window.destroy) 
        self.window.config(menu=menubar) 

    def populate_settings_frame(self):

        # Settings
        self.settings_label = ttk.Label(master=self.settings_frame, text="Settings")
        self.enforce_cb = ttk.Checkbutton(master=self.settings_frame, text="Enforce Parkour Volume", variable=self.variables["enforceParkourVolume"], onvalue=True, offvalue=False, command=self.cb_toggle)
        self.fill_air_cb = ttk.Checkbutton(master=self.settings_frame, text="Fill Volume with Air", variable=self.variables["fillParkourVolumeWithAir"], onvalue=True, offvalue=False, state="disabled")

        self.parkour_volume_label = ttk.Label(master=self.settings_frame, text="Parkour Volume:", state="disabled")
        self.parkour_volume = ttk.Entry(master=self.settings_frame, textvariable=self.variables["parkourVolume"], state="disabled")

        self.parkour_length_label = ttk.Label(master=self.settings_frame, text="Max Parkour Length:")
        self.parkour_length = ttk.Spinbox(master=self.settings_frame, textvariable=self.variables["maxParkourLength"], from_=0, to=1000)

        self.start_position_label = ttk.Label(master=self.settings_frame, text="Start Coordinates:")
        self.start_position = ttk.Entry(master=self.settings_frame, textvariable=self.variables["startPosition"])

        self.settings_label.grid(row=0, column=0, sticky="W", padx=0, pady=0)
        self.enforce_cb.grid(row=1, column=0, sticky="W", padx=0, pady=0)
        self.fill_air_cb.grid(row=1, column=1, sticky="W", padx=0, pady=0)
        self.parkour_volume_label.grid(row=2, column=1, sticky="W", padx=0, pady=0)
        self.parkour_volume.grid(row=3, column=1, sticky="W", padx=0, pady=0)
        self.parkour_length_label.grid(row=2, column=0, sticky="W", padx=0, pady=0)
        self.parkour_length.grid(row=3, column=0, sticky="W", padx=0, pady=0)
        self.start_position_label.grid(row=5, column=0, sticky="W", padx=0, pady=0)
        self.start_position.grid(row=6, column=0, sticky="W", padx=0, pady=0)


        # Generate Button
        self.generate_button = ttk.Button(master=self.settings_frame, text="Generate Parkour", padding=10, command=self.generate_parkour)
        self.generate_button.grid(row=100, column=0, sticky="S", padx=10, pady=10)

        # Loading Bar
        self.loadingbar = ttk.Progressbar(master=self.settings_frame, value=0, length=200)
        self.loadingbar.grid(row=101, column=0, sticky="N", padx=10, pady=10)
    
    def cb_toggle(self):
        if self.variables["enforceParkourVolume"].get() is True:
            self.fill_air_cb["state"] = "normal"
            self.parkour_volume_label["state"] = "normal"
            self.parkour_volume["state"] = "normal"
        else:
            self.fill_air_cb["state"] = "disabled"
            self.parkour_volume_label["state"] = "disabled"
            self.parkour_volume["state"] = "disabled"
    
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