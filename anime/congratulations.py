import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.window_ess as we

rec=[]

def main(canvas):
    we.text(canvas, "Congratulations on becoming a", 190, 214, font_size=16*-1)
    we.text(canvas, "Player", 448, 214, font_extra="Bold", font_size=16*-1)

    return rec