import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import subprocess
import math
import time

# ------------------- Config -------------------
BUTTON_IMAGE_PATH = "assets/home/icon.gif"   # looping gif
RECT_IMAGE_PATH = "assets/home/home.png"
BUTTON_RADIUS = 45  # increased size for better visibility
ANIMATION_STEPS = 25
ANIMATION_DELAY = 15
QUIT_BUTTON_HEIGHT = 25
QUIT_BUTTON_WIDTH = 60

# ------------------- Setup Tkinter -------------------
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Adjusted position for bigger button
start_x = screen_width - (BUTTON_RADIUS*2 + 30)
start_y = 30
window_size = BUTTON_RADIUS*2 + 10
root.geometry(f"{window_size}x{window_size}+{start_x}+{start_y}")

# Transparent background
if os.name == "nt":
    root.wm_attributes("-transparentcolor", "white")

canvas = tk.Canvas(
    root,
    width=window_size,
    height=window_size,
    highlightthickness=0,
    bg="white" if os.name == "nt" else ""
)
canvas.pack()

# ------------------- Load Images -------------------
_image_cache_home = {}

def load_circle_gif(path, radius):
    """Load and resize a GIF, returning a list of PhotoImage frames with circular mask."""
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path)
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_image = img.convert("RGBA").resize((radius*2, radius*2), Image.LANCZOS)
            mask = Image.new("L", (radius*2, radius*2), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, radius*2, radius*2), fill=255)
            frame_image.putalpha(mask)
            frames.append(ImageTk.PhotoImage(frame_image))
        return frames
    except Exception as e:
        print("Error loading GIF:", e)
        return None

def load_rect_image(path, size):
    if not os.path.exists(path):
        return None
    cache_key = f"{path}_{size}"
    if cache_key in _image_cache_home:
        return _image_cache_home[cache_key]
    try:
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        _image_cache_home[cache_key] = photo
        return photo
    except Exception:
        return None

button_frames = load_circle_gif(BUTTON_IMAGE_PATH, BUTTON_RADIUS)
rect_photo = load_rect_image(RECT_IMAGE_PATH, (200, 100))

# ------------------- State -------------------
at_center = False
animating = False
dragging = False
offset_x = offset_y = 0
quit_button_visible = False
menu_process = None
current_gif_frame = 0

center_win_x = (screen_width - 200) // 2
center_win_y = (screen_height - 200) // 2

quit_button = tk.Button(
    root, text="QUIT", font=("Arial", 10), bg="red", fg="white",
    command=root.destroy
)
quit_button.place_forget()

# ------------------- Utilities -------------------
def check_quit_flag():
    quit_flag_file = "Brain/files/quit_flag.txt"
    if os.path.exists(quit_flag_file):
        try:
            os.remove(quit_flag_file)
            root.quit()
            root.destroy()
            return True
        except:
            pass
    return False

def draw_hexagon(canvas, center_x, center_y, radius, **kwargs):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.extend([x, y])
    return canvas.create_polygon(points, **kwargs)

# ------------------- Draw Button -------------------
def draw_button(rect=False):
    global current_gif_frame
    canvas.delete("all")

    if rect:
        if rect_photo:
            canvas.config(width=200, height=200)
            canvas.create_image(100, 100, image=rect_photo)
        else:
            canvas.config(width=200, height=200)
            draw_hexagon(canvas, 100, 100, 80, fill="#1a1a1a", outline="#05d5ff", width=2)
    else:
        if button_frames:
            canvas.config(width=BUTTON_RADIUS*2, height=BUTTON_RADIUS*2)
            frame = button_frames[current_gif_frame]
            canvas.create_image(BUTTON_RADIUS, BUTTON_RADIUS, image=frame)
        else:
            canvas.config(width=BUTTON_RADIUS*2, height=BUTTON_RADIUS*2)
            canvas.create_oval(0, 0, BUTTON_RADIUS*2, BUTTON_RADIUS*2, fill="black")

def update_gif_frame():
    """Continuously loop the circular GIF."""
    global current_gif_frame
    if not at_center and button_frames:
        current_gif_frame = (current_gif_frame + 1) % len(button_frames)
        draw_button(rect=False)
    root.after(100, update_gif_frame)  # adjust delay for speed

