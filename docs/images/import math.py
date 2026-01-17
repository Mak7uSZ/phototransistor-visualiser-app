import math

points = []
center_x = 4
center_y = 0
radius = 4
num_points = 24

for i in range(num_points):
    theta = 2 * math.pi * i / num_points
    x = center_x + radius * math.cos(theta)
    y = center_y + radius * math.sin(theta)
    points.append((x, y))

for p in points:
    print(f"{p[0]:.3f}, {p[1]:.3f}")
