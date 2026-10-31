from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
import os

rec=[]

def main(canvas):
    image_image_2 = PhotoImage(
        file=("anime/small/level_up.png"))
    image_2 = canvas.create_image(
        363.0,
        77.0,
        image=image_image_2
    )

    rec.append(image_image_2)

    return rec

