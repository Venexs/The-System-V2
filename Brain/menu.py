import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import math
import os
import subprocess
import sys
import time

# ------------------- Config -------------------
INNER_HEXAGON_RADIUS = 80  # Inner hexagon (from home.py)
OUTER_HEXAGON_RADIUS = 140  # Outer hexagon (button border)
EXTEND_DISTANCE = 20  # How much to extend on hover
ANIMATION_DELAY = 15
BUTTON_COLORS = {
    "default": "#003d68",
    "hover": "#3a3a3a",
    "quit": "#6B0101",
    "quit_hover": "#ff7e7e",
    "hexagon": "#044655",
    "hexagon_outline": "#96E6F7"
}

# Button labels and positions
# Mapping: right-top, top, left-top, left-bottom, bottom, right-bottom
# Hexagon vertices: -30°(top-right), 30°(right), 90°(bottom-right), 150°(bottom-left), 210°(left), 270°(top-left)
# But we want: right-top, top, left-top, left-bottom, bottom, right-bottom
# So: -30°(right-top)=STATS, 90°(top)=DUNGEONS, 150°(left-top)=SETTINGS, 210°(left-bottom)=INVENTORY, 270°(bottom)=QUIT, 30°(right-bottom)=SHOP
BUTTON_LABELS = ["STATS", "DUNGEONS", "SETTINGS", "INVENTORY", "QUIT", "SHOP"]
# Button angle offsets: -30°, 90°, 150°, 210°, 270°, 30°
BUTTON_ANGLES = [-30, 90, 150, 210, 270, 30]

# ------------------- Setup Window -------------------
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Center the menu window (larger to accommodate extended buttons)
menu_size = 450
center_x = screen_width // 2
center_y = screen_height // 2
root.geometry(f"{menu_size}x{menu_size}+{center_x - menu_size//2}+{center_y - menu_size//2}")

if os.name == "nt":
    root.wm_attributes("-transparentcolor", "white")
canvas = Canvas(root, width=menu_size, height=menu_size, highlightthickness=0, 
                bg="white" if os.name == "nt" else "#000000")
canvas.pack(fill=tk.BOTH, expand=True)

# ------------------- Pre-calculated Values -------------------
CENTER_CANVAS_X = menu_size // 2
CENTER_CANVAS_Y = menu_size // 2
BUTTON_ANGLES_RAD = [math.radians(angle) for angle in BUTTON_ANGLES]
THIRTY_DEG_RAD = math.radians(30)
SIXTY_DEG_RAD = math.radians(60)

# ------------------- Assets -------------------
ASSETS_MENU_DIR = "assets/menu"
ICON_SIZE = 32  # Size of icons in buttons

# ------------------- State -------------------
button_hover_states = [False] * 6
button_polygons = []
button_texts = []
button_icons = []
button_extend_progress = [0.0] * 6
animating = False
icon_cache = {}

# ------------------- Draw Trapezium Button -------------------
def create_trapezium_button(index, inner_radius, outer_radius, extend=0):
    # Pre-calculated angle for this button
    start_angle = BUTTON_ANGLES_RAD[index]
    end_angle = start_angle + SIXTY_DEG_RAD
    
    # Cache cos/sin values
    cos_start = math.cos(start_angle)
    sin_start = math.sin(start_angle)
    cos_end = math.cos(end_angle)
    sin_end = math.sin(end_angle)
    
    # Inner hexagon points (where trapezium connects to inner hexagon)
    inner_x1 = CENTER_CANVAS_X + inner_radius * cos_start
    inner_y1 = CENTER_CANVAS_Y + inner_radius * sin_start
    inner_x2 = CENTER_CANVAS_X + inner_radius * cos_end
    inner_y2 = CENTER_CANVAS_Y + inner_radius * sin_end
    
    # Outer hexagon points (extended on hover)
    outer_radius_with_extend = outer_radius + extend
    outer_x1 = CENTER_CANVAS_X + outer_radius_with_extend * cos_start
    outer_y1 = CENTER_CANVAS_Y + outer_radius_with_extend * sin_start
    outer_x2 = CENTER_CANVAS_X + outer_radius_with_extend * cos_end
    outer_y2 = CENTER_CANVAS_Y + outer_radius_with_extend * sin_end
    
    # Create trapezium (4 points: inner_start, outer_start, outer_end, inner_end)
    return [inner_x1, inner_y1, outer_x1, outer_y1, outer_x2, outer_y2, inner_x2, inner_y2]

