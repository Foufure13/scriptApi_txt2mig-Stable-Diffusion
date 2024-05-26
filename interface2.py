import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import json
import subprocess
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the Image module from the PIL package
from ttkbootstrap.widgets import Meter


# -----------------------------------------------------------------
#--------------------------CONFIGURATION --------------------------
# -----------------------------------------------------------------
#importation de mes fichier
from confighere import *
from fonctionhere import *

# Appeler la fonction pour vérifier/configurer le chemin
stable_diffusion_path = check_config()

# Vérifier le service web et exécuter le script si nécessaire
if stable_diffusion_path:
    service_url = "http://localhost:7860"  # Remplacez par l'URL de votre service web
    check_webservice_and_run_script(stable_diffusion_path, service_url)

# -----------------------------------------------------------------
#--------------------------CONFIGURATION --------------------------
# -----------------------------------------------------------------







def send_command(arg):
    subprocess.Popen(['python', 'Api_txt2img.py'] + arg.split())
    print("Command sent")
    pass

def on_slider_change(event):
    # Placeholder function for slider change
    print("Slider value:", event)

def on_dropdown_change(event):
    # Placeholder function for dropdown change
    print("Dropdown value:", event)




# -----------------------------------------------------------------
#---------------------------- WINDOWS -----------------------------
# -----------------------------------------------------------------


# Création de la fenêtre principale
root = ttk.Window(themename="superhero")
root.title("Stable Diffusion Controler")


# Ajout du meter à la boîte verte
# meter = Meter(
#     frame_green_box,
#     bootstyle="success",
#     subtextstyle="warning",
#     metersize=200,
#     amountused=50  # Définir la valeur initiale du Meter
# )
# meter.pack(ipadx=10, pady=20)


# meter = ttk.Meter(bootstyle="success", subtextstyle="warning")
# meter.pack(ipadx=10)



# Création des cadres
frame_gray = tk.Frame(root)
frame_gray.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_green = tk.Frame(root)
frame_green.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False, ipadx=20)

frame_orange = tk.Frame(frame_gray)
frame_orange.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, pady=(0, 0))


#--------------------------------------------------------------
#----------------------Zone de Prompt--------------------------
#--------------------------------------------------------------



# Partir 1
frame_part1 = tk.Frame(frame_gray)
frame_part1.pack(fill=tk.X, pady=(10, 0))


label_Prompts = tk.Label(frame_part1, text="Prompts")
label_Prompts.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche

entry_Prompts = tk.Text(frame_part1, width=50, height=5)
entry_Prompts.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
# entry_Prompts.bind("<KeyRelease>", lambda event: print("Prompts : "+entry_Prompts.get("1.0", tk.END)))


# Partir 2
frame_part2 = tk.Frame(frame_gray)
frame_part2.pack(fill=tk.X, pady=(10, 0))

label_NegPrompts = tk.Label(frame_part2, text="Negative Prompts")
label_NegPrompts.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche

#--------------------------------------------------------------
#----------------------Zone de Prompt--------------------------
#--------------------------------------------------------------




# entry_NegPrompts = tk.Entry(frame_part2, width=50)
# entry_NegPrompts.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10, pady=5, ipady=25)
entry_NegPrompts = tk.Text(frame_part2, width=50, height=5)
entry_NegPrompts.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
entry_NegPrompts.bind("<KeyRelease>", lambda event: print("Negative Prompts : "+entry_NegPrompts.get("1.0", tk.END)))




# Ajout des sliders
label_steps = tk.Label(frame_green, text="Sampling steps : 20")
label_steps.pack()
slider0 = ttk.Scale(frame_green, from_=1, to=150, length=100, command=lambda value: label_steps.config(text="Sampling steps : "+str(round(float(value)))))
slider0.pack(padx=10, pady=5)
slider0.set(20)
slider0.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider0.get()))


label_batchcount = tk.Label(frame_green, text="Batch count : 1")
label_batchcount.pack(pady=(10, 0))
slider1 = ttk.Scale(frame_green, from_=1, to=100, length=100, command=lambda value: label_batchcount.config(text="Batch count : "+str(round(float(value)))))
slider1.pack(padx=10, pady=5)
slider1.set(1)
slider1.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider1.get()))

label_batchsize = tk.Label(frame_green, text="Batch size : 1")
label_batchsize.pack(pady=(10, 0))
slider2 = ttk.Scale(frame_green, from_=1, to=8, length=100, command=lambda value: label_batchsize.config(text="Batch size : "+str(round(float(value)))))
slider2.pack(padx=10, pady=5)
slider2.set(1)
slider2.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider2.get()))

label_cfg = tk.Label(frame_green, text="CFG Scale : 4")
label_cfg.pack(pady=(10, 0))
slider3 = ttk.Scale(frame_green, from_=1, to=30, length=100, command=lambda value: label_cfg.config(text="CFG Scale : "+str(round(float(value)))))
slider3.pack(padx=10, pady=5)
slider3.set(4)
slider3.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider3.get()))

# Ajout de la liste déroulante
options = ["Option 1", "Option 2", "Option 3"]
dropdown = ttk.Combobox(frame_green, values=options, width=15)
dropdown.pack(padx=10, pady=5)
dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_change(dropdown.get()))

# Ajout du bouton SEND
button_send = tk.Button(frame_orange, text="Send Prompt", command=lambda: send_command(create_arg(entry_Prompts.get("1.0", tk.END), entry_NegPrompts.get("1.0", tk.END), round(slider0.get()), round(slider1.get()), round(slider2.get()), round(slider3.get()))))
button_send.pack(padx=10, pady=(45,15), fill=tk.BOTH, expand=True)
button_send.configure(height=1, width=15, bd=0, cursor="hand2")


# -----------------------------------------------------------------
#---------------------------- RESULT ------------------------------
# -----------------------------------------------------------------


frame_blue = tk.Frame(root)
frame_blue.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# label_blue = tk.Label(frame_blue, text="Résultat")
# label_blue.pack(pady=(10, 0))

# Ajouter la zone d'affichage des photos
photo_frame = tk.Frame(frame_blue)
photo_frame.pack(padx=10, pady=5)


# Appeler la fonction pour afficher les photos
def update_photos():
    display_photos(photo_frame)
    root.after(5000, update_photos)

update_photos()



# -----------------------------------------------------------------
#---------------------------- RESULT ------------------------------
# -----------------------------------------------------------------

# Lancement de la boucle principale
root.mainloop()
