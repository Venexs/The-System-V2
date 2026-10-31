from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import ujson
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, project_root)

import thesystem.dungeon
import thesystem.window_ess as we

rec = []

def main(canvas, window):
    rank='X'

    item_name = thesystem.dungeon.get_item_name_from_csv()
    with open('Files/Player Data/Inventory.json', 'r') as file:
        data = ujson.load(file)

    # Find the item and update or remove it
    if item_name in data:
        for item in data[item_name]:
            rank=item["rank"]

    image_image_3 = PhotoImage(
        file=("anime/small/enter_txt.png"))
    image_3 = canvas.create_image(
        363.0,
        56.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=("anime/small/close.png"))
    image_4 = canvas.create_image(
        596.0,
        53.0,
        image=image_image_4
    )

    canvas.tag_bind(image_4, "<ButtonPress-1>", lambda e: we.ex_close(window))

    we.text(canvas, f"{rank}-Rank Instance Dungeon", 264, 65, "#45EF2A", font_size=15 * -1)

    button_image_1 = PhotoImage(
        file=("anime/small/yes.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: thesystem.dungeon.update_inventory(window),
        relief="flat"
    )
    button_1.place(
        x=212.0,
        y=90.0,
        width=68.0,
        height=17.0
    )

    button_image_2 = PhotoImage(
        file=("anime/small/no.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: we.ex_close(window),
        relief="flat"
    )
    button_2.place(
        x=445.0,
        y=90.0,
        width=68.0,
        height=17.0
    )

    rec.append(image_image_3)
    rec.append(image_image_4)
    rec.append(button_image_1)
    rec.append(button_image_2)

    return rec
