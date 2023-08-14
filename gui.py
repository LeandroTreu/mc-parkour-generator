import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()

frame_1 = tk.Frame(master=window, relief="flat", borderwidth=5, bg="grey")
frame_1.pack(fill=tk.BOTH, expand=True)

label = tk.Label(
    master=frame_1,
    text="Hello, Tkinter",
    fg="white",
    bg="grey",
    width=10,
    height=5
)


button = tk.Button(
    master=frame_1,
    text="Click me!",
    width=25,
    height=5,
    bg="black",
    fg="green",
)

entry = tk.Entry(master=frame_1, fg="black", bg="white", width=10)







label.pack()
button.pack()
entry.pack()

window.mainloop()