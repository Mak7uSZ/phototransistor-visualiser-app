import json
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math

 #Custom colors for categories
activeColor = 'red'
inactiveColor = 'blue'
disabledColor = 'yellow'

# Load sensor coordinates and label from a JSON file
def load_coordinates_from_file():
    global label
    coordinates = []
    try:
        with open('src/coordinates.json', 'r') as file:
            data = json.load(file)
            for item in data:
                label = item["label"]
                coord = item["coordinates"]
                coordinates.append((label, tuple(coord)))
        return coordinates
    except Exception as e:
        print(f"Error loading coordinates: {e}")

coordinates = load_coordinates_from_file()
NUM_SENSORS = len(coordinates) 

# Get all current ports used by the system for serial communication
# available_ports = [port.device for port in serial.tools.list_ports.comports()]

def start_graph():
   # selected_port = port_var.get()
   # try:
   #     ser = serial.Serial(selected_port, 115200, timeout=1)
  #  except Exception as e:
   #     messagebox.showerror("Serial Port Error", f"Could not open {selected_port}:\n{e}")
   #     return

    # Create a figure and size for the axis for the plot
    xSize = 16
    ySize = 16
    fig, ax = plt.subplots(figsize=(xSize, ySize))
    scatter = ax.scatter(
        [coord[0] for _, coord in coordinates],
        [coord[1] for _, coord in coordinates],
    s=100
    )
    
    # Create a label for each sensor based on the coordinates
    # You can customize the label position and other elements as needed
    for label, (x, y) in coordinates:
        ax.text(x, y + 0.3, str(label), ha='center', fontsize=8)


    ax.set_title(
        f"Sensor Visualisation\n"
        f"activeColor = {activeColor} | "
        f"inactiveColor = {inactiveColor} | "
        f"disabledColor = {disabledColor}"
    )
    ax.grid(True)
    ax.set_aspect('equal')

    arrows = []  # List to store drawn arrows so we can remove them each frame

    def update(frame):
        global colors
        try:
                # EERSTE 40 INPUT
                # LAATSTE 40 THRESHOLDS

                #ACTIVE IF INPUT > THRESHOLD
                #    
                          #0  1  2  3  4  5  6  7  8  9  10 11 12 13  14  15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
                values = [ 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0,  0, 0,  0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0]


                                    

                if len(values) != NUM_SENSORS * 2:
                    print("Invalid data length, amount of values read over serial: ", values)
                    print("Expected length from coordinates.json + thresholds: ", NUM_SENSORS * 2)
                    return scatter,
            
                sensors = values[:NUM_SENSORS]
                thresholds = values[NUM_SENSORS:NUM_SENSORS*2]

                colors = []
                for i in range(NUM_SENSORS):
                    if thresholds[i] == -1:
                        colors.append(disabledColor)
                    elif sensors[i] > thresholds[i]:
                        colors.append(activeColor)
                    else:
                        colors.append(inactiveColor)
                scatter.set_color(colors)   

                arrows_drawing(ax)      
                
                # Remove old arrows
                for arr in arrows:
                    arr.remove()
                arrows.clear()

        except Exception as e:
            print(f"Error: {e}")
        return scatter,


    # customize animation with ani variable
    ani = FuncAnimation(fig, update, interval=200, blit=False)
    plt.tight_layout()
    plt.show()
   # ser.close()

def arrows_drawing(ax):
    global arrows_list

    if 'arrows_list' in globals():
        for a in arrows_list:
            a.remove()
        arrows_list.clear()
    else:
        arrows_list = []

    active_positions = [
        (x, y)
        for i, (label, (x, y)) in enumerate(coordinates)
        if colors[i] == activeColor
    ]

    if not active_positions:
        return

    xs = [p[0] for p in active_positions]
    ys = [p[1] for p in active_positions]

    centroid_x = sum(xs) / len(xs)
    centroid_y = sum(ys) / len(ys)

    left_group = []
    right_group = []

    for x, y in active_positions:
        if x > centroid_x:
            right_group.append((x, y))
        else:
            left_group.append((x, y))

    if not left_group or not right_group:
        dx = centroid_x
        dy = centroid_y
    else:
        lx = sum(x for x, y in left_group) / len(left_group)
        ly = sum(y for x, y in left_group) / len(left_group)
        rx = sum(x for x, y in right_group) / len(right_group)
        ry = sum(y for x, y in right_group) / len(right_group)

        dx = lx - rx
        dy = ly - ry


    angle = 90.0

    angle_rad = math.atan2(dy, dx)
    angle = angle_rad * 180.0 / math.pi


    if(angle < 0):
        angle += 360.0

   
    if(angle > 180.0):
        angle -= 180.0

    yBall = 50
    xBall = 20

    arrowhead_color = str("red")
    arrow_color = str("red")

    if((angle <= 20 and angle >= 0) or (angle <= 180 and angle >= 160)):
        dx = xBall
        arrowhead_color = str("red")
        arrow_color = str("yellow")

    elif((angle <= 120 and angle >= 70) or (angle <= 65 and angle >= 46) and yBall > 0):
    #robot is precies op de lijn
        dx = 0
        dy = 100
        arrowhead_color = str("green")
        arrow_color = str("yellow")
        

    elif (angle <= 18 and angle >= 49 and yBall < 0 and xBall > 0):
        dx = -25
        dy = -50
        arrowhead_color = str("orange")
        arrow_color = str("yellow")

    elif (angle <= 45 and angle >= 20 and yBall > 0):
        dy = 120
        arrowhead_color = str("yellow")
        arrow_color = str("yellow")

    elif (angle <= 160 and angle >= 135):
        dx = -100
    else:
        dx = 0



    yBorder = 1.5; 

    for i in range(23):
        if((angle <= 20 and angle >= 0) or (angle <= 180 and angle >= 160)):
            if(colors[i] == activeColor and coordinates[i][1][1] > yBorder):
                dy = 100
                arrowhead_color = str("purple")
                arrow_color = str("purple")
                break
            elif(colors[i] == activeColor and coordinates[i][1][1] < -yBorder):
                dy = -100
                arrowhead_color = str("brown")
                arrow_color = str("brown")
                break
            else:
                dy = 0

    length = np.hypot(dx, dy)
    if length == 0:
        return

    dx = dx / length * 3.0
    dy = dy / length * 3.0

    arrow = ax.arrow(
        0, 0,
        dx, dy,
        head_width=0.6,
        head_length=0.8,
        fc= arrowhead_color,
        ec= arrow_color
    )

    arrows_list.append(arrow)





# Dropdown menu for selecting COM port
root = tk.Tk()
root.title("Sensor COM Port Selector")

tk.Label(root, text="Select COM Port:").pack(pady=5)

port_var = tk.StringVar()
port_dropdown = ttk.Combobox(root, textvariable=port_var)
port_dropdown['values'] = [1,2,3,4,5]  # Example COM ports for demonstration

# Select the first available port by default if any are found
#if available_ports:
#    port_dropdown.current(0)  
#else:
  #  port_dropdown.set('No COM ports found')

port_dropdown.current(0)  
port_dropdown.pack(pady=5)

# Button to start the graph
tk.Button(root, text="Start Graph", command=start_graph).pack(pady=10)

root.mainloop()
