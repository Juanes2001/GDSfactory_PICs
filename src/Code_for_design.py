import gdsfactory  as gf
import functions as fun

def main():
    chip = gf.Component(name="StructuresUnal_Design_Demo")

    spacing = 500

    # Variables for spirals 1 , create six spirals with 2 bends and different lengths
    x_in_position = 0
    y_in_position = 0
    width_up = 3.0
    width_down = 0.42
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

    # Show a preview if you're in a Jupyter environment that supports it
    chip.plot()
    chip.pprint_ports()

    # Write out the final GDS file
    gds_filename = "my_dcouplers_and_spirals_design_Juanes.gds"
    chip.write_gds(gds_filename)
    chip.show()
    print(f"✅ GDS file saved as: {gds_filename}")


