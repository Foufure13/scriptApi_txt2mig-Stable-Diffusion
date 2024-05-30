import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import json
import subprocess
import requests
from tkinter import messagebox, filedialog
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

def send_command_faceCapture(dir, output_dir=""):
    command_capture = ["python", "capture.py", "-dir", dir]
    if output_dir:
        command_capture += ["-output", output_dir]

    os.chdir("face-capture")
    subprocess.Popen(command_capture)
    os.chdir("..")

    print("Command sent --> " + " ".join(command_capture))


def send_command_faceRecognition(dir, output_dir=""):
    command_capture = ["python", "FaceReco/eigenfaces3.py", "-gallery", dir]
    if output_dir:
        command_capture += ["-output", output_dir]

    os.chdir("face-capture")
    subprocess.Popen(command_capture)
    os.chdir("..")

    print("Command sent --> " + " ".join(command_capture))

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
root.title("Stable Diffusion Controller")

# Création d'un Notebook pour les onglets
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


#  Stable Prompt
#  #############################################################
#  #############################################################
#  #############################################################

# Fonction pour créer une page avec les widgets
def create_page_stablePrompt(parent):
    frame_gray = tk.Frame(parent)
    frame_gray.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_green = tk.Frame(frame_gray)
    frame_green.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False, ipadx=20)

    frame_orange = tk.Frame(frame_gray)
    frame_orange.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, pady=(0, 0))

    # Zone de Prompt
    frame_part1 = tk.Frame(frame_gray)
    frame_part1.pack(fill=tk.X, pady=(10, 0))

    label_Prompts = tk.Label(frame_part1, text="Prompts")
    label_Prompts.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche

    entry_Prompts = tk.Text(frame_part1, width=50, height=5)
    entry_Prompts.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    frame_part2 = tk.Frame(frame_gray)
    frame_part2.pack(fill=tk.X, pady=(10, 0))

    label_NegPrompts = tk.Label(frame_part2, text="Negative Prompts")
    label_NegPrompts.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche

    entry_NegPrompts = tk.Text(frame_part2, width=50, height=5)
    entry_NegPrompts.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
    entry_NegPrompts.bind("<KeyRelease>", lambda event: print("Negative Prompts : " + entry_NegPrompts.get("1.0", tk.END)))

    # Ajout de la liste déroulante
    label_Sampmethod = tk.Label(frame_green, text="Sampling method")
    label_Sampmethod.pack(pady=(10, 0))
    options = ['DPM++ 2M Karras', 'DPM++ SDE Karras', 'DPM++ 2M SDE Exponential', 'DPM++ 2M SDE Karras', 'Euler a', 'Euler', 'LMS', 'Heun', 'DPM2', 'DPM2 a', 'DPM++ 2S a', 'DPM++ 2M', 'DPM++ SDE', 'DPM++ 2M SDE', 'DPM++ 2M SDE Heun', 'DPM++ 2M SDE Heun Karras', 'DPM++ 2M SDE Heun Exponential', 'DPM++ 3M SDE', 'DPM++ 3M SDE Karras', 'DPM++ 3M SDE Exponential', 'DPM fast', 'DPM adaptive', 'LMS Karras', 'DPM2 Karras', 'DPM2 a Karras', 'DPM2 a Karras', 'DPM++ 2S a Karras', 'Restart', 'DDIM', 'PLMS', 'UniPC',]

    dropdown = ttk.Combobox(frame_green, values=options, width=30)
    dropdown.set("DPM++ 2M Karras")  # Set the default option
    dropdown.pack(padx=10, pady=5)
    dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_change(dropdown.get()))

    # Ajout des sliders
    label_width = tk.Label(frame_green, text="Width : 720")
    label_width.pack()
    sliderw = ttk.Scale(frame_green, from_=64, to=2400, length=150, command=lambda value: label_width.config(text="Width : " + str(round(float(value)))))
    sliderw.pack(padx=10, pady=5)
    sliderw.set(720)
    sliderw.bind("<ButtonRelease-1>", lambda event: on_slider_change(sliderw.get()))

    label_height = tk.Label(frame_green, text="Height : 720")
    label_height.pack()
    sliderh = ttk.Scale(frame_green, from_=64, to=2400, length=150, command=lambda value: label_height.config(text="Height : " + str(round(float(value)))))
    sliderh.pack(padx=10, pady=5)
    sliderh.set(720)
    sliderh.bind("<ButtonRelease-1>", lambda event: on_slider_change(sliderh.get()))

    label_steps = tk.Label(frame_green, text="Sampling steps : 20")
    label_steps.pack()
    slider0 = ttk.Scale(frame_green, from_=1, to=150, length=150, command=lambda value: label_steps.config(text="Sampling steps : " + str(round(float(value)))))
    slider0.pack(padx=10, pady=5)
    slider0.set(20)
    slider0.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider0.get()))

    label_batchcount = tk.Label(frame_green, text="Batch count : 1")
    label_batchcount.pack(pady=(10, 0))
    slider1 = ttk.Scale(frame_green, from_=1, to=100, length=150, command=lambda value: label_batchcount.config(text="Batch count : " + str(round(float(value)))))
    slider1.pack(padx=10, pady=5)
    slider1.set(1)
    slider1.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider1.get()))

    label_batchsize = tk.Label(frame_green, text="Batch size : 1")
    label_batchsize.pack(pady=(10, 0))
    slider2 = ttk.Scale(frame_green, bootstyle="danger", from_=1, to=8, length=150, command=lambda value: label_batchsize.config(text="Batch size : " + str(round(float(value)))))
    slider2.pack(padx=10, pady=5)
    slider2.set(1)
    slider2.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider2.get()))

    label_cfg = tk.Label(frame_green, text="CFG Scale : 4")
    label_cfg.pack(pady=(10, 0))
    slider3 = ttk.Scale(frame_green, from_=1, to=30, length=150, command=lambda value: label_cfg.config(text="CFG Scale : " + str(round(float(value)))))
    slider3.pack(padx=10, pady=5)
    slider3.set(4)
    slider3.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider3.get()))

    label_seed = tk.Label(frame_green, text="Seed")
    label_seed.pack(padx=(10), pady=(10, 0))  # Aligne le titre à gauche
    entry_seed = tk.Text(frame_green, width=10, height=1)
    entry_seed.pack(fill=tk.BOTH, padx=15, pady=5)
    entry_seed.insert(tk.END, "-1")
    entry_seed.tag_configure("center", justify="center")
    entry_seed.tag_add("center", "1.0", "end")

    # Ajout du bouton SEND
    button_send = tk.Button(frame_gray, text="Send Prompt", command=lambda: send_command_stablePrompt(create_arg(entry_Prompts.get("1.0", tk.END), entry_NegPrompts.get("1.0", tk.END), round(slider0.get()), round(slider1.get()), round(slider2.get()), round(slider3.get()), round(sliderw.get()), round(sliderh.get()), dropdown.get(), entry_seed.get("1.0", tk.END))))
    button_send.pack(padx=10, pady=(45, 15), fill=tk.BOTH, expand=True)
    button_send.configure(height=1, width=15, bd=0, cursor="hand2")
    button_send.place(relx=0.5, rely=1, anchor=tk.S, width=200, height=50)


