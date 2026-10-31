import sfx
import threading
import thesystem

def start_move(window, event):
    window.lastx, window.lasty = event.widget.winfo_pointerxy()

def move_window(window, event):
    x_root, y_root = event.widget.winfo_pointerxy()
    deltax, deltay = x_root - window.lastx, y_root - window.lasty

    if deltax != 0 or deltay != 0:  # Update only if there is actual movement
        window.geometry(f"+{window.winfo_x() + deltax}+{window.winfo_y() + deltay}")
        window.lastx, window.lasty = x_root, y_root

def ex_close(window):
    threading.Thread(target=sfx.close, daemon=True).start()
    window.after(250)
    thesystem.system.animate_window_close(window, window.winfo_height(), window.winfo_width(), step=45, delay=1)

    
def text(canvas, texts, x, y, clr="#FFFFFF", font="Montserrat", font_extra="Regular", font_size=16 * -1):
    canvas.create_text(
        x,
        y,
        anchor="nw",
        text=f"{texts}",
        fill=clr,
        font=(f"{font} {font_extra}", font_size)
    )