import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os, socket, threading, time, gc

ASSETS_DIR = "assets"
SPLASH_WIDTH = 640
SPLASH_HEIGHT = 360


# =======================================================
# CYBERPUNK THEMED ANIMATION SELECTION WINDOW
# =======================================================
def choose_animation_type():
    """
    Shows cyberpunk-styled pop-up asking whether to load complex animations.
    Background plays complex.gif if present, otherwise black.
    """
    choice = {"value": None}

    win = tk.Tk()
    win.overrideredirect(True)
    win.wm_attributes("-topmost", True)
    win.configure(bg="#000000")

    # Size and center
    WIDTH, HEIGHT = 480, 270
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - WIDTH)//2, (sh - HEIGHT)//2
    win.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
    canvas.pack()

    # Try to load complex.gif
    gif_path = os.path.join(ASSETS_DIR, "loadingscreen", "complex.gif")
    frames, delay = [], 80
    if os.path.exists(gif_path):
        gif = Image.open(gif_path)
        delay = gif.info.get("duration", 80)
        for frame in ImageSequence.Iterator(gif):
            f = frame.convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(f.copy()))
    else:
        from PIL import Image
        img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
        frames = [ImageTk.PhotoImage(img)]

    bg_id = canvas.create_image(WIDTH//2, HEIGHT//2, image=frames[0])

    # Border
    canvas.create_rectangle(10, 10, WIDTH-10, HEIGHT-10, outline="#00ffff", width=2)

    # Text
    canvas.create_text(
        WIDTH//2, 70,
        text="ACTIVATE COMPLEX ANIMATIONS?",
        fill="#00ffff",
        font=("Consolas", 13, "bold")
    )

    # Hover glow effect
    def on_hover(widget, enter, base_color, glow_color):
        widget.config(bg=glow_color if enter else base_color)

    def choose_complex():
        choice["value"] = "complex"
        win.destroy()

    def choose_default():
        choice["value"] = "default"
        win.destroy()

    # Buttons
    btn_style = dict(width=10, height=1, font=("Consolas", 11, "bold"), cursor="hand2", bd=0)

    btn_yes = tk.Label(win, text="YES", fg="#000", bg="#00ffff", **btn_style)
    btn_no = tk.Label(win, text="NO", fg="#000", bg="#ff0066", **btn_style)

    btn_yes.place(x=WIDTH//2 - 110, y=HEIGHT//2 + 30)
    btn_no.place(x=WIDTH//2 + 20, y=HEIGHT//2 + 30)

    btn_yes.bind("<Enter>", lambda e: on_hover(btn_yes, True, "#00ffff", "#33ffff"))
    btn_yes.bind("<Leave>", lambda e: on_hover(btn_yes, False, "#00ffff", "#00ffff"))
    btn_no.bind("<Enter>", lambda e: on_hover(btn_no, True, "#ff0066", "#ff3399"))
    btn_no.bind("<Leave>", lambda e: on_hover(btn_no, False, "#ff0066", "#ff0066"))
    btn_yes.bind("<Button-1>", lambda e: choose_complex())
    btn_no.bind("<Button-1>", lambda e: choose_default())

    # Animate background
    frame_idx = [0]
    def animate():
        frame_idx[0] = (frame_idx[0] + 1) % len(frames)
        canvas.itemconfig(bg_id, image=frames[frame_idx[0]])
        win.after(delay, animate)

    animate()
    win.mainloop()
    return choice["value"] or "default"


# =======================================================
# SPLASH SCREEN (USES loop.gif)
# =======================================================
class SplashScreen:
    def __init__(self, animation_mode="default"):
        self.animation_mode = animation_mode
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        TRANSPARENT_COLOR = "#ff00ff"
        self.root.config(bg=TRANSPARENT_COLOR)
        self.root.attributes('-transparentcolor', TRANSPARENT_COLOR)

        # Center window
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw - SPLASH_WIDTH)//2, (sh - SPLASH_HEIGHT)//2
        self.root.geometry(f"{SPLASH_WIDTH}x{SPLASH_HEIGHT}+{x}+{y}")

        self.canvas = tk.Canvas(
            self.root, width=SPLASH_WIDTH, height=SPLASH_HEIGHT,
            bd=0, highlightthickness=0, bg=TRANSPARENT_COLOR
        )
        self.canvas.pack()

        # Always load loop.gif from assets/loadingscreen
        gif_path = os.path.join(ASSETS_DIR, "loadingscreen", "loop.gif")
        if os.path.exists(gif_path):
            self.frames, self.frame_delay = self.load_gif(gif_path)
        else:
            self.frames, self.frame_delay = self.black_screen()

        self.gif_id = self.canvas.create_image(SPLASH_WIDTH//2, SPLASH_HEIGHT//2, image=self.frames[0])

        self.text_id = self.canvas.create_text(
            SPLASH_WIDTH//2, SPLASH_HEIGHT - 30,
            text="", fill="red", font=("Consolas", 11, "bold")
        )

        self.frame_index = 0
        self.is_running = True
        self.active_refs = []

    def black_screen(self):
        img = Image.new("RGBA", (SPLASH_WIDTH, SPLASH_HEIGHT), (0, 0, 0, 255))
        return [ImageTk.PhotoImage(img)], 100

    def load_gif(self, path):
        gif = Image.open(path)
        delay = gif.info.get("duration", 50)
        orig_w, orig_h = gif.size
        scale = min(SPLASH_WIDTH / orig_w, SPLASH_HEIGHT / orig_h)
        new_size = (int(orig_w * scale), int(orig_h * scale))
        frames = []
        for frame in ImageSequence.Iterator(gif):
            im = frame.convert("RGBA").resize(new_size, Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(im.copy()))
        return frames, delay

    def animate_gif(self):
        if not self.is_running:
            return
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        frame = self.frames[self.frame_index]
        self.active_refs.append(frame)
        if len(self.active_refs) > 5:
            self.active_refs.pop(0)
        self.canvas.itemconfig(self.gif_id, image=frame)
        self.root.after(self.frame_delay, self.animate_gif)
        gc.collect()

    def is_wifi_available(self, timeout_seconds=2):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_seconds)
            sock.connect(("1.1.1.1", 53))
            sock.close()
            return True
        except Exception:
            return False

    def preload_assets(self):
        image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
        video_exts = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
        for root_dir, _, files in os.walk(ASSETS_DIR):
            for fname in files:
                fpath = os.path.join(root_dir, fname)
                ext = os.path.splitext(fname.lower())[1]
                try:
                    if ext in image_exts:
                        with Image.open(fpath) as img:
                            img.load()
                    elif ext in video_exts:
                        with open(fpath, "rb") as f:
                            _ = f.read()
                except Exception:
                    pass

    def go_next(self):
        self.is_running = False
        self.root.destroy()
        os.system("python Brain/loginhandler.py")

    def start_sequence(self):
        if not self.is_wifi_available():
            self.canvas.itemconfig(self.text_id, text="Please connect to wifi and try again")
            self.root.after(4000, self.root.destroy)
            return

        start_time = time.time()
        preload_thread = threading.Thread(target=self.preload_assets, daemon=True)
        preload_thread.start()

        def check_done():
            elapsed = time.time() - start_time
            if not preload_thread.is_alive() and elapsed >= 3:
                self.root.after(500, self.go_next)
            else:
                self.root.after(200, check_done)
        check_done()

    def run(self):
        self.root.after(0, self.animate_gif)
        self.root.after(0, self.start_sequence)
        self.root.mainloop()


# =======================================================
# MAIN ENTRYPOINT
# =======================================================
if __name__ == "__main__":
    animation_choice = choose_animation_type()
    splash = SplashScreen(animation_mode=animation_choice)
    splash.run()