# ------------------- Load Icon -------------------
def load_button_icon(label):
    # Convert label to lowercase filename (e.g., "STATS" -> "stats.png")
    icon_name = label.lower()
    icon_path = os.path.join(ASSETS_MENU_DIR, f"{icon_name}.png")
    
    # Check cache first
    if icon_path in icon_cache:
        return icon_cache[icon_path]
    
    # Try to load icon
    if os.path.exists(icon_path):
        try:
            img = Image.open(icon_path).convert("RGBA")
            img = img.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            icon_cache[icon_path] = photo
            return photo
        except Exception as e:
            print(f"Error loading icon {icon_path}: {e}")
    
    return None

# ------------------- Draw Buttons -------------------
def draw_all_buttons():
    # Clear existing buttons using tags for efficiency
    canvas.delete("button_polygon")
    canvas.delete("button_text")
    canvas.delete("button_icon")
    button_polygons.clear()
    button_texts.clear()
    button_icons.clear()
    
    for i, label in enumerate(BUTTON_LABELS):
        is_quit = (label == "QUIT")
        extend = EXTEND_DISTANCE * button_extend_progress[i]
        
        # Create trapezium
        points = create_trapezium_button(i, INNER_HEXAGON_RADIUS, OUTER_HEXAGON_RADIUS, extend)
        
        # Choose color (pre-check)
        color = (BUTTON_COLORS["quit_hover"] if button_hover_states[i] else BUTTON_COLORS["quit"]) if is_quit else (BUTTON_COLORS["hover"] if button_hover_states[i] else BUTTON_COLORS["default"])
        
        # Draw trapezium
        poly_id = canvas.create_polygon(points, fill=color, outline="#05d5ff", width=1.5, 
                                        tags=("button_polygon", f"button_{i}"))
        button_polygons.append(poly_id)
        
        # Calculate center position of trapezium (cached angle)
        angle = BUTTON_ANGLES_RAD[i]
        center_radius = (INNER_HEXAGON_RADIUS + OUTER_HEXAGON_RADIUS + extend) * 0.5
        angle_for_pos = angle + THIRTY_DEG_RAD
        center_x = CENTER_CANVAS_X + center_radius * math.cos(angle_for_pos)
        center_y = CENTER_CANVAS_Y + center_radius * math.sin(angle_for_pos)
        
        # Load and draw icon (cached)
        icon_photo = load_button_icon(label)
        if icon_photo:
            icon_id = canvas.create_image(center_x, center_y - 8, image=icon_photo, 
                                         tags=("button_icon", f"button_icon_{i}"))
            button_icons.append(icon_id)
            # Bind events to icon
            canvas.tag_bind(icon_id, "<Enter>", lambda e, idx=i: on_button_enter(idx))
            canvas.tag_bind(icon_id, "<Leave>", lambda e, idx=i: on_button_leave(idx))
            canvas.tag_bind(icon_id, "<Button-1>", lambda e, idx=i, lbl=label: on_button_click(idx, lbl))
        
        # Draw text below icon
        text_id = canvas.create_text(center_x, center_y + 12, text=label, fill="#ffffff", 
                                    font=("Consolas", 8, "bold"), tags=("button_text", f"button_text_{i}"))
        button_texts.append(text_id)
        
        # Bind events to polygon and text
        for tag_id in [poly_id, text_id]:
            canvas.tag_bind(tag_id, "<Enter>", lambda e, idx=i: on_button_enter(idx))
            canvas.tag_bind(tag_id, "<Leave>", lambda e, idx=i: on_button_leave(idx))
            canvas.tag_bind(tag_id, "<Button-1>", lambda e, idx=i, lbl=label: on_button_click(idx, lbl))

