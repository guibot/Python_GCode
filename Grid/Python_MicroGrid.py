def generate_dot_grid_gcode(
    width=100,
    height=100,
    points_x=10,
    points_y=10,
    print_height=0.2,
    z_hop=5.0,
    flow_rate=0.017,
    travel_speed=600,
    extrude_speed=60,
    origin_x=160,
    origin_y=140,
    pause_time_ms=4000
):
    gcode = []

    gcode.append("; Generated dot matrix G-code")
    gcode.append("G90 ; absolute positioning")
    gcode.append("M82 ; absolute extrusion mode")
    gcode.append("G21 ; use mm")
    gcode.append("G28 ; home all axes")
    gcode.append("T0 ; select tool 0 - extrusor")
    # gcode.append("G92 E0 ; reset extrusion")
    gcode.append("G1 Z{:.2f} F{}".format(z_hop, travel_speed))

    spacing_x = width / (points_x - 1) if points_x > 1 else 0
    spacing_y = height / (points_y - 1) if points_y > 1 else 0
    e_total = 0

    for j in range(points_y):
        for i in range(points_x):
            x = origin_x + round(i * spacing_x, 3)
            y = origin_y + round(j * spacing_y, 3)

            gcode.append("; Point ({}, {})".format(i + 1, j + 1))
            gcode.append("G1 Z{:.2f} F{}".format(z_hop, travel_speed))  # lift
            gcode.append("G1 X{:.3f} Y{:.3f} F{}".format(x, y, travel_speed))  # move
            gcode.append("G1 Z{:.2f} F{}".format(print_height, travel_speed))  # drop
            e_total += flow_rate
            gcode.append("G1 E{:.5f} F{}".format(e_total, extrude_speed))  # extrude
            gcode.append("G1 Z{:.2f} F{}".format(z_hop, travel_speed))  # lift
            gcode.append(f"G4 P{pause_time_ms} ; wait {pause_time_ms}ms")


    gcode.append("; End of print")
    gcode.append("G1 Z{:.2f} F{}".format(z_hop + 5, travel_speed))
    #gcode.append("G1 X0 Y0 F{}".format(travel_speed))
    gcode.append("M104 S0 ; turn off hotend")
    gcode.append("M140 S0 ; turn off bed")
    gcode.append("M84 ; disable motors")

    return "\n".join(gcode)

# Salvar num ficheiro:
with open("dot_matrix.gcode", "w") as f:
    f.write(generate_dot_grid_gcode(
        width=25,
        height=25,
        points_x=5,
        points_y=5,
        print_height=0.2,
        z_hop=5.0,
        flow_rate=0.022,
        travel_speed=600,
        extrude_speed=20,
        origin_x=160,
        origin_y=140,
        pause_time_ms=3000

    ))