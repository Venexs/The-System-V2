import tkinter as tk
from tkinter import PhotoImage
import threading
import ujson
import json
import csv
import subprocess
import time
from datetime import datetime, timedelta
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

import thesystem.system
import thesystem.misc
import thesystem.window_ess as we

rec = []

def main(window, canvas):

    status_data = thesystem.misc.load_ujson("Files/Player Data/Status.json")

    def title_chng(event):
        subprocess.Popen(['python', 'Anime Version/Equip Title/gui.py']) # SUBPROCESS REMOVE

        we.ex_close(window)

    def load_fatigue_value():
        with open('Files/Player Data/Status.json', 'r') as file:
            data = json.load(file)
            fatigue = data["status"][0].get("fatigue", 0)
            fatigue_max = data["status"][0].get("fatigue_max", 1)  # Avoid division by zero
            # Calculate fatigue percentage
            fatigue_percent = int((fatigue / fatigue_max) * 100)
            return fatigue_percent

    # Function to update the text on the canvas every 3 minutes
    update_after_id = None
    loaded_fatigue_value = None

    def update_fatigue_text(canvas, fatigue_val):
        global update_after_id, loaded_fatigue_value

        current_fatigue_percent = load_fatigue_value()

        # Update canvas text only if fatigue value has changed
        if current_fatigue_percent != loaded_fatigue_value:
            canvas.itemconfig(fatigue_val, text=f"{current_fatigue_percent}%")
            subprocess.Popen(['python', 'Files/Mod/default/sfx_point.py'])
            loaded_fatigue_value = current_fatigue_percent

        # Check again in 3 minutes (180,000 ms)
        update_after_id = canvas.after(180_000, update_fatigue_text, canvas, fatigue_val)

    def start_update_loop(canvas, fatigue_val):
        global update_after_id, loaded_fatigue_value
        loaded_fatigue_value = load_fatigue_value()   # Load fatigue value once
        update_after_id = canvas.after(180_000, update_fatigue_text, canvas, fatigue_val)

    def update_tabs_ujson(status='Open'):
        tabs_ujson_path = "Files/Player Data/Tabs.json"
        with open(tabs_ujson_path, 'r+') as tab_ujson:
            tab_data = ujson.load(tab_ujson)
            tab_data["Status"] = status
            tab_ujson.seek(0)
            ujson.dump(tab_data, tab_ujson, indent=4)
            tab_ujson.truncate()

    def start_job(event):
        data = thesystem.misc.load_ujson("Files/Player Data/Job_info.json")
        data["status"][0]["job_active"] = 'True'
        date_format = "%Y-%m-%d"
        future_date = (datetime.now() + timedelta(days=2)).strftime(date_format)
        with open("Files/Temp Files/Job_Change Date.csv", 'w', newline='') as file:
            csv.writer(file).writerow([future_date])
        with open("Files/Player Data/Job_info.json", 'w') as fson:
            ujson.dump(data, fson, indent=4)

    # Title color assignment
    def title_color(name):  
        color_map = {"False Ranker": "#FF2F2F", "One Above All": "#FFCF26"}
        return color_map.get(name, "#FFFFFF")

    def fatigue_window():
        subprocess.Popen(['python', 'Files/Mod/default/sfx_button.py']) # SUBPROECSS REMOVE
        subprocess.Popen(['python', 'Anime Version/Fatigue/gui.py']) # SUBPROECSS REMOVE

    # Display Character Status
    name, hp, mp, lvl = status_data["status"][0]["name"].upper(), status_data["status"][0]["hp"], status_data["status"][0]["mp"], status_data["status"][0]["level"]
    job, title = status_data["status"][1]["job"].upper(), status_data["status"][1]["title"]
    coins=status_data["status"][0]["coins"]
    av_str_based=status_data["avail_eq"][0]["str_based"]
    av_int_based=status_data["avail_eq"][0]["int_based"]
    xp = status_data["status"][0]["XP"]

    we.text(canvas, "LEVEL", 322.0, 225.0, clr="#FFFFFF", font="Montserrat", font_extra="Regular", font_size=24 * -1)
    we.text(canvas, f"{lvl:02d}", 328.0, 164.0, clr="#FFFFFF", font="Montserrat", font_extra="Bold", font_size=60 * -1)
    we.text(canvas, "JOB:", 55.0, 199.0, clr="#FFFFFF", font="Montserrat", font_extra="Bold", font_size=20 * -1)
    we.text(canvas, job, 107.0, 200.0, clr="#FFFFFF", font="Montserrat", font_extra="Regular", font_size=18 * -1)
    we.text(canvas, title.upper(), 122.0, 234.0, clr=title_color(title), font="Montserrat", font_extra="Regular", font_size=18 * -1)

    # Stat Display (STR, INT, etc.) with buffs
    stat_attributes = ["str", "int", "agi", "vit", "per", "man"]
    stat_text_widgets = {}

    for i, stat in enumerate(stat_attributes):
        value = status_data["status"][0][stat]
        buff = status_data["equipment"][0].get(stat.upper(), 0)
        position = (104 if i < 3 else 282, 392 + (i % 3) * 55)

        stat_text_widgets[stat] = canvas.create_text(position, anchor="nw", text=f"{value:03d}", fill="#FFFFFF", font=("Montserrat SemiBold", 20 * -1))
        we.text(x=position[0] + 40, y=position[1] + 5, 
                text=f"({thesystem.system.sign(buff)+thesystem.system.pos_fix(thesystem.system.equipment_value_plus(buff))})", 
                clr="#34FF48", font="Montserrat", font_extra="Regular", font_size=13 * -1)

    image_3_0 = PhotoImage(
        file=("title.png"))
    image_3 = canvas.create_image(
        150.0,
        117.0,
        image=image_3_0
    )

    rec.append(image_3_0)

    image_4_0 = PhotoImage(
        file=("breaker1.png"))
    image_4 = canvas.create_image(
        232.0,
        460.0,
        image=image_4_0
    )

    rec.append(image_4_0)

    image_5_0 = PhotoImage(
        file=("breaker2.png"))
    image_5 = canvas.create_image(
        232.0,
        333.0,
        image=image_5_0
    )

    rec.append(image_5_0)

    # ? =====================================================================
    # ? =====================================================================

    # ? =====================================================================
    # Get the result from get_fin_xp()
    fin_list = thesystem.system.get_fin_xp()

    re_check = fin_list[0]
    fin_xp=round(fin_list[1], 2)

    if re_check==True:
        try:
            subprocess.Popen(["python", "Anime Version/Status Tab/gui.py"])
            
            we.ex_close(window)
        except:
            print()

    # ? =====================================================================
    def update_stat(stat_name): 
        with open("Files/Player Data/Ability_Check.json", 'r') as ability_check_file:
            ability_check_file_data=ujson.load(ability_check_file)
            val=ability_check_file_data["Check"][stat_name.upper()]
        available_points = status_data["avail_eq"][0]["str_based"] if stat_name in ["str", "agi", "vit"] else status_data["avail_eq"][0]["int_based"]
        if val<8 and available_points > 0:
                de_update_str() if stat_name in ["str", "agi", "vit"] else de_update_int()
                status_data["status"][0][stat_name] += 1
                val=status_data["status"][0][stat_name]
                canvas.itemconfig(stat_text_widgets[stat_name], text=f"{val:03d}")
                subprocess.Popen(['python', 'Files/Mod/default/sfx_point.py'])
                status_data["avail_eq"][0]["str_based" if stat_name in ["str", "agi", "vit"] else "int_based"] -= 1
                if stat_name=='vit':
                    status_data["status"][0]["fatigue_max"]+=20
                elif stat_name=='int':
                    status_data["status"][0]["mp"]+=5
                with open("Files/Player Data/Status.json", 'w') as fson:
                    ujson.dump(status_data, fson, indent=6)
                with open("Files/Player Data/Ability_Check.json", 'w') as fin_ability_check_file:
                    ability_check_file_data["Check"][stat_name.upper()]+=1
                    ujson.dump(ability_check_file_data, fin_ability_check_file, indent=4)
                #if stat_name=='vit':
                    #update_fatigue_text(canvas,fatigue_val)
        elif val>=8 and available_points > 0:
            with open("Files/Temp Files/Urgent Temp.csv", 'w', newline='') as urgent_file:
                fr=csv.writer(urgent_file)
                fr.writerow([stat_name.upper()])
            subprocess.Popen(['python', 'Anime Version/Urgent Quest/gui.py'])
            we.ex_close(window)

    stat_buttons = {
        stat: PhotoImage(file=("plus.png"))
        for stat in stat_attributes
    }
    for stat in stat_attributes:
        canvas.create_image(
            188.0 if stat in ["str", "int", "agi"] else 364.0, 
            408.0 + (stat_attributes.index(stat) % 3) * 54, 
            image=stat_buttons[stat], 
            tags=stat
        )
        canvas.tag_bind(stat, "<ButtonPress-1>", lambda e, s=stat: update_stat(s))
        rec.append(stat_buttons[stat])
        
    # / =================================================
    # / =================================================

    def de_update_str():
        global av_str_based
        with open("Files/Player Data/Status.json", 'r') as fson:
            data=ujson.load(fson)
            check_value=data["avail_eq"][0]['str_based']
        if check_value>0:
            global av_str_based_txt
            current_number = int(check_value)
            new_number = current_number - 1
            new_text = f"{new_number:03d}"
            canvas.itemconfig(av_str_based_txt, text=new_text)
            av_str_based=new_number

    def de_update_int():
        global av_int_based
        with open("Files/Player Data/Status.json", 'r') as fson:
            data=ujson.load(fson)
            check_value=data["avail_eq"][0]['int_based']
        if check_value>0:
            global av_int_based_txt
            current_number = int(check_value)
            new_number = current_number - 1
            new_text = f"{new_number:03d}"
            canvas.itemconfig(av_int_based_txt, text=new_text)
            av_int_based=new_number

    # / =================================================
    # / =================================================

    image_6_0 = PhotoImage(
        file=("str.png"))
    image_6 = canvas.create_image(
        86.0,
        407.0,
        image=image_6_0
    )

    rec.append(image_6_0)

    image_7_0 = PhotoImage(
        file=("int.png"))
    image_7 = canvas.create_image(
        84.0,
        461.5,
        image=image_7_0
    )
    rec.append(image_7_0)
    

    image_8_0 = PhotoImage(
        file=("agi.png"))
    image_8 = canvas.create_image(
        85.0,
        517.0,
        image=image_8_0
    )
    rec.append(image_8_0)
    

    image_9_0 = PhotoImage(
        file=("vit.png"))
    image_9 = canvas.create_image(
        266.0-0,
        407.0,
        image=image_9_0
    )
    rec.append(image_9_0)

    image_10_0 = PhotoImage(
        file=("per.png"))
    image_10 = canvas.create_image(
        270.0-8,
        462.0,
        image=image_10_0
    )
    rec.append(image_10_0)

    image_11_0 = PhotoImage(
        file=("cmd.png"))
    image_11 = canvas.create_image(
        273.0-13,
        517.0,
        image=image_11_0
    )
    rec.append(image_11_0)

    gap=20

    image_12_0 = PhotoImage(
        file=("hp.png"))
    image_12 = canvas.create_image(
        94.0-gap,
        315.0,
        image=image_12_0
    )
    rec.append(image_12_0)

    canvas.create_text(
        113.0-gap,
        301.0,
        anchor="nw",
        text=hp,
        fill="#FFFFFF",
        font=("Montserrat Medium", 18 * -1)
    )

    image_13_0 = PhotoImage(
        file=("ip.png"))
    image_13 = canvas.create_image(
        190.0-gap,
        315.0,
        image=image_13_0
    )
    rec.append(image_13_0)

    canvas.create_text(
        205.0-gap,
        301.0,
        anchor="nw",
        text=mp,
        fill="#FFFFFF",
        font=("Montserrat Medium", 18 * -1)
    )

    image_13_5 = PhotoImage(
        file=("fatigue.png"))
    image_23 = canvas.create_image(
        302.0-gap,
        315.0,
        image=image_13_5
    )
    rec.append(image_13_5)

    fat_val = load_fatigue_value()
    fatigue_val=canvas.create_text(
        347.0-gap,
        301.0,
        anchor="nw",
        text=f"{int(fat_val)}%",
        fill="#FFFFFF",
        font=("Montserrat Medium", 18 * -1)
    )

    image_14_0 = PhotoImage(
        file=("xp_block.png"))
    image_14 = canvas.create_image(
        179.0,
        343.0,
        image=image_14_0
    )
    rec.append(image_14_0)

    canvas.create_text(
        280.0,
        330.0,
        anchor="nw",
        text=fin_xp,
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    canvas.create_text(
        322.0,
        225.0,
        anchor="nw",
        text="LEVEL",
        fill="#FFFFFF",
        font=("Montserrat Regular", 24 * -1)
    )

    canvas.create_text(
        55.0,
        199.0,
        anchor="nw",
        text="JOB:",
        fill="#FFFFFF",
        font=("Montserrat Bold", 20 * -1)
    )

    canvas.create_text(
        55.0,
        233.0,
        anchor="nw",
        text="TITLE:",
        fill="#FFFFFF",
        font=("Montserrat Bold", 20 * -1)
    )

    canvas.create_text(
        107.0,
        200.0,
        anchor="nw",
        text=job.upper(),
        fill="#FFFFFF",
        font=("Montserrat Regular", 18 * -1)
    )


    canvas.create_text(
        55.0,
        166.0,
        anchor="nw",
        text="NAME:",
        fill="#FFFFFF",
        font=("Montserrat Bold", 20 * -1)
    )

    canvas.create_text(
        129.0,
        167.0,
        anchor="nw",
        text=name,
        fill="#FFFFFF",
        font=("Montserrat Regular", 18 * -1)
    )

    av_int_based_txt=canvas.create_text(
        365.0,
        615.0,
        anchor="nw",
        text=f"{av_int_based:03d}",
        fill="#FFFFFF",
        font=("Montserrat Bold", 24 * -1)
    )

    image_15_0 = PhotoImage(
        file=("av_str.png"))
    image_15 = canvas.create_image(
        297.0,
        630.0,
        image=image_15_0
    )
    rec.append(image_15_0)

    av_str_based_txt=canvas.create_text(
        365.0,
        560.0,
        anchor="nw",
        text=f"{av_str_based:03d}",
        fill="#FFFFFF",
        font=("Montserrat Bold", 24 * -1)
    )

    image_15_0 = PhotoImage(
        file=("av_int.png"))
    image_16 = canvas.create_image(
        304.0,
        579.0,
        image=image_15_0
    )
    rec.append(image_15_0)

    canvas.create_text(
        51.0,
        574.0,
        anchor="nw",
        text="COINS:",
        fill="#FFFFFF",
        font=("Montserrat Medium", 16 * -1)
    )

    image_17_0 = PhotoImage(
        file=("coin_box.png"))
    image_17 = canvas.create_image(
        132.0,
        609.0,
        image=image_17_0
    )
    rec.append(image_17_0)

    canvas.create_text(
        85.0,
        598.0,
        anchor="nw",
        text=coins,
        fill="#FFFFFF",
        font=("Montserrat Regular", 20 * -1)
    )

    image_18_0= PhotoImage(
        file=("button.png"))
    image_18 = canvas.create_image(
        300.0,
        245.0,
        image=image_18_0
    )
    rec.append(image_18_0)

    canvas.tag_bind(image_18, "<ButtonPress-1>", title_chng)


    image_image_200 = PhotoImage(
        file=("job_open.png"))
    image_200 = canvas.create_image(
        300.0,
        208.0,
        image=image_image_200,
        tags='Job',
        state='normal'
    )
    rec.append(image_image_200)

    canvas.tag_bind(image_200, "<ButtonPress-1>", start_job)

    
    image_image_24 = PhotoImage(
        file=("help.png"))
    image_24 = canvas.create_image(
        261.0,
        112.0,
        image=image_image_24
    )
    rec.append(image_image_24)

    canvas.tag_bind(image_24, "<ButtonPress-1>", lambda event: thesystem.system.info_open("ABI Points"))

    image_image_25 = PhotoImage(
        file=("fatigue_win.png")) 
    image_25 = canvas.create_image(
        384.0,
        313.9999694824219,
        image=image_image_25
    )
    rec.append(image_image_25)

    canvas.tag_bind(image_25, "<ButtonPress-1>", lambda event: fatigue_window())

    start_update_loop(canvas, fatigue_val)
