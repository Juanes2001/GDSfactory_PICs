import gdsfactory as gf
import numpy as np
import os

# ==================================================
# Parameters
# ==================================================
wg_width = 0.5
input_length = 100.0
split_length = 60.0
output_length = 100.0
output_separation = 10.0
layer = (1, 0)

gf.gpdk.PDK.activate()
# ==================================================
# Create component
# ==================================================
c = gf.Component("true_adiabatic_Y")

# ==================================================
# 1) Input straight
# ==================================================
xs = gf.cross_section.strip(width=wg_width)

wg_in = c << gf.components.straight(
    length=input_length,
    cross_section=xs
)

wg_in.move(origin=wg_in.center, destination=(0, 0))

x0 = wg_in.ports["o2"].center[0]

# ==================================================
# 2) Adiabatic Y region (single polygon body)
# ==================================================
npts = 200
x = np.linspace(0, split_length, npts)

# Quadratic smooth splitting profile
y_center = (output_separation / 2) * (x / split_length) ** 2

# Upper and lower boundaries
upper_outer = np.column_stack([x + x0, y_center + wg_width/2])
upper_inner = np.column_stack([x + x0, y_center - wg_width/2])
lower_outer = np.column_stack([x + x0, -y_center - wg_width/2])
lower_inner = np.column_stack([x + x0, -y_center + wg_width/2])

# Build full Y polygon
polygon_points = np.vstack([
    upper_outer,
    lower_outer[::-1],
    lower_inner,
    upper_inner[::-1]
])

c.add_polygon(polygon_points, layer=layer)

# ==================================================
# 3) Output straights
# ==================================================
x_end = x0 + split_length
y_end = output_separation / 2

# Upper output
wg_up = c << gf.components.straight(
    length=output_length,
    cross_section=xs
)
wg_up.move((x_end, y_end - wg_width/2))

# Lower output
wg_down = c << gf.components.straight(
    length=output_length,
    cross_section=xs
)
wg_down.move((x_end, -y_end - wg_width/2))

# ==================================================
# Center entire structure
# ==================================================
c.move(origin=c.center, destination=(0, 0))

# ==================================================
# Export GDS
# ==================================================
filepath = c.write_gds("true_adiabatic_Y.gds")
c.show()
print("Saved at:", os.path.abspath(filepath))