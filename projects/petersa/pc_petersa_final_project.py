

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    root = tkinter.Tk()
    root.title('Robot Twister')
    controller = ttk.Frame()
    controller.grid()

    part = ttk.Label(root, text="R-MOTOR, L-MOTOR, ARM")
    part.grid(row=0, column=0)
    part_entry = ttk.Entry(root, width=10)
    part_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    root.mainloop()


main()
