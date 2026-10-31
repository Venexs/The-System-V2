from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
import os
import numpy as np
import anime.runner

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.system
import thesystem.window_ess as we
import anime_temps

window = Tk()
top_images, bottom_images, top_preloaded_images, bottom_preloaded_images, video_path = anime_temps.default_frame_setup(window)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 449,
    width = 696,
    highlightthickness = 0
)

canvas.place(x = 0, y = 0)
image_index = 0
bot_image_index = 0

player = thesystem.system.FastVideoPlayer(canvas, np.load(video_path, mmap_mode='r'), 478.0, 313.0) # Video Placement
frame_img = anime_temps.default_frame(canvas) # White Frame Default Size
exclam_img, notif_img = anime_temps.default_screen_notifi(canvas) # Notification Header Default Size 

image_record=anime.runner.runner_start(canvas,window)
for images in image_record:
    images

anime_temps.transp_default(canvas) # Creates the Transparant Bars
left, right = anime_temps.sidebars_default(canvas) # Creates the side Bars

top_image, bottom_image = anime_temps.top_bottom_default( # Placing Top and Bottom Bars
    canvas,
    top_images=top_preloaded_images[image_index],
    bottom_images=bottom_preloaded_images[bot_image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", lambda e: we.start_move(window, e))
canvas.tag_bind(top_image, "<B1-Motion>", lambda e: we.move_window(window, e))

anime_temps.start_image_animation( # Top and Bottom Animation Starter
    window,
    canvas,
    top_image,
    bottom_image,
    top_preloaded_images,
    bottom_preloaded_images
)

close = anime_temps.close(window, 564.0, 70.0) # Window Close Button

window.resizable(False, False)
window.mainloop()
