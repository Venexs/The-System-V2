import pygame
import threading
import ujson
import os
import time

# -----------------------------
# Initialization
# -----------------------------
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=128)

with open("Files/Mod/presets.json", "r") as pres_file:
    pres_file_data = ujson.load(pres_file)

with open("Files/Player Data/Theme_Check.json", "r") as theme_file:
    theme_data = ujson.load(theme_file)
    theme = theme_data["Theme"]

sfx_cache = {}
SFX_KEYS = ["Open SFX", "Button SFX", "Close SFX", "Error SFX", "Glitch SFX", "Point SFX"]

# -----------------------------
# Load sounds
# -----------------------------
def load_sound(key):
    try:
        path = pres_file_data[theme].get(key)
        if not path or not os.path.exists(path):
            print(f"[SFX Warning] File not found: {path}")
            return None
        sound = pygame.mixer.Sound(path)
        sfx_cache[key] = sound
        return sound
    except Exception as e:
        print(f"[SFX Error] Could not load '{key}': {e}")
        return None

def preload_sounds():
    for key in SFX_KEYS:
        load_sound(key)
    print(f"[SFX] Preloaded {len(sfx_cache)} sounds for theme: {theme}")

preload_sounds()

# -----------------------------
# Playback with guaranteed full playback
# -----------------------------
def play_sfx(key, wait_for_completion=False):
    """
    Play a sound safely.
    If wait_for_completion=True, blocks until sound finishes (for Close SFX).
    """
    sound = sfx_cache.get(key)
    if not sound:
        print(f"[SFX Warning] '{key}' not loaded")
        return

    def _play():
        # Play on a dedicated channel
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(sound)
            if wait_for_completion:
                # Block until the sound finishes
                while channel.get_busy():
                    time.sleep(0.01)
        else:
            # fallback
            sound.play()
            if wait_for_completion:
                time.sleep(sound.get_length())

    # Run playback in thread if not waiting
    if wait_for_completion:
        _play()  # blocking call
    else:
        threading.Thread(target=_play, daemon=True).start()

# -----------------------------
# SFX functions
# -----------------------------
def main():    play_sfx("Open SFX")
def button():  play_sfx("Button SFX")
def close():   play_sfx("Close SFX", wait_for_completion=True)  # guaranteed full playback
def error():   play_sfx("Error SFX")
def glitch():  play_sfx("Glitch SFX")
def point():   play_sfx("Point SFX")

# -----------------------------
# Stop or reload
# -----------------------------
def stop_all():
    pygame.mixer.stop()

def reload_sounds(new_theme=None):
    global theme
    if new_theme:
        theme = new_theme
    sfx_cache.clear()
    preload_sounds()
    print(f"[SFX] Reloaded theme: {theme}")
