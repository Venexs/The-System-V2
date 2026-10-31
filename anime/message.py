from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
from sympy import im
import ujson
import csv
import sys
import os
import numpy as np
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import sfx
import thesystem.system
import thesystem.misc

rec=[]

def main(canvas, window):
    with open("Files/Checks/Message.csv", 'r') as check_file:
        check_fr=csv.reader(check_file)
        for k in check_fr:
            message=k[0]

    with open("Files/Mod/presets.json", 'r') as pres_file:
        pres_file_data=ujson.load(pres_file)
        file_path=pres_file_data["Message"][message][0]

    canvas_center_x = window.winfo_width() // 2
    canvas_center_y = window.winfo_height() // 2

    original_image = Image.open(file_path)
    new_width = int(original_image.width * 0.95)
    new_height = int(original_image.height * 0.95)
    resized_image = original_image.resize((new_width, new_height))

    # Convert to a PhotoImage for Tkinter
    image_image_3 = ImageTk.PhotoImage(resized_image)

    # Place the resized image on the canvas
    image_3 = canvas.create_image(
        canvas_center_x,
        canvas_center_y,
        image=image_image_3
    )

    rec.append(image_image_3)
    return rec


