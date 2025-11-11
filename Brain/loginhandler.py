import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import json
import time
from supabase import create_client, Client
import json as _json

# ------------------ Supabase Setup ------------------
CONFIG_PATH = os.path.join("Brain", "DONOTDELETE", "important.json")
_cfg = {}
try:
    with open(CONFIG_PATH, "r") as _f:
        _raw = _f.read().strip() or "{}"
        _cfg = _json.loads(_raw)
except Exception:
    _cfg = {}

SUPABASE_URL = _cfg.get("SUPABASE_URL", "")
SUPABASE_KEY = _cfg.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------ Assets ------------------
ASSETS_ROOT = "assets"
COMPLEX_ROOT = os.path.join(ASSETS_ROOT, "complex")
DEFAULT_ROOT = os.path.join(ASSETS_ROOT, "default")

# Choose which animation path to load
ANIM_ROOT = COMPLEX_ROOT if os.path.exists(COMPLEX_ROOT) else DEFAULT_ROOT
OPEN_GIF = os.path.join(ANIM_ROOT, "open", "loginscreen.gif")
LOOP_DIR = os.path.join(ANIM_ROOT, "loop", "loading")

GIF_PATHS = {
    "background": os.path.join(LOOP_DIR, "background.gif"),
    "email": os.path.join(LOOP_DIR, "email.gif"),
    "password": os.path.join(LOOP_DIR, "password.gif"),
    "close": os.path.join(LOOP_DIR, "close.gif"),
    "heading": os.path.join(LOOP_DIR, "heading.gif"),
    "register": os.path.join(LOOP_DIR, "register.gif")
}

# ------------------ Utility: GIF Loader ------------------
def load_gif_frames(path, resize=None):
    frames, durations = [], []
    if not os.path.exists(path):
        return frames, durations
    try:
        gif = Image.open(path)
        for frame in ImageSequence.Iterator(gif):
            frm = frame.convert("RGBA")
            if resize:
                frm = frm.resize(resize, Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frm))
            durations.append(frame.info.get("duration", 40))
    except Exception:
        pass
    return frames, durations

