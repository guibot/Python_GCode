Python Img to Grid GCODE Generator

![Heart Dots](heart_dots.jpg)

**********************************************************

DISCLAIMER

This software is an experimental GCODE generator created specifically for a custom Bio Printer. It is intended for research and personal use only.

Use at your own risk.

The software is provided "as is", without warranty of any kind, either express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or noninfringement.

The creator(s) are not responsible for any damages or consequences arising from the use of this tool, including but not limited to any printer malfunctions, injuries, or other unexpected outcomes.

By using this software, you acknowledge and accept the risks involved.

************************************************************

Python_ImageToGrid.py

all parameters need to be edited in the .py script

gcode = generate_dot_grid_from_image(
    "img_spiral1.png",
    width=30,
    height=30,
    points_x=15,
    points_y=15,
    origin_x=160,
    origin_y=140
)

************************************************************

Python_ImageToGrid_APP.py

This script creates a webapp at http://127.0.0.1:5000/

![Python_ImgToGrid_WebAPP](ImgToGrid_WebAPP.jpg)


