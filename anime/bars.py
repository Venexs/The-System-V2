from pathlib import Path
from filelock import FileLock
from tkinter import PhotoImage
import ujson
import threading
import numpy as np
import sys
import os
import time
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, project_root)
import sfx

rec = []

last_warn_time = 0  # global tracker
target_hp = 0
warn1 = False
current_hp_display = 0
hp_max = 1

x_add=20

def hp_bar(canvas, window):

    def read_hp():
        lock = FileLock("Files/Player Data/status.json.lock")
        with lock:
            with open("Files/Player Data/Status.json", 'r') as fson:
                data = ujson.load(fson)
        return data["status"][0]['hp'], data["status"][0]['hp_max']

    def init_health():
        """Run once at startup: sync display with actual file values."""
        global current_hp_display, target_hp, hp_max
        hp, hp_max = read_hp()
        current_hp_display = target_hp = hp
        update_display()

    def update_health_bar():
        """Runs every 1s to fetch the real hp from the file."""
        global target_hp, hp_max
        hp, hp_max = read_hp()
        target_hp = hp
        window.after(1000, update_health_bar)

    def animate_health_text():
        """
        Runs every 10 ms. Adjusts HP smoothly so the total change
        completes in ~2 seconds regardless of difference.
        """
        global current_hp_display, target_hp

        if current_hp_display != target_hp:
            diff = target_hp - current_hp_display
            step = diff / 200.0  # 200 ticks in 2 seconds
            # Make sure very small diffs still complete
            if abs(step) < 1:
                step = 1 if diff > 0 else -1

            current_hp_display += step

            # Clamp to avoid overshoot
            if (step > 0 and current_hp_display > target_hp) or (step < 0 and current_hp_display < target_hp):
                current_hp_display = target_hp
            
        update_display()
        window.after(5, animate_health_text)

    def update_display():
        global warn1, last_warn_time
        # Bar width
        bar_width = 442 - 187 + 91
        current_width = (current_hp_display / hp_max) * bar_width
        canvas.coords(health_bar, 187+x_add, 66, 187 + current_width + x_add, 70.5)
        
        # Update HP text
        canvas.itemconfig(hp_text, text=f"{int(current_hp_display)}")
        canvas.itemconfig(hp_max_text, text=f"/{hp_max}")
        
        # Change bar color based on health percent
        health_percent = (current_hp_display / hp_max) * 100
        if health_percent < 30:
            canvas.itemconfig(health_bar, fill="#FF0000")
            canvas.itemconfig(hp_text, fill="#FF0000")
            canvas.itemconfig(hp_max_text, fill="#FF0000")
            
            # play sound only once per second
            current_time = time.time()
            if current_time - last_warn_time >= 1:
                threading.Thread(target=sfx.error(), daemon=True).start()
                last_warn_time = current_time
        else:
            canvas.itemconfig(health_bar, fill="#FFFFFF")
            canvas.itemconfig(hp_text, fill="#FFFFFF")
            canvas.itemconfig(hp_max_text, fill="#FFFFFF")

    with open("Files/Player Data/Status.json", 'r') as fson:
        data=ujson.load(fson)
        hp=data["status"][0]['hp']
        hp_max=data["status"][0]['hp_max']

    image_image_3 = PhotoImage(
        file=("anime/small/hp.png"))
    image_3 = canvas.create_image(
        158.0,
        75.0,
        image=image_image_3
    )

    image_image_9 = PhotoImage(
        file=("anime/small/bar_back.png"))
    image_9 = canvas.create_image(
        360.0+x_add,
        68.0,
        image=image_image_9
    )

    health_bar = canvas.create_rectangle(
        187.0+x_add,
        66,
        442.0+91+x_add,
        70.5,
        fill="#FFFFFF",
        outline="")

    hp_text = canvas.create_text(
        333.0+100+x_add,
        79.0,
        anchor="nw",
        text=f"{hp}",
        fill="#FFFFFF",
        font=("Montserrat Medium", 18 * -1)
    )

    hp_max_text = canvas.create_text(
        385.0+100+x_add,
        82.0,
        anchor="nw",
        text=f"/ {hp_max}",
        fill="#FFFFFF",
        font=("Montserrat Regular", 15 * -1)
    )

    rec.append(image_image_3)
    rec.append(image_image_9)

    init_health()
    update_health_bar()
    animate_health_text()

    return rec
