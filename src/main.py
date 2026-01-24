import json
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

 #Custom colors for categories
activeColor = 'red'
inactiveColor = 'blue'
disabledColor = 'yellow'

# Load sensor coordinates and label from a JSON file
def load_coordinates_from_file():
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
                values = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,  0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0]
                                                                                                        

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
    global colors, arrows_list

    # очистка старых стрелок
    if 'arrows_list' in globals():
        for a in arrows_list:
            a.remove()
        arrows_list.clear()
    else:
        arrows_list = []

    active = {i for i, c in enumerate(colors) if c == activeColor}

    FRONT = set(range(32, 36))   # вверх → стрелка вниз
    BACK  = set(range(36, 40))   # вниз → стрелка вверх
    LEFT  = set(range(28, 32))   # влево → стрелка вправо
    RIGHT = set(range(24, 28))   # вправо → стрелка влево

    dx, dy = 0, 0

    if active & FRONT:
        dy -= 1
    if active & BACK:
        dy += 1
    if active & LEFT:
        dx += 1
    if active & RIGHT:
        dx -= 1

    # если направления нет
    if dx == 0 and dy == 0:
        return

    vec = np.array([dx, dy], dtype=float)
    vec = vec / np.linalg.norm(vec) * 3.0  # длина стрелки

    arrow = ax.arrow(
        0, 0,
        vec[0], vec[1],
        head_width=0.6,
        head_length=0.8,
        fc='red',
        ec='red'
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
