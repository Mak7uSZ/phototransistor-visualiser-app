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
           # ser.write(b'R')
           # data = ser.readline().decode('utf-8').strip()
           # if data:
                values = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1, 1,1,1,1,
                          1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1, 1,1,1,1, 1, 1, 1, 1, 1, 1, 1 , 1,        ]


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
                global colors, coordinates
                active_sensors = []
                for i in range(len(colors)):
                    if colors[i] == activeColor:
                        active_sensors.append(i)

                # Remove previous arrows (optional: store them globally)
                if 'arrows_list' not in globals():
                    global arrows_list
                    arrows_list = []
                for arr in arrows_list:
                    arr.remove()
                arrows_list.clear()
                active_sensors = []
            
                for i in range(len(colors)):
                    if colors[i] == activeColor:
                       active_sensors[i] = i

                for active in active_sensors:
                    print(f"Sensor {active} is active.")
                    if (active >= 28 and active <= 31 ) or (active >= 32 and active <= 35) or (active >= 24 and active <= 27) or (active >= 36 and active <= 39):
                        print("Distance sensor activated!")
                        x, y = coordinates[active][1]
                        vec = np.array([x, y])
                        if np.linalg.norm(vec) != 0:
                            vec = -vec / np.linalg.norm(vec) * 1.0  # arrow length = 1.0

                        arrow = ax.arrow(x, y, vec[0], vec[1], head_width=0.3, head_length=0.5, fc='green', ec='green')
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
