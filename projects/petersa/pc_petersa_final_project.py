

import tkinter
from tkinter import ttk
import math

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def things_to_draw(self, sides, fill_color, outline_color):
        print('Robot has completed his masterpiece')
        print('Robot has drawn shape with', sides, 'sides', fill_color,
              'fill color', outline_color, 'outline color')
        root = tkinter.Toplevel()
        root.title = "Robots Masterpiece"

        canvas = tkinter.Canvas(root, background="lightgray", width=800,
                                height=500)
        canvas.grid(columnspan=2)
        if sides == 0:
            canvas.create_oval(50, 50, 150, 150, fill=fill_color,
                               outline=outline_color)
        else:
            print('made it to polygon')
            polygon_sides = polygon(sides)
            print(polygon_sides)
            canvas.create_polygon(polygon_sides, fill=fill_color,
                                  outline=outline_color)


def main():
    pc_delegate = MyDelegateOnThePc()
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Robot Artist')
    controller = ttk.Frame(root, padding=50)
    controller.grid()

    combo_shapes_readings = tkinter.StringVar()
    shapes = ttk.Combobox(controller, textvariable=combo_shapes_readings)
    shapes['values'] = ('Square', 'Circle', 'Triangle', 'Other')
    shapes.grid(row=0, column=0)

    combo_colorf_reading = tkinter.StringVar()
    color_fill = ttk.Combobox(controller, textvariable=combo_colorf_reading)
    color_fill['values'] = ('Red', 'Blue', 'Yellow', 'Green', 'Black', 'None')
    color_fill.grid(row=0, column=1)

    combo_coloro_reading = tkinter.StringVar()
    color_outline = ttk.Combobox(controller,
                                 textvariable=combo_coloro_reading)
    color_outline['values'] = ('Red', 'Blue', 'Yellow', 'Green', 'Black',
                               'None')
    color_outline.grid(row=0, column=2)
    color_outline.get()

    enter = ttk.Button(controller, text='Enter')
    enter.grid(row=1, column=2)

    enter['command'] = (lambda: entered(shapes.get(), color_fill.get(),
                                        color_outline.get(),
                                        controller, mqtt_client))
    root.mainloop()


def entered(shapes_input, color_fill, color_outline, frame, mqtt_client):
    if shapes_input == 'Other':
        other_shape = ttk.Entry(frame)
        other_shape.grid(row=2, column=0)
        other_shape_button = ttk.Button(frame, text='Enter Sides')
        other_shape_button.grid(row=2, column=1)

        other_shape_button['command'] = lambda: to_the_robot(
            int(other_shape.get()), color_fill, color_outline, mqtt_client)
    elif shapes_input == 'Circle':
        circle_sides = 0
        to_the_robot(circle_sides, color_fill, color_outline, mqtt_client)
    elif shapes_input == 'Square':
        square_sides = 4
        to_the_robot(square_sides, color_fill, color_outline, mqtt_client)
    else:
        triangle_sides = 3
        to_the_robot(triangle_sides, color_fill, color_outline, mqtt_client)


def to_the_robot(sides, fill_color, outline_color, mqtt_client):
    print(sides, fill_color, outline_color)

    mqtt_client.send_message('drive_shapes', [sides, fill_color,
                                              outline_color])


def polygon(sides, radius=50, rotation=0, translation=None):
    one_segment = math.pi * 2 / sides

    points = [
        (math.sin(one_segment * i + rotation) * radius + 250,
         math.cos(one_segment * i + rotation) * radius + 150)
        for i in range(sides)]

    if translation:
        points = [[sum(pair) for pair in zip(point, translation)]
                  for point in points]

    return points


main()