def animate_button_extends():
    global animating
    if animating:
        return
    animating = True
    
    def step_animation():
        global animating
        changed = False
        INTERP_FACTOR = 0.25
        THRESHOLD = 0.01
        
        for i in range(6):
            target = 1.0 if button_hover_states[i] else 0.0
            current = button_extend_progress[i]
            diff = target - current
            
            if abs(diff) > THRESHOLD:
                changed = True
                button_extend_progress[i] += diff * INTERP_FACTOR
        
        if changed:
            draw_all_buttons()
            root.after(ANIMATION_DELAY, step_animation)
        else:
            animating = False
    
    step_animation()

def on_button_enter(index):
    button_hover_states[index] = True
    animate_button_extends()

def on_button_leave(index):
    button_hover_states[index] = False
    animate_button_extends()

def on_button_click(index, label):
    if label == "QUIT":
        handle_quit()
    else:
        handle_button_click(index, label)

# ------------------- Button Actions -------------------
def handle_button_click(index, text):
    print(f"Button {index} clicked: {text}")
    if text == "QUIT":
        return  # QUIT is handled separately
    
    # Convert button label to Python filename (e.g., "STATS" -> "stats.py")
    filename = text.lower() + ".py"
    filepath = os.path.join("Brain", "menu", filename)
    
    if os.path.exists(filepath):
        try:
            subprocess.Popen(["python", filepath])
        except Exception as e:
            print(f"Error running {filepath}: {e}")
    else:
        print(f"File not found: {filepath}")

def handle_quit():
    try:
        # Create a quit flag file for home.py to check
        quit_flag_file = "Brain/files/quit_flag.txt"
        os.makedirs(os.path.dirname(quit_flag_file), exist_ok=True)
        with open(quit_flag_file, "w") as f:
            f.write("quit")
        
        # Run save.py
        save_process = subprocess.Popen(["python", "Brain/save.py"])
        time.sleep(0.3)
        
        # Quit menu window
        root.quit()
        root.destroy()
        sys.exit(0)
    except Exception as e:
        print(f"Error running save.py: {e}")
        root.quit()
        root.destroy()

# ------------------- Initialize Menu -------------------
def init_menu():
    # Don't draw inner hexagon here - it's already drawn by home.py
    # Just draw the trapezium buttons
    root.update_idletasks()  # Ensure window is ready
    
    # Draw a test rectangle to verify visibility (can be removed later)
    # canvas.create_rectangle(10, 10, 50, 50, fill="red", outline="yellow")
    
    draw_all_buttons()
    
    # Verify buttons were created
    if len(button_polygons) == 0:
        print("WARNING: No buttons were drawn!")
    else:
        print(f"Menu initialized: {len(button_polygons)} buttons drawn")
    
    root.update()  # Force immediate update

# ------------------- Close on Escape -------------------
def on_escape(event):
    root.quit()
    root.destroy()

# Check for close flag from home.py
CLOSE_FLAG_FILE = "Brain/files/close_menu_flag.txt"

def check_close_flag():
    if os.path.exists(CLOSE_FLAG_FILE):
        try:
            # Read and remove the flag
            with open(CLOSE_FLAG_FILE, "r") as f:
                f.read()  # Just to ensure file is readable
            try:
                os.remove(CLOSE_FLAG_FILE)
            except:
                pass
            # Close the window
            root.quit()
            root.destroy()
            return True
        except Exception as e:
            print(f"Error handling close flag: {e}")
    return False

def periodic_close_check():
    if check_close_flag():
        return
    root.after(100, periodic_close_check)

root.bind("<Escape>", on_escape)

# ------------------- Start -------------------
# Ensure window is visible and on top
root.lift()
root.focus_force()
init_menu()
periodic_close_check()
root.mainloop()
