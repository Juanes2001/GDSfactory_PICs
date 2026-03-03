import gdsfactory as gf

# =====================================
# Parameters
# =====================================
wg_width = 0.39
wg_length = 100.0
taper_length = 20.0
sbend_length = 20.0
output_offset = 3.5  # vertical separation
gap = 0.3            # small lithographic gap at split


gf.gpdk.PDK.activate()


# =====================================
# Cross section (strip)
# =====================================
xs = gf.cross_section.strip(width=wg_width)

# =====================================
# Create component
# =====================================
c = gf.Component("horizontal_Y_S_bend")

# ---- Input straight (100 µm) ----
wg_in = c << gf.components.straight(
    length=wg_length,
    cross_section=xs
)

wg_in.move(origin=wg_in.center, destination=(0, 0))

# ---- Short straight splitter section ----
splitter = c << gf.components.straight(
    length=taper_length,
    cross_section=xs
)

splitter.connect("o1", wg_in.ports["o2"])

# ---- Upper S-bend ----
sbend_up = c << gf.components.bend_s(
    size=(sbend_length, output_offset),
    cross_section=xs
)

sbend_up.connect("o1", splitter.ports["o2"])

# ---- Lower S-bend ----
sbend_down = c << gf.components.bend_s(
    size=(sbend_length, -output_offset),
    cross_section=xs
)

sbend_down.connect("o1", splitter.ports["o2"])

# ---- Upper output straight (100 µm) ----
out_up = c << gf.components.straight(
    length=wg_length,
    cross_section=xs
)

out_up.connect("o1", sbend_up.ports["o2"])

# ---- Lower output straight (100 µm) ----
out_down = c << gf.components.straight(
    length=wg_length,
    cross_section=xs
)

out_down.connect("o1", sbend_down.ports["o2"])

# =====================================
# Center structure at (0,0)
# =====================================
c.move(origin=c.center, destination=(0, 0))

# =====================================
# Export GDS
# =====================================
c.write_gds("horizontal_Y_S_bend.gds")
c.show()
print("Horizontal Y-branch exported successfully.")