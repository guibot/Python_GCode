from PIL import Image
import numpy as np

def generate_dot_grid_from_image(
    image_path,
    width=100,
    height=100,
    points_x=10,
    points_y=10,
    print_height=0.2,
    z_hop=5.0,
    flow_rate=0.08,
    travel_speed=1000,
    extrude_speed=20,
    threshold=1,
    origin_x=0.0,
    origin_y=0.0,
    pause_time_ms=2000
):
    img = Image.open(image_path).convert("L").resize((points_x, points_y))

    # Inverter tons (preto vira branco e vice-versa)
    img = Image.eval(img, lambda x: 255 - x)

    # Corrigir orientação vertical
    img = img.transpose(Image.FLIP_TOP_BOTTOM)

    pixels = np.array(img)

    gcode = [
        "; Generated dot matrix G-code from image",
        "G90 ; absolute positioning",
        "M82 ; absolute extrusion mode",
        "G21 ; use mm",
        "G28 ; home all axes",
        "T0 ; select tool 0 - extrusor",
        #"G92 E0 ; reset extrusion",
        f"G1 Z{z_hop:.2f} F{travel_speed}"
    ]

    spacing_x = width / (points_x - 1)
    spacing_y = height / (points_y - 1)
    e_total = 0

    for j in range(points_y):
        for i in range(points_x):
            intensity = pixels[j][i]
            if intensity < threshold:
                x = round(origin_x + i * spacing_x, 3)
                y = round(origin_y + j * spacing_y, 3)
                amount = (255 - intensity) / 255
                extrusion = flow_rate * amount



                gcode += [
                    f"; Dot at ({i},{j}) - Intensity: {intensity}",
                    f"G1 Z{z_hop:.2f} F{travel_speed}",
                    f"G1 X{x:.3f} Y{y:.3f} F{travel_speed}",
                    f"G1 Z{print_height:.2f} F{travel_speed}",
                    f"G1 E{e_total + extrusion:.5f} F{extrude_speed}",
                    f"G4 P{pause_time_ms} ; pause after extrusion",
                    f"G1 Z{z_hop:.2f} F{travel_speed}"
                ]
                e_total += extrusion

    gcode += [
        "; End of print",
        f"G1 Z{z_hop + 5:.2f} F{travel_speed}",
        f"G1 X0 Y0 F{travel_speed}",
        "M104 S0 ; turn off hotend",
        "M140 S0 ; turn off bed",
        "M84 ; disable motors"
    ]

    return "\n".join(gcode)


# === EXECUÇÃO DO SCRIPT ===
gcode = generate_dot_grid_from_image(
    "img_spiral1.png",
    width=30,
    height=30,
    points_x=15,
    points_y=15,
    origin_x=160,
    origin_y=140
)

with open("imagem_to_dot.gcode", "w") as f:
    f.write(gcode)

print("G-code gerado com sucesso como 'imagem_to_dot.gcode'")
