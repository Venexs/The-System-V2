import os
import sys
from tkinter import PhotoImage

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, project_root)
import thesystem

rec=[]

def main(canvas):
    image_image_5 = PhotoImage(file=("anime/special/job_change_info.png"))
    canvas.create_image(
        357.0,
        240.0,
        image=image_image_5
    )

    rec.append(image_image_5)

    thesystem.system.start_job(canvas)

    return rec
