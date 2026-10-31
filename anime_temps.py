import threading
from anyio import Path
import ujson
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import thesystem
import thesystem.system
import thesystem.window_ess as we
import sfx

def default_frame_setup(window):
    initial_height = 0
    target_height = 449
    window_width = 696

    job=thesystem.misc.return_status()["status"][1]["job"]

    all_prev=''
    video='Video'

    if job!='None':
        all_prev='alt_'
        video='Alt Video'

    top_images = f"thesystem/{all_prev}top_bar"
    bottom_images = f"thesystem/{all_prev}bottom_bar"

    top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (695, 39), job, type_="top")
    bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (702, 36), job, type_="bottom")

    threading.Thread(target=sfx.main(), daemon=True).start()

    window.geometry(f"{window_width}x{initial_height}")
    thesystem.system.animate_window_open(window, target_height, window_width, step=45, delay=1)
    thesystem.system.make_window_transparent(window)
    thesystem.system.center_window(window,window_width,target_height)
    window.configure(bg = "#FFFFFF")
    set_data=thesystem.misc.return_settings()
    transp_value=set_data["Settings"]["Transparency"]

    window.attributes('-alpha',transp_value)
    window.overrideredirect(True)
    window.wm_attributes("-topmost", True)

    with open("Files/Mod/presets.json", 'r') as pres_file:
        pres_file_data=ujson.load(pres_file)
        video_path=pres_file_data["Anime"][video]

    return top_images, bottom_images, top_preloaded_images, bottom_preloaded_images, video_path

def default_frame(canvas):
    img = PhotoImage(file="anime/default/frame.png")
    canvas.create_image(348, 233, image=img)
    return img

def default_screen_notifi(canvas, x=0, y=0):
    img1 = PhotoImage(file="anime/Main_reccur/exclam.png")
    img2 = PhotoImage(file="anime/Main_reccur/notification.png")

    canvas.create_image(379+x, 110+y, image=img2)
    canvas.create_image(186+x, 110+y, image=img1)

    return img1, img2

def transp_default(canvas):

    job=thesystem.misc.return_status()["status"][1]["job"]
    transp_clr='#0C679B'
    if job!='None':transp_clr='#652AA3'

    canvas.create_rectangle(
        0.0,
        0.0,
        300.0,
        42.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        0.0,
        414.0,
        710.0,
        449.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        0.0,
        0.0,
        696.0,
        29.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        0.0,
        5.0,
        60.0,
        455.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        647.0,
        0.0,
        696.0,
        458.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        119.0,
        0.0,
        381.0,
        38.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        56.0,
        421.0,
        923.0,
        460.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        50.0,
        19.0,
        643.0,
        44.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        137.0,
        -10.0,
        765.0,
        50.0,
        fill=transp_clr,
        outline="")

def sidebars_default(canvas):
    image_40 = thesystem.system.side_bar("left_bar.png", (47, 393))
    canvas.create_image(33.0, 235.0, image=image_40)

    image_50 = thesystem.system.side_bar("right_bar.png", (46, 385))
    canvas.create_image(666.0, 235.0, image=image_50)

    return image_40, image_50

def top_bottom_default(canvas, top_images, bottom_images):
    top_image = canvas.create_image(
        348.0,
        29.0,
        image=top_images
    )

    bottom_image = canvas.create_image(
        357.0,
        437.0,
        image=bottom_images
    )

    return top_image, bottom_image

# ==========================================================

def small_frame_setup(window):
    initial_height = 0
    target_height = 144
    window_width = 715

    job=thesystem.misc.return_status()["status"][1]["job"]

    all_prev=''
    video='Video'
    transp_clr='#0C679B'

    if job!='None':
        all_prev='alt_'
        video='Alt Video'
        transp_clr='#652AA3'

    window.geometry(f"{window_width}x{initial_height}")
    thesystem.system.animate_window_open(window, target_height, window_width, step=45, delay=1)
    thesystem.system.make_window_transparent(window, transp_clr)
    thesystem.system.center_window(window,window_width,target_height)
    window.configure(bg = "#FFFFFF")
    set_data=thesystem.misc.return_settings()
    transp_value=set_data["Settings"]["Transparency"]

    window.attributes('-alpha',transp_value)
    window.overrideredirect(True)
    window.wm_attributes("-topmost", True)

    # Preload top and bottom images
    top_images = f"thesystem/{all_prev}top_bar"
    bottom_images = f"thesystem/{all_prev}bottom_bar"

    top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (715, 41), job, type_="top")
    bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (715, 41), job, type_="bottom")

    with open("Files/Mod/presets.json", 'r') as pres_file:
        pres_file_data=ujson.load(pres_file)
        video_path=pres_file_data["Anime"][video]

    return top_images, bottom_images, top_preloaded_images, bottom_preloaded_images, video_path