# ------------------- Menu Handling -------------------
def run_menu():
    global menu_process
    close_flag_file = "Brain/files/close_menu_flag.txt"
    if os.path.exists(close_flag_file):
        try:
            os.remove(close_flag_file)
        except:
            pass

    try:
        menu_process = subprocess.Popen(["python", "Brain/menu.py"])
    except Exception as e:
        print("Error running menu.py:", e)

def close_menu():
    global menu_process
    close_flag_file = "Brain/files/close_menu_flag.txt"
    try:
        os.makedirs(os.path.dirname(close_flag_file), exist_ok=True)
        with open(close_flag_file, "w") as f:
            f.write("close")
    except Exception as e:
        print(f"Error creating close flag: {e}")

    if menu_process:
        try:
            menu_process.terminate()
            time.sleep(0.3)
            if menu_process.poll() is None:
                menu_process.kill()
                time.sleep(0.1)
        except:
            pass
    menu_process = None

    def cleanup_flag():
        try:
            if os.path.exists(close_flag_file):
                os.remove(close_flag_file)
        except:
            pass
    root.after(500, cleanup_flag)

# ------------------- Animation -------------------
def animate(to_center=True):
    global at_center, animating, quit_button_visible

    animating = True
    quit_button.place_forget()
    quit_button_visible = False

    if to_center:
        target_x, target_y = center_win_x, center_win_y
    else:
        target_x, target_y = start_x, start_y

    step = 0
    dx = (target_x - root.winfo_x()) / ANIMATION_STEPS
    dy = (target_y - root.winfo_y()) / ANIMATION_STEPS

    def step_animation():
        nonlocal step
        global at_center, animating, menu_process
        if step < ANIMATION_STEPS:
            new_x = int(root.winfo_x() + dx)
            new_y = int(root.winfo_y() + dy)
            root.geometry(f"{window_size}x{window_size}+{new_x}+{new_y}")
            step += 1
            draw_button(rect=at_center)
            root.after(ANIMATION_DELAY, step_animation)
        else:
            root.geometry(f"{200}x{200}+{target_x}+{target_y}" if to_center else f"{window_size}x{window_size}+{target_x}+{target_y}")
            at_center = to_center
            draw_button(rect=at_center)
            if at_center:
                if menu_process is None:
                    run_menu()
                else:
                    poll_result = menu_process.poll()
                    if poll_result is not None:
                        menu_process = None
                        run_menu()
            animating = False

    step_animation()

# ------------------- Drag -------------------
def start_drag(event):
    global dragging, offset_x, offset_y
    if at_center or animating:
        return
    dragging = True
    offset_x = event.x
    offset_y = event.y

def stop_drag(event):
    global dragging
    dragging = False

def do_drag(event):
    if dragging:
        new_x = root.winfo_x() + (event.x - offset_x)
        new_y = root.winfo_y() + (event.y - offset_y)
        root.geometry(f"{window_size}x{window_size}+{new_x}+{new_y}")

canvas.bind("<ButtonPress-1>", start_drag)
canvas.bind("<ButtonRelease-1>", stop_drag)
canvas.bind("<B1-Motion>", do_drag)

# ------------------- Click -------------------
def on_left_click(event):
    global animating, at_center
    if animating or dragging:
        return
    if at_center:
        close_menu()
        animate(False)
    else:
        animate(True)

def on_right_click(event):
    global quit_button_visible
    if at_center:
        btn_x = root.winfo_x() + (200 - QUIT_BUTTON_WIDTH)//2
        btn_y = root.winfo_y() + 100 + 5
        quit_button.place(x=btn_x, y=btn_y, width=QUIT_BUTTON_WIDTH, height=QUIT_BUTTON_HEIGHT)
        quit_button_visible = True

canvas.bind("<Button-1>", on_left_click)
canvas.bind("<Button-3>", on_right_click)

# ------------------- Start -------------------
draw_button()
update_gif_frame()

def periodic_check():
    if check_quit_flag():
        return
    root.after(100, periodic_check)

periodic_check()
root.mainloop()
