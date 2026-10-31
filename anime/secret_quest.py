from tkinter import Button, PhotoImage
import sys
import os

rec=[]

def main(canvas, window):

    def prog():
        canvas.itemconfig("First", state="normal")
        window.after(3000, hide_first)

    def hide_first():
        canvas.itemconfig("First", state="hidden")
        canvas.itemconfig("Second", state="normal")
        window.after(3000, show_third)

    def show_third():
        canvas.itemconfig("Second", state="hidden")
        canvas.itemconfig("Third", state="normal")
        window.after(30000, end_prog)

    def end_prog():
        canvas.itemconfig("Third", state="hidden")
        window.quit()  # Uncomment this line if you want to close the window after 20 seconds

    def fin(a):
        subprocess.Popen(['python', 'First/Congrats/gui.py']) # SUBPROCESS REMOVE
        window.quit()

    def no(a):
        window.quit()


    image_image_5 = PhotoImage(
        file=("image_5.png"))
    image_5 = canvas.create_image(
        347.0,
        276.0,
        image=image_image_5,
        tags="First",
        state="hidden"  
    )

    image_image_6 = PhotoImage(
        file=("image_6.png"))
    image_6 = canvas.create_image(
        363.0,
        206.0,
        image=image_image_6,
        tags="Second",
        state="hidden"
    )

    image_image_7 = PhotoImage(
        file=("image_7.png"))
    image_7 = canvas.create_image(
        349.0,
        202.0,
        image=image_image_7,
        tags="Third",
        state="hidden"
    )

    image_image_8 = PhotoImage(
        file=("image_8.png"))
    image_8 = canvas.create_image(
        236.0,
        300.0,
        image=image_image_8,
        tags="Third",
        state="hidden"
    )

    canvas.tag_bind(image_8, "<ButtonPress-1>", fin)

    image_image_9 = PhotoImage(
        file=("image_9.png"))
    image_9 = canvas.create_image(
        439.0,
        300.0,
        image=image_image_9,
        tags="Third",
        state="hidden"
    )

    canvas.tag_bind(image_9, "<ButtonPress-1>", no)

    rec.append(image_image_5)
    rec.append(image_image_6)
    rec.append(image_image_7)
    rec.append(image_image_8)
    rec.append(image_image_9)

    prog()

    return rec

    