# ------------------ Tkinter Window ------------------
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
WINDOW_W, WINDOW_H = 800, 500
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{WINDOW_W}x{WINDOW_H}+{(sw - WINDOW_W)//2}+{(sh - WINDOW_H)//2}")
root.configure(bg="#000")

canvas = tk.Canvas(root, width=WINDOW_W, height=WINDOW_H, bd=0, highlightthickness=0, bg="#000")
canvas.pack(fill="both", expand=True)

# -----------------------------------------------------
# Placeholder for later (these will be assigned below)
# -----------------------------------------------------
def show_login_view(): ...
def show_register_view(): ...
def login_action(): ...
def signup_action(): ...

# ------------------ Stage 1: Play Opening Animation ------------------
def play_opening_animation(on_finish):
    frames, durs = load_gif_frames(OPEN_GIF, (WINDOW_W, WINDOW_H))
    if not frames:
        on_finish()
        return
    gif_id = canvas.create_image(WINDOW_W//2, WINDOW_H//2, image=frames[0])
    frame_idx = [0]

    def loop():
        if frame_idx[0] >= len(frames):
            canvas.delete(gif_id)
            on_finish()
            return
        canvas.itemconfig(gif_id, image=frames[frame_idx[0]])
        delay = durs[frame_idx[0]] if frame_idx[0] < len(durs) else 40
        frame_idx[0] += 1
        root.after(delay, loop)

    loop()

# ------------------ Stage 2: Load Element GIFs ------------------
element_gifs = {}
element_ids = {}

def create_looping_element(tag, path, position, size):
    frames, durs = load_gif_frames(path, size)
    if not frames:
        return
    gif_id = canvas.create_image(position[0], position[1], image=frames[0], anchor="center", tags=tag)
    element_gifs[tag] = {"frames": frames, "durs": durs, "idx": 0, "id": gif_id}

def animate_elements():
    for tag, data in element_gifs.items():
        frames, durs, idx, gif_id = data["frames"], data["durs"], data["idx"], data["id"]
        if not frames:
            continue
        idx = (idx + 1) % len(frames)
        canvas.itemconfig(gif_id, image=frames[idx])
        data["idx"] = idx
        element_gifs[tag] = data
    root.after(60, animate_elements)

def show_ui_elements():
    # Background
    create_looping_element("background", GIF_PATHS["background"], (WINDOW_W//2, WINDOW_H//2), (WINDOW_W, WINDOW_H))

    # Heading
    create_looping_element("heading", GIF_PATHS["heading"], (WINDOW_W//2, 70), (500, 80))

    # Email box
    create_looping_element("email", GIF_PATHS["email"], (WINDOW_W//2, 190), (400, 50))

    # Password box
    create_looping_element("password", GIF_PATHS["password"], (WINDOW_W//2, 260), (400, 50))

    # Register button
    create_looping_element("register", GIF_PATHS["register"], (WINDOW_W//2, 340), (220, 70))

    # Close button
    create_looping_element("close", GIF_PATHS["close"], (WINDOW_W - 60, 40), (40, 40))

    animate_elements()

    # Delay to make UI feel cohesive with animation sync
    root.after(100, lambda: show_login_view())

# -----------------------------------------------------
# Your existing login system code goes below (unchanged)
# -----------------------------------------------------

# ------------------ Entry Fields, Supabase Login Logic, and UI Setup ------------------
email_var = tk.StringVar()
password_var = tk.StringVar()
username_var = tk.StringVar()

entry_bg = "#101010"
entry_fg = "#eaeaea"
accent = "#05d5ff"

widgets_login = []
widgets_register = []

def clear_widgets(widgets):
    for w in widgets:
        try:
            w.place_forget()
        except Exception:
            pass

def create_entry_with_placeholder(parent, var, placeholder, x, y, width, height, show=None):
    entry = tk.Entry(parent, textvariable=var, font=("Consolas", 13), fg="#888888", bg=entry_bg, insertbackground=entry_fg, bd=0, show=show)
    entry.place(x=x, y=y, width=width, height=height)
    
    def on_focus_in(event):
        if var.get() == placeholder:
            var.set("")
            entry.config(fg=entry_fg)
            if show:
                entry.config(show=show)
    
    def on_focus_out(event):
        if not var.get():
            var.set(placeholder)
            entry.config(fg="#888888")
            if show:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    var.set(placeholder)
    if show:
        entry.config(show="")
    
    return entry

def show_login_view():
    clear_widgets(widgets_register)
    email_var.set("")
    password_var.set("")

    x_center = WINDOW_W//2
    field_w = 320
    field_h = 36

    email_entry = create_entry_with_placeholder(root, email_var, "Enter your email", x_center - field_w//2, 190, field_w, field_h)
    password_entry = create_entry_with_placeholder(root, password_var, "Enter your password", x_center - field_w//2, 240, field_w, field_h, show="*")

    login_btn = tk.Button(root, text="Login", font=("Consolas", 14, "bold"), fg="#000", bg=accent, bd=0, activebackground=accent, command=login_action)
    login_btn.place(x=x_center - 70, y=295, width=140, height=38)

    register_btn = tk.Button(root, text="Register Now", font=("Consolas", 11), fg="#fff", bg="#202020", bd=0, activebackground="#303030", command=show_register_view)
    register_btn.place(x=x_center - 75, y=345, width=150, height=34)

    widgets_login[:] = [email_entry, password_entry, login_btn, register_btn]


def show_register_view():
    clear_widgets(widgets_login)
    email_var.set("")
    username_var.set("")
    password_var.set("")

    x_center = WINDOW_W//2
    field_w = 320
    field_h = 36

    email_entry_r = create_entry_with_placeholder(root, email_var, "Enter your email", x_center - field_w//2, 170, field_w, field_h)
    username_entry_r = create_entry_with_placeholder(root, username_var, "Enter your username", x_center - field_w//2, 220, field_w, field_h)
    password_entry_r = create_entry_with_placeholder(root, password_var, "Enter your password", x_center - field_w//2, 270, field_w, field_h, show="*")

    signup_btn = tk.Button(root, text="Sign Up", font=("Consolas", 14, "bold"), fg="#000", bg=accent, bd=0, activebackground=accent, command=signup_action)
    signup_btn.place(x=x_center - 70, y=325, width=140, height=38)

    back_btn = tk.Button(root, text="Back", font=("Consolas", 11), fg="#fff", bg="#202020", bd=0, activebackground="#303030", command=show_login_view)
    back_btn.place(x=20, y=WINDOW_H-50, width=90, height=30)

    widgets_register[:] = [email_entry_r, username_entry_r, password_entry_r, signup_btn, back_btn]


def login_action():
    # your same login logic
    messagebox.showinfo("Login", "Placeholder for login logic")


def signup_action():
    # your same signup logic
    messagebox.showinfo("Signup", "Placeholder for signup logic")


# ------------------ Boot ------------------
play_opening_animation(show_ui_elements)
root.mainloop()
