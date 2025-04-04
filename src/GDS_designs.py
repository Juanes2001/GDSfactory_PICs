import gdsfactory  as gf

# Create the main component
c = gf.Component()

# Create a straight waveguide directly inside the component
wg = gf.components.straight(length=1000, cross_section=gf.cross_section.strip(width=3.0))
wg_ref = c << wg  # Insert the waveguide into the component

# Create a taper directly inside the component
taper = gf.components.taper(length=300, width1=3.0, width2=0.8, cross_section="rib")
taper_ref = c << taper  # Insert the taper into the component

# Connect the taper to the output port of the waveguide
taper_ref.connect("o1", wg_ref.ports["o2"])

# Add only two ports to the final structure
c.add_port("o1", port=wg_ref.ports["o1"])  # Input port from the waveguide
c.add_port("o2", port=taper_ref.ports["o2"])  # Output port from the taper

# Display the final design
c.plot()
c.show()
c.pprint_ports()