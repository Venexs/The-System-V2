from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, project_root)

import thesystem.system
import thesystem.job
import thesystem.misc as misc

rec=[]

# Beserker
def job0(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(5000, second)

    def second():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(5000, third)

    def third():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")

        thesystem.job.beserker()

    image_image_5 = PhotoImage(
        file=("anime/special/job0/image_5.png"))
    image_5 = canvas.create_image(
        348.0,
        225.0,
        image=image_image_5,
        tags="First",
        state="hidden"
    )

    image_image_6 = PhotoImage(
        file=("anime/special/job0/image_6.png"))
    image_6 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("anime/special/job0/image_7.png"))
    image_7 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)

    prog()

    return rec

# Speedster
def job1(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(5000, second)

    def second():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(5000, third)

    def third():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")

        thesystem.job.speedster()

    image_image_5 = PhotoImage(
        file=("anime/special/job1/image_5.png"))
    image_5 = canvas.create_image(
        348.0,
        225.0,
        image=image_image_5,
        tags="First",
        state="hidden"
    )

    image_image_6 = PhotoImage(
        file=("anime/special/job1/image_6.png"))
    image_6 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("anime/special/job1/image_7.png"))
    image_7 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)

    prog()

    return rec

# Tank
def job2(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(5000, second)

    def second():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(5000, third)

    def third():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")

        thesystem.job.tank()

    image_image_5 = PhotoImage(
        file=("anime/special/job2/image_5.png"))
    image_5 = canvas.create_image(
        348.0,
        225.0,
        image=image_image_5,
        tags="First",
        state="hidden"
    )

    image_image_6 = PhotoImage(
        file=("anime/special/job2/image_6.png"))
    image_6 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("anime/special/job2/image_7.png"))
    image_7 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)

    prog()

    return rec

# Artificer
def job3(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(5000, second)

    def second():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(5000, third)

    def third():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")

        thesystem.job.commander()

    image_image_5 = PhotoImage(
        file=("anime/special/job3/image_5.png"))
    image_5 = canvas.create_image(
        348.0,
        225.0,
        image=image_image_5,
        tags="First",
        state="hidden"
    )

    image_image_6 = PhotoImage(
        file=("anime/special/job3/image_6.png"))
    image_6 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("anime/special/job3/image_7.png"))
    image_7 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)

    prog()

    return rec

# Observer
def job4(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(5000, second)

    def second():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(5000, third)

    def third():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")

        thesystem.job.observer()

    image_image_5 = PhotoImage(
        file=("anime/special/job4/image_5.png"))
    image_5 = canvas.create_image(
        348.0,
        225.0,
        image=image_image_5,
        tags="First",
        state="hidden"
    )

    image_image_6 = PhotoImage(
        file=("anime/special/job4/image_6.png"))
    image_6 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("anime/special/job4/image_7.png"))
    image_7 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)

    prog()

    return rec

# Commander
def job5(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(5000, second)

    def second():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(5000, third)

    def third():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")

        thesystem.job.commander()

    image_image_5 = PhotoImage(
        file=("anime/special/job5/image_5.png"))
    image_5 = canvas.create_image(
        348.0,
        225.0,
        image=image_image_5,
        tags="First",
        state="hidden"
    )

    image_image_6 = PhotoImage(
        file=("anime/special/job5/image_6.png"))
    image_6 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("anime/special/job5/image_7.png"))
    image_7 = canvas.create_image(
        347.0,
        225.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)

    prog()

    return rec

