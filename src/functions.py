import gdsfactory  as gf
from pyglet.libs.win32 import com


def create_component():
    c = gf.Component()
    return c

def taper(length, width1, width2, crss_section):
    c = gf.components.taper(length=length, width1=width1, width2=width2, cross_section=crss_section)
    # el cross section es la forma
    # que adopta la seccion transversal, en este caso es cuadrado
    return c

def str_line(length, crss_section):
    # Import the structure
    c = gf.components.straight(length=length, cross_section=crss_section)
    return c

def snake_structure(spiral_length,num_spirals,spiral_style, width ):
    c = gf.components.delay_snake2(
        length=spiral_length,
        length0=0,
        length2=0,
        n=num_spirals,
        bend180=spiral_style,
        cross_section=gf.cross_section.strip(width = width)
    )

    return c



def spiral_with_taper_and_snake(n_values, spiral_lengths, y_offset=700, chip_length=11000, margin=200):
    """
    Generates multiple structures consisting of:
    - An input straight waveguide
    - An input taper
    - A snake (spiral) waveguide
    - An output taper
    - An output straight waveguide

    Each structure ensures proper spacing within the chip dimensions.

    Args:
        n_values (list): List of `n` values (number of bends in the snake).
        spiral_lengths (list): List of snake (spiral) lengths.
        y_offset (float): Vertical spacing between each generated structure.
        chip_length (float): Total chip length constraint.
        margin (float): Safety margin at the chip edges.
    """
    c = create_component()

    for idx, (n, spiral_length) in enumerate(zip(n_values, spiral_lengths)):
        structure = create_component()

        # Base parameters
        wg_width = 3.0  # Width of the input and output straight waveguides
        taper_length = 300  # Fixed taper length
        usable_length = chip_length - 2 * margin  # Available space on the chip

        # Generate the snake (spiral) component with the given parameters
        snake_component = snake_structure(spiral_length, n, "bend_euler180", 0.8)

        snake_length_real = snake_component.size_info.width  # Actual X length of the snake

        # Compute the remaining space for the straight waveguides
        remaining_length = usable_length - (1000 + taper_length + snake_length_real + taper_length + 1000)

        if remaining_length < 0:
            raise ValueError(f"The total design length exceeds {chip_length} µm.")

        straight_length = remaining_length / 2  # Divide evenly for both straight waveguides

        # 1. Create the first straight waveguide (input)
        straight_waveguide1 = structure.add_ref(
            # gf.components.straight(length=1000, cross_section=gf.cross_section.strip(width=wg_width))
            str_line(100,gf.cross_section.strip(width=wg_width))
        )
        structure.add_port(name=f"o{2*idx+1}", port=straight_waveguide1.ports["o1"])  # Define correct input port

        # 2. Create the first taper (3.0 µm → 0.8 µm)
        taper_in = structure.add_ref(
            # gf.components.taper(
            #     length=taper_length,
            #     width1=3.0,
            #     width2=0.8,
            #     cross_section=gf.cross_section.strip
            # )
            taper(taper_length,3.0,0.8,gf.cross_section.strip)
        )
        taper_in.connect("o1", straight_waveguide1.ports["o2"])

        # 3. Create the second straight waveguide (before the snake)
        straight_waveguide2 = structure.add_ref(
            # gf.components.straight(length=straight_length, cross_section=gf.cross_section.strip(width=0.8))
            str_line(straight_length, gf.cross_section.strip(width=0.8))
        )
        straight_waveguide2.connect("o1", taper_in.ports["o2"])

        # 4. Add the snake (spiral) structure
        snake = structure.add_ref(snake_component)
        snake.connect("o1", straight_waveguide2.ports["o2"])

        # 5. Create the third straight waveguide (after the snake)
        straight_waveguide3 = structure.add_ref(
            # gf.components.straight(length=straight_length, cross_section=gf.cross_section.strip(width=0.8))
            str_line(straight_length, gf.cross_section.strip(width=0.8))
        )
        straight_waveguide3.connect("o1", snake.ports["o2"])

        # 6. Create the second taper (0.8 µm → 3.0 µm)
        taper_out = structure.add_ref(
            # gf.components.taper(
            #     length=taper_length,
            #     width1=0.8,
            #     width2=3.0,
            #     cross_section=gf.cross_section.strip
            # )
            taper(taper_length, 0.8, 3.0, gf.cross_section.strip)
        )
        taper_out.connect("o1", straight_waveguide3.ports["o2"])

        # 7. Create the last straight waveguide (output)
        straight_waveguide4 = structure.add_ref(
            # gf.components.straight(length=1000, cross_section=gf.cross_section.strip(width=wg_width))
            str_line(1000, gf.cross_section.strip(width=wg_width))
        )
        straight_waveguide4.connect("o1", taper_out.ports["o2"])

        # 8. Define the correct output port name
        structure.add_port(name=f"o{2*idx+2}", port=straight_waveguide4.ports["o2"])

        # Add the complete structure to `c` and position it with an offset in Y
        ref = c.add_ref(structure)
        ref.move((0, idx * y_offset))  # Offset each structure vertically

        # Re-add the ports to the main component
        c.add_port(name=f"o{2*idx+1}", port=ref.ports[f"o{2*idx+1}"])
        c.add_port(name=f"o{2*idx+2}", port=ref.ports[f"o{2*idx+2}"])

    return c





