

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    root = tkinter.Tk()
    root.title('Robot Twister')
    controller = ttk.Frame()
    controller.grid()

    part = ttk.Label(root, text="R-MOTOR, L-MOTOR, ")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    root.mainloop()


main()