def small_frame(canvas):
    image_image_2 = PhotoImage(
        file=("anime/small/frame.png"))
    image_2 = canvas.create_image(
        363.0,
        75.0,
        image=image_image_2
    )

    return image_image_2

def transp_small(canvas):

    job=thesystem.misc.return_status()["status"][1]["job"]
    transp_clr='#0C679B'
    if job!='None':transp_clr='#652AA3'

    side = PhotoImage(file=("anime/small/blue.png"))
    if job.upper()!="NONE":
        side = PhotoImage(file=("anime/small/purple.png"))

    canvas.create_image(677.0, 71.0, image=side)
    canvas.create_image(47.0, 72.0, image=side)
        
    canvas.create_rectangle(
        158.0,
        0.0,
        732.0,
        30.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        0.0,
        0.0,
        162.0,
        16.0,
        fill=transp_clr,
        outline="")

    canvas.create_rectangle(
        0.0,
        123.0,
        715.0,
        144.0,
        fill=transp_clr,
        outline="")
    
    return side

def special_small_close(canvas, window):
    image_image_3 = PhotoImage(
        file=("anime/small/close.png"))
    image_3 = canvas.create_image(
        596.0,
        53.0,
        image=image_image_3
    )

    canvas.tag_bind(image_3, "<ButtonPress-1>", lambda e: we.ex_close(window))

    return image_image_3

def top_bottom_small(canvas, top_images, bottom_images):
    top_image = canvas.create_image(
        357.0,
        20.0,
        image=top_images
    )

    bottom_image = canvas.create_image(
        370.0,
        128.0,
        image=bottom_images
    )

    return top_image, bottom_image

def sidebars_small(canvas):
    image_40 = thesystem.system.side_bar("left_bar.png", (30, 100))
    canvas.create_image(82.0, 76.0, image=image_40)

    image_50 = thesystem.system.side_bar("right_bar.png", (30, 114))
    canvas.create_image(640.0, 75.0, image=image_50)

    return image_40, image_50

# ==========================================================

def long_frame_setup(window):

    initial_height = 0
    target_height = 717
    window_width = 488

    job=thesystem.misc.return_status()["status"][1]["job"]

    all_prev=''
    video='Video'

    if job!='None':
        all_prev='alt_'
        video='Alt Video'

    top_images = f"thesystem/{all_prev}top_bar"
    bottom_images = f"thesystem/{all_prev}bottom_bar"

    top_images = f"thesystem/{all_prev}top_bar"
    bottom_images = f"thesystem/{all_prev}bottom_bar"

    top_preloaded_images = thesystem.system.load_or_cache_images(top_images, (488, 38), job, type_="top")
    bottom_preloaded_images = thesystem.system.load_or_cache_images(bottom_images, (609, 33), job, type_="bottom")

    threading.Thread(target=sfx.main(), daemon=True).start()
    
    window.geometry(f"{window_width}x{initial_height}")
    thesystem.system.animate_window_open(window, target_height, window_width, step=45, delay=1)
    thesystem.system.make_window_transparent(window)
    thesystem.system.center_window(window,window_width,target_height)
    window.configure(bg = "#FFFFFF")
    set_data=thesystem.misc.return_settings()
    transp_value=set_data["Settings"]["Transparency"]

    window.attributes('-alpha',transp_value)
    window.overrideredirect(True)
    window.wm_attributes("-topmost", True)

    with open("Files/Mod/presets.json", 'r') as pres_file:
        pres_file_data=ujson.load(pres_file)
        video_path=pres_file_data["Anime"][video]

    return top_images, bottom_images, top_preloaded_images, bottom_preloaded_images, video_path

def long_frame(canvas):
    image_2 = PhotoImage(
        file=("frame.png"))
    image_2 = canvas.create_image(
        239.0,
        350.0,
        image=image_2
    )

    return image_2


# ==========================================================
def close(window, x1=0, y1=0):
    button_image_20 = PhotoImage(
        file=("anime/Main/close.png"))
    button_20 = Button(
        image=button_image_20,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: we.ex_close(window),
        relief="flat"
    )
    button_20.place(
        x=x1,
        y=y1,
        width=21,
        height=24
    )

    return button_image_20

def start_image_animation(
    window,
    canvas,
    top_image,
    bottom_image,
    top_preloaded_images,
    bottom_preloaded_images,
    fps=24
):
    image_index = 0
    bot_image_index = 0
    delay = 1000 // fps

    def update_images():
        nonlocal image_index, bot_image_index

        image_index = (image_index + 1) % len(top_preloaded_images)
        top_img = top_preloaded_images[image_index]
        canvas.itemconfig(top_image, image=top_img)
        canvas.top_img = top_img  # prevent GC

        bot_image_index = (bot_image_index + 1) % len(bottom_preloaded_images)
        bot_img = bottom_preloaded_images[bot_image_index]
        canvas.itemconfig(bottom_image, image=bot_img)
        canvas.bot_img = bot_img

        window.after(delay, update_images)

    update_images()



