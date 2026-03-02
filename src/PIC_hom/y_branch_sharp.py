import gdsfactory as gf
import numpy as np

# ==============================
# Parameters
# ==============================
wg_width = 0.5       # µm
wg_length = 100.0    # µm
branch_angle = 20    # degrees

gf.gpdk.PDK.activate()

# ==============================
# Define strip cross section
# ==============================
xs = gf.cross_section.strip(width=wg_width)

# ==============================
# Create component
# ==============================
c = gf.Component("sharp_Y_branch")

# ---- Input waveguide ----
wg_in = c << gf.components.straight(
    length=wg_length,
    cross_section=xs
)

# Move so input is centered
wg_in.move(origin=wg_in.center, destination=(0, 0))

# ---- Upper branch ----
upper = c << gf.components.straight(
    length=wg_length,
    cross_section=xs
)

upper.connect("o1", wg_in.ports["o2"])
upper.rotate(branch_angle, center=upper.ports["o1"].center)

# ---- Lower branch ----
lower = c << gf.components.straight(
    length=wg_length,
    cross_section=xs
)

lower.connect("o1", wg_in.ports["o2"])
lower.rotate(-branch_angle, center=lower.ports["o1"].center)

# ==============================
# Center entire structure
# ==============================
c.move(origin=c.center, destination=(0, 0))

# ==============================
# Export GDS
# ==============================
c.write_gds("sharp_Y_branch.gds")
c.show()
print("Sharp Y-branch GDS exported successfully.")