#  Face Capture
#  #############################################################
#  #############################################################
#  #############################################################

def create_page_faceCapture(parent):
    frame_gray = tk.Frame(parent)
    frame_gray.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_green = tk.Frame(frame_gray)
    frame_green.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False, ipadx=20)

    frame_orange = tk.Frame(frame_gray)
    frame_orange.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, pady=(0, 0))

    # Zone de Prompt
    frame_part1 = tk.Frame(frame_gray)
    frame_part1.pack(fill=tk.X, pady=(10, 0))

    # Section for input folder
    def browse_folder():
        folder_path = filedialog.askdirectory()
        entry_folder.delete(0, tk.END)
        entry_folder.insert(tk.END, folder_path)

    label_folder = tk.Label(frame_part1, text="Images Folder Path to face capture")
    label_folder.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 0))  # Align the label to the left

    entry_folder = tk.Entry(frame_part1, width=50)
    entry_folder.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(5, 0))

    button_browse = tk.Button(frame_part1, text="Browse", command=browse_folder)
    button_browse.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 10))


    # Section for output folder
    def browse_output_folder():
        output_folder_path = filedialog.askdirectory()
        entry_output_folder.delete(0, tk.END)
        entry_output_folder.insert(tk.END, output_folder_path)

    label_output_folder = tk.Label(frame_part1, text="Output Folder Path")
    label_output_folder.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(10, 0))  # Align the label to the left

    entry_output_folder = tk.Entry(frame_part1, width=50)
    entry_output_folder.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(5, 0))

    button_browse_output = tk.Button(frame_part1, text="Browse", command=browse_output_folder)
    button_browse_output.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 10))
   

    # Ajout de la liste déroulante
    label_Sampmethod = tk.Label(frame_green, text="Sampling method")
    label_Sampmethod.pack(pady=(10, 0))

    # Ajout du bouton SEND
    button_send = tk.Button(frame_gray, text="Send Prompt", command=lambda: send_command_faceCapture(entry_folder.get(),entry_output_folder.get()))
    button_send.pack(padx=10, pady=(45, 15), fill=tk.BOTH, expand=True)
    button_send.configure(height=1, width=15, bd=0, cursor="hand2")
    button_send.place(relx=0.5, rely=1, anchor=tk.S, width=200, height=50)


