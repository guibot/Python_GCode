from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import io

app = Flask(__name__)
last_preview = None  # imagem gerada com grelha e pontos


def generate_dot_preview(pixels, points_x, points_y):
    img_width = 400
    img_height = 400
    spacing_x = img_width / (points_x - 1)
    spacing_y = img_height / (points_y - 1)

    preview = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(preview)

    for j in range(points_y):
        for i in range(points_x):
            intensity = pixels[j][i]
            x = int(i * spacing_x)
            y = int(j * spacing_y)
            if intensity > 0:
                draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill="black")
            draw.ellipse((x - 1, y - 1, x + 1, y + 1), outline="gray")

    preview = preview.transpose(Image.FLIP_TOP_BOTTOM)

    return preview


@app.route("/", methods=["GET", "POST"])
def index():
    global last_preview
    gcode = ""
    
    form_data = {
        "width": 100.0,
        "height": 100.0,
        "points_x": 10,
        "points_y": 10,
        "origin_x": 0.0,
        "origin_y": 0.0,
        "print_height": 0.2,
        "z_hop": 2.0,
        "flow_rate": 0.05,
        "pause_time_ms": 100
    }

    if request.method == "POST":
        image = request.files["image"]
        form_data["width"] = float(request.form["width"])
        form_data["height"] = float(request.form["height"])
        form_data["points_x"] = int(request.form["points_x"])
        form_data["points_y"] = int(request.form["points_y"])
        form_data["origin_x"] = float(request.form["origin_x"])
        form_data["origin_y"] = float(request.form["origin_y"])
        form_data["print_height"] = float(request.form["print_height"])
        form_data["z_hop"] = float(request.form["z_hop"])
        form_data["flow_rate"] = float(request.form["flow_rate"])
        form_data["pause_time_ms"] = int(request.form["pause_time_ms"])

        # Process image
        img = Image.open(image).convert("L").resize((form_data["points_x"], form_data["points_y"]))
        img = ImageOps.invert(img).transpose(Image.FLIP_TOP_BOTTOM)
        pixels = np.array(img)

        last_preview = generate_dot_preview(pixels, form_data["points_x"], form_data["points_y"])

        # G-code generation
        spacing_x = form_data["width"] / (form_data["points_x"] - 1)
        spacing_y = form_data["height"] / (form_data["points_y"] - 1)
        e_total = 0

        gcode_lines = [
            "; Generated dot matrix G-code from image",
            "G90 ; absolute positioning",
            "M82 ; absolute extrusion mode",
            "G21 ; use mm",
            "G28 ; home all axes",
            "T0 ; select tool 0",
            f"G1 Z{form_data['z_hop']:.2f} F1000"
        ]

        for j in range(form_data["points_y"]):
            for i in range(form_data["points_x"]):
                intensity = pixels[j][i]
                if intensity > 0:
                    x = round(form_data["origin_x"] + i * spacing_x, 3)
                    y = round(form_data["origin_y"] + j * spacing_y, 3)
                    extrusion = form_data["flow_rate"]
                    gcode_lines += [
                        f"; Dot at ({i},{j}) - Intensity: {intensity}",
                        f"G1 Z{form_data['z_hop']:.2f} F1000",
                        f"G1 X{x:.3f} Y{y:.3f} F1000",
                        f"G1 Z{form_data['print_height']:.2f} F1000",
                        f"G1 E{e_total + extrusion:.5f} F20",
                        f"G4 P{form_data['pause_time_ms']}",
                        f"G1 Z{form_data['z_hop']:.2f} F1000"
                    ]
                    e_total += extrusion

        gcode_lines += [
            "; End of print",
            f"G1 Z{form_data['z_hop'] + 5:.2f} F1000",
            "M104 S0",
            "M140 S0",
            "M84"
        ]

        gcode = "\n".join(gcode_lines)

    return render_template("index.html", gcode=gcode, form_data=form_data)




@app.route("/preview.png")
def preview():
    global last_preview
    if last_preview is None:
        return "", 404
    img_io = io.BytesIO()
    last_preview.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
