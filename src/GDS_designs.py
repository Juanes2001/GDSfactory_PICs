import gdsfactory  as gf
import functions as fun

# Create the main component
# c = gf.Component()
#
# # Create a straight waveguide directly inside the component
# wg = gf.components.straight(length=1000, cross_section=gf.cross_section.strip(width=3.0))
# wg_ref = c << wg  # Insert the waveguide into the component
#
# # Create a taper directly inside the component
# taper = gf.components.taper(length=300, width1=3.0, width2=0.8, cross_section="rib")
# taper_ref = c << taper  # Insert the taper into the component
#
# # Connect the taper to the output port of the waveguide
# taper_ref.connect("o1", wg_ref.ports["o2"])
#
# # Add only two ports to the final structure
# c.add_port("o1", port=wg_ref.ports["o1"])  # Input port from the waveguide
# c.add_port("o2", port=taper_ref.ports["o2"])  # Output port from the taper

#############################################################################################

# c = fun.create_component()
# wg = fun.str_line(1000,2, gf.cross_section.strip(width=3.0))
# wg_ref = c << wg
#
# taper = fun.taper(300,3.0,0.8,"rib")
# taper_ref = c << taper
#
# taper_ref.connect("o1", wg_ref.ports["o2"])
#
# c.add_port("o1", port=wg_ref.ports["o1"])  # Input port from the waveguide
# c.add_port("o2", port=taper_ref.ports["o2"])  # Output port from the taper
#
# # Display the final design
# c.plot()
# c.show()
# c.pprint_ports()

# Define `n` and `spiral_length` values to test multiple configurations
# n_values = [3, 2, 4, 4, 4]  # Number of loops in each spiral
# spiral_lengths = [1000, 4000, 5000, 6000, 7000]  # Different snake lengths
#
# # c = fun.snake_structure(3000,2,"bend_euler180", 0.8)
#
# c = fun.spiral_with_taper_and_snake(n_values, spiral_lengths, y_offset=500, chip_length=11000, margin=200)
#
# # Verify that the ports are visible and correctly assigned
# c.pprint_ports()  # Display port names and locations in the console
# c.show()  # Open in KLayout for visualization
# c.plot()  # Plot using Matplotlib