def create_page_faceRecognition(parent):
    frame_gray = tk.Frame(parent)
    frame_gray.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    frame_green = tk.Frame(frame_gray)
    frame_green.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False, ipadx=20)

    frame_orange = tk.Frame(frame_gray)
    frame_orange.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, pady=(0, 0))

    # Zone de Prompt
    frame_part1 = tk.Frame(frame_gray)
    frame_part1.pack(fill=tk.X, pady=(10, 0))

    # Section for input folder
    def browse_folder():
        folder_path = filedialog.askdirectory()
        entry_folder.delete(0, tk.END)
        entry_folder.insert(tk.END, folder_path)

    label_folder = tk.Label(frame_part1, text="Images Folder Path to Picture Recognition [Only Faces Grey Pictures]")
    label_folder.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 0))  # Align the label to the left

    entry_folder = tk.Entry(frame_part1, width=50)
    entry_folder.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(5, 0))

    button_browse = tk.Button(frame_part1, text="Browse", command=browse_folder)
    button_browse.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 10))


    # Section for output folder
    def browse_output_folder():
        output_folder_path = filedialog.askdirectory()
        entry_output_folder.delete(0, tk.END)
        entry_output_folder.insert(tk.END, output_folder_path)

    label_output_folder = tk.Label(frame_part1, text="Output Folder Path")
    label_output_folder.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(10, 0))  # Align the label to the left

    entry_output_folder = tk.Entry(frame_part1, width=50)
    entry_output_folder.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(5, 0))

    button_browse_output = tk.Button(frame_part1, text="Browse", command=browse_output_folder)
    button_browse_output.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 10))
   

    # Ajout de la liste déroulante
    label_Sampmethod = tk.Label(frame_green, text="Sampling method")
    label_Sampmethod.pack(pady=(10, 0))

    # Ajout du bouton SEND
    button_send = tk.Button(frame_gray, text="Send Prompt", command=lambda: send_command_faceCapture(entry_folder.get(),entry_output_folder.get()))
    button_send.pack(padx=10, pady=(45, 15), fill=tk.BOTH, expand=True)
    button_send.configure(height=1, width=15, bd=0, cursor="hand2")
    button_send.place(relx=0.5, rely=1, anchor=tk.S, width=200, height=50)




# Créer les deux pages
page1 = ttk.Frame(notebook)
page2 = ttk.Frame(notebook)
page3 = ttk.Frame(notebook)


create_page_stablePrompt(page1)
create_page_faceCapture(page2)
create_page_faceRecognition(page3)

notebook.add(page1, text="Stable Prompt")
notebook.add(page2, text="Face Capture")
notebook.add(page3, text="Face Recognition")

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
    global last_files
    output_folder = "dir_stable_images"
    current_files = set(os.listdir(output_folder))
    
    if current_files != last_files:
        last_files = current_files
        display_photos(photo_frame)
        
    root.after(10000, update_photos)

display_photos(photo_frame)
last_files = set(os.listdir("dir_stable_images"))
update_photos()

# -----------------------------------------------------------------
#---------------------------- RESULT ------------------------------
# -----------------------------------------------------------------

# Lancement de la boucle principale
root.mainloop()
