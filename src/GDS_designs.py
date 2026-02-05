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

#############################################################################

# Define `n` and `spiral_length` values to test multiple configurations
# n_values = [3, 2, 4, 4, 4]  # Number of loops in each spiral
# spiral_lengths = [1000, 4000, 5000, 6000, 7000]  # Different snake lengths
#
# # c = fun.snake_structure(3000,2,"bend_euler180", 0.8)
#
# c = fun.spiral_with_taper_and_snake(n_values, spiral_lengths)
#
# # Verify that the ports are visible and correctly assigned
# c.pprint_ports()  # Display port names and locations in the console
# c.show()  # Open in KLayout for visualization
# c.plot()  # Plot using Matplotlib




def main():
    """
    Main function that creates a 'root' chip component and
    places the multiple directional couplers within it.
    """
    gf.gpdk.PDK.activate()

    # Root chip component with a custom name
    chip = gf.Component(name="StructuresUnal_Design_Demo")

    spacing = 500

    # Variables for spirals 1 , create six spirals with 2 bends and different lengths
    x_in_position = 0
    y_in_position = 0
    width_up = 3.0
    width_down = 0.8
    y_offset = 300
    spiral_array = [2,2,2,2,2,2]
    lengths_array = [1000,2000,3000,4000,5000,6000]



    spirals1 = fun.spiral_with_taper_and_snake(spiral_array,
                                              lengths_array,
                                              width_up,
                                              width_down,
                                              y_offset,
                                              x_in_position,
                                              y_in_position)
    chip.add_ref(spirals1[0])

    # Variables for spirals 2 , create three spirals with 2 bends and different lengths
    x_in_position = spirals1[1]
    y_in_position = spirals1[2] + spacing
    width_up = 3.0
    width_down = 0.8
    y_offset = 300
    spiral_array = [2, 4, 6]
    lengths_array = [3000, 3000, 3000]


    spirals2 = fun.spiral_with_taper_and_snake(spiral_array,
                                              lengths_array,
                                              width_up,
                                              width_down,
                                              y_offset,
                                              x_in_position,
                                              y_in_position)

    chip.add_ref(spirals2[0])


    #Variables for the DC 50:50 at 780nm wavelenght
    num_of_couplers = 3
    initial_pos_x = spirals2[1]
    initial_pos_y = spirals2[2]
    y_offset = 300
    coupler_width = 0.35
    gap = 0.4
    inner_s_bend_x = 10
    inner_s_bend_y = 4
    outter_s_bend_x = 50
    outter_s_bend_y = 30                    # S-Bend (width, height)
    laser_lambda  = 0.78
    n1 = 1.776611224
    n2 = 1.776134225

    dc_50_50 = fun.multiple_directional_Couplers_50_to_50_with_SBend(num_of_couplers,
                                                                      initial_pos_x,
                                                                      initial_pos_y,
                                                                      y_offset,
                                                                      coupler_width,
                                                                      gap,
                                                                      inner_s_bend_x,
                                                                      inner_s_bend_y,
                                                                      outter_s_bend_x,
                                                                      outter_s_bend_y,  # S-Bend (width, height)
                                                                      laser_lambda,
                                                                      n1,
                                                                      n2)
    chip.add_ref(dc_50_50[0])

    # Variables for the DC 25:75 at 780nm wavelenght
    num_of_couplers = 3
    initial_pos_x = dc_50_50[1]
    initial_pos_y = dc_50_50[2]
    y_offset = 300
    coupler_width = 0.35
    gap = 0.4
    inner_s_bend_x = 10
    inner_s_bend_y = 4
    outter_s_bend_x = 50
    outter_s_bend_y = 30  # S-Bend (width, height)
    laser_lambda = 0.78
    n1 = 1.776611224
    n2 = 1.776134225

    dc_25_75 = fun.multiple_directional_Couplers_25_to_75_with_SBend(num_of_couplers,
                                                                     initial_pos_x,
                                                                     initial_pos_y,
                                                                     y_offset,
                                                                     coupler_width,
                                                                     gap,
                                                                     inner_s_bend_x,
                                                                     inner_s_bend_y,
                                                                     outter_s_bend_x,
                                                                     outter_s_bend_y,  # S-Bend (width, height)
                                                                     laser_lambda,
                                                                     n1,
                                                                     n2)
    chip.add_ref(dc_25_75[0])

    # Variables for the DC 0:100 at 780nm wavelenght
    num_of_couplers = 3
    initial_pos_x = dc_25_75[1]
    initial_pos_y = dc_25_75[2]
    y_offset = 300
    coupler_width = 0.35
    gap = 0.4
    inner_s_bend_x = 10
    inner_s_bend_y = 4
    outter_s_bend_x = 50
    outter_s_bend_y = 30  # S-Bend (width, height)
    laser_lambda = 0.78
    n1 = 1.776611224
    n2 = 1.776134225

    dc_0_100 = fun.multiple_directional_Couplers_0_to_100_with_SBend(num_of_couplers,
                                                                     initial_pos_x,
                                                                     initial_pos_y,
                                                                     y_offset,
                                                                     coupler_width,
                                                                     gap,
                                                                     inner_s_bend_x,
                                                                     inner_s_bend_y,
                                                                     outter_s_bend_x,
                                                                     outter_s_bend_y,  # S-Bend (width, height)
                                                                     laser_lambda,
                                                                     n1,
                                                                     n2)
    chip.add_ref(dc_0_100[0])


    # Show a preview if you're in a Jupyter environment that supports it
    chip.plot()
    chip.pprint_ports()

    # Write out the final GDS file
    gds_filename = "my_dcouplers_and_spirals_design_Juanes.gds"
    chip.write_gds(gds_filename)
    chip.show()
    print(f"✅ GDS file saved as: {gds_filename}")


# If running as a standalone script (e.g. python script.py):
if __name__ == "__main__":
    main()


