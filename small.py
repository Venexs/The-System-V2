from tkinter import Tk, Canvas
import threading
import anime.runner
import sys
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import sfx
import thesystem.system
import thesystem.window_ess as we
import anime_temps

window = Tk()
top_images, bottom_images, top_preloaded_images, bottom_preloaded_images, video_path = anime_temps.small_frame_setup(window)

threading.Thread(target=sfx.main(), daemon=True).start()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 144,
    width = 715,
    highlightthickness = 0,
)

canvas.place(x = 0, y = 0)
image_index = 0
bot_image_index = 0

player = thesystem.system.FastVideoPlayer(canvas, np.load(video_path, mmap_mode='r'), 478.0, 313.0) # Video Placement
frame = anime_temps.small_frame(canvas)

image_record=anime.runner.runner_start(canvas,window)
for images in image_record:
    images

sides=anime_temps.transp_small(canvas) # Creates the Transparant Bars
left, right = anime_temps.sidebars_small(canvas) # Creates the side Bars

top_image, bottom_image = anime_temps.top_bottom_small( # Placing Top and Bottom Bars
    canvas,
    top_images=top_preloaded_images[image_index],
    bottom_images=bottom_preloaded_images[bot_image_index]
)

canvas.tag_bind(top_image, "<ButtonPress-1>", lambda e: we.start_move(window, e))
canvas.tag_bind(top_image, "<B1-Motion>", lambda e: we.move_window(window, e))

close_img = anime_temps.special_small_close(canvas,window) # Close button

anime_temps.start_image_animation( # Top and Bottom Animation Starter
    window,
    canvas,
    top_image,
    bottom_image,
    top_preloaded_images,
    bottom_preloaded_images
)

window.resizable(False, False)
window.mainloop()
