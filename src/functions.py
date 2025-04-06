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


def multiple_directional_Couplers_50_to_50_with_SBend(
    coupler_width=0.8,
    chip_length=11000,  # Total allowed chip length
    margin=200,         # Safe margins
    gap=0.5,
    dx=10,
    dy=4,
    bend_s_x=10,
    bend_s_y=4,
    s_bend_size=(50, 30),  # S-Bend (width, height)
    y_offset=250
    ):
    """
    Generates directional couplers with correctly oriented S-Bends at input and output.

    Returns:
        gf.Component: Multiple directional couplers with properly adjusted S-Bends.
    """

    if gap < 0.4:
        raise ValueError(f"Invalid gap: {gap} µm. Must be >= 0.4 µm.")

    c = gf.Component()
    # Example base_length (approximation)
    base_length = 1.55 / ( 4* (1.574498017 - 1.565599018))

    for idx in range(1, 4):
        structure = gf.Component()
        length = base_length * idx

        custom_bend_s = gf.components.bend_s(
            size=(bend_s_x, bend_s_y),
            cross_section=gf.cross_section.strip(width=coupler_width),
        )

        coupler = structure.add_ref(
            gf.components.coupler(
                gap=gap,
                length=length,
                dy=dy,
                dx=dx,
                cross_section=gf.cross_section.strip(width=coupler_width),
                allow_min_radius_violation=False,
                bend=custom_bend_s
            )
        )

        # Extra length in X due to the S-bend
        s_bend_extra_length = s_bend_size[0]

        total_fixed_length = (
            2 * (1000 + 300)  # waveguides + tapers
            + length
            + 2 * s_bend_extra_length
        )

        usable_length = chip_length - 2 * margin
        remaining_length = max((usable_length - total_fixed_length) / 2, 100)

        #  **Upper Input Path**
        straight1 = structure.add_ref(
            gf.components.straight(
                length=1000,
                cross_section=gf.cross_section.strip(width=3.0)
            )
        )
        taper1 = structure.add_ref(
            gf.components.taper(
                length=300,
                width1=3.0,
                width2=coupler_width,
                cross_section="strip"
            )
        )
        s_bend1 = structure.add_ref(
            gf.components.bend_s(
                size=s_bend_size,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        straight2 = structure.add_ref(
            gf.components.straight(
                length=remaining_length,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )

        taper1.connect("o1", straight1.ports["o2"])
        s_bend1.connect("o1", taper1.ports["o2"])
        straight2.connect("o1", s_bend1.ports["o2"])
        coupler.connect("o1", straight2.ports["o2"])

        #  **Lower Input Path**
        straight3 = structure.add_ref(
            gf.components.straight(
                length=remaining_length,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        s_bend2 = structure.add_ref(
            gf.components.bend_s(
                size=s_bend_size,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        s_bend2.mirror(p1=(0, 0), p2=(0, 1))  # Mirror for correct orientation
        taper2 = structure.add_ref(
            gf.components.taper(
                length=300,
                width1=coupler_width,
                width2=3.0,
                cross_section="strip"
            )
        )
        straight4 = structure.add_ref(
            gf.components.straight(
                length=1000,
                cross_section=gf.cross_section.strip(width=3.0)
            )
        )

        straight3.connect("o1", coupler.ports["o2"])
        s_bend2.connect("o1", straight3.ports["o2"])
        taper2.connect("o1", s_bend2.ports["o2"])
        straight4.connect("o1", taper2.ports["o2"])

        #  **Upper Output Path**
        straight5 = structure.add_ref(
            gf.components.straight(
                length=remaining_length,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        s_bend3 = structure.add_ref(
            gf.components.bend_s(
                size=s_bend_size,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        s_bend3.mirror(p1=(0, 0), p2=(0, 1))
        taper3 = structure.add_ref(
            gf.components.taper(
                length=300,
                width1=coupler_width,
                width2=3.0,
                cross_section="strip"
            )
        )
        straight6 = structure.add_ref(
            gf.components.straight(
                length=1000,
                cross_section=gf.cross_section.strip(width=3.0)
            )
        )

        straight5.connect("o1", coupler.ports["o4"])
        s_bend3.connect("o1", straight5.ports["o2"])
        taper3.connect("o1", s_bend3.ports["o2"])
        straight6.connect("o1", taper3.ports["o2"])

        #  **Lower Output Path**
        straight7 = structure.add_ref(
            gf.components.straight(
                length=remaining_length,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        s_bend4 = structure.add_ref(
            gf.components.bend_s(
                size=s_bend_size,
                cross_section=gf.cross_section.strip(width=coupler_width)
            )
        )
        taper4 = structure.add_ref(
            gf.components.taper(
                length=300,
                width1=coupler_width,
                width2=3.0,
                cross_section="strip"
            )
        )
        straight8 = structure.add_ref(
            gf.components.straight(
                length=1000,
                cross_section=gf.cross_section.strip(width=3.0)
            )
        )

        straight7.connect("o1", coupler.ports["o3"])
        s_bend4.connect("o1", straight7.ports["o2"])
        taper4.connect("o1", s_bend4.ports["o2"])
        straight8.connect("o1", taper4.ports["o2"])

        #  **Labels**
        text_label1 = structure.add_ref(
            gf.components.text(
                text="DC 50:50 with S-Bend",
                size=50,
                position=(straight1.xmin + 500, straight1.ymax + 150),
                justify="left",
                layer="WG"
            )
        )

        text_label2 = structure.add_ref(
            gf.components.text(
                text="DC 50:50 with S-Bend",
                size=50,
                position=(straight6.xmin - 500, straight6.ymax + 150),
                justify="left",
                layer="WG"
            )
        )

        #  **Assign Ports**
        structure.add_port(name=f"o{4*idx-3}", port=straight1.ports["o1"])
        structure.add_port(name=f"o{4*idx-2}", port=straight4.ports["o2"])
        structure.add_port(name=f"o{4*idx-1}", port=straight8.ports["o2"])
        structure.add_port(name=f"o{4*idx}", port=straight6.ports["o2"])

        ref = c.add_ref(structure)
        ref.move((0, idx * y_offset))

    return c





