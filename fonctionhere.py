import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import json
import subprocess
import io
import datetime
import requests
import base64
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # Import the Image module from the PIL package
from ttkbootstrap.widgets import Meter


def send_command_stablePrompt(arg):
    subprocess.Popen(['python', 'Api_txt2img.py'] + arg.split())
    print("Command sent")
    pass

def send_command_faceCapture(dir, output_dir=""):
    command_capture = ["python", "capture.py", "-dir", dir]
    if output_dir:
        command_capture += ["-output", output_dir]

    os.chdir("face-capture")
    subprocess.Popen(command_capture)
    os.chdir("..")

    print("Command sent --> " + " ".join(command_capture))


def send_command_faceRecognition(dir, output_dir=""):
    command_capture = ["python", "eigenfaces4.py", "--gallery", dir]
    # command_capture = ["python", "eigenfaces4.py", ""]

    if output_dir:
        command_capture += ["-output", output_dir]

    os.chdir("FaceReco")
    subprocess.Popen(command_capture)
    os.chdir("..")

    print("Command sent --> " + " ".join(command_capture))

def on_slider_change(event):
    # Placeholder function for slider change
    print("Slider value:", event)

def on_dropdown_change(event):
    # Placeholder function for dropdown change
    print("Dropdown value:", event)


def create_arg(prompt, negprompt, steps, batchcount, batchsize, cfg, width, height, samplingMethod, seed):
    prompt = prompt.replace("\n", "")
    negprompt = negprompt.replace("\n", "")

    sampler_name_list = ['DPM++ 2M Karras','DPM++ SDE Karras','DPM++ 2M SDE Exponential','DPM++ 2M SDE Karras', 'Euler a','Euler', 'LMS', 'Heun', 'DPM2', 'DPM2 a' ,'DPM++ 2S a','DPM++ 2M','DPM++ SDE','DPM++ 2M SDE','DPM++ 2M SDE Heun','DPM++ 2M SDE Heun Karras','DPM++ 2M SDE Heun Exponential','DPM++ 3M SDE','DPM++ 3M SDE Karras','DPM++ 3M SDE Exponential','DPM fast','DPM adaptive','LMS Karras','DPM2 Karras','DPM2 a Karras','DPM2 a Karras','DPM++ 2S a Karras','Restart','DDIM','PLMS','UniPC',]

    if samplingMethod in sampler_name_list:
        sampler_index = sampler_name_list.index(samplingMethod)
    else:
        sampler_index = 2

    arg_list = []
    if prompt != "":
        arg_list.append("--prompt \"" + prompt + "\"")
    if negprompt != "":
        arg_list.append("--NegativePrompt \"" + negprompt + "\"")
    if steps != 20:
        arg_list.append("--steps " + str(steps))
    if batchcount != 1:
        arg_list.append("--batch_count " + str(batchcount))
    if batchsize != 1:
        arg_list.append("--batch_size " + str(batchsize))
    if cfg != 4:
        arg_list.append("--scale_cfg " + str(cfg))
    if width != 720:
        arg_list.append("--width " + str(width))
    if height != 720:
        arg_list.append("--height " + str(height))
    if samplingMethod != 0:
        arg_list.append("--sampler_name " + str(sampler_index) )
    if seed != -1 and seed != "-1":
        arg_list.append("--seed " + str(seed))
    
    arg = " ".join(arg_list)
    print("arg created:", arg)
    return arg
















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
    entry_Prompts.insert(tk.END, "A photography of cover photo dark-haired woman, cold colors , beautiful , 3D rendering , realistic,  ultra close up , Sketch drawing style , Backlight, long hair, green eyes, japanese clothes")

    frame_part2 = tk.Frame(frame_gray)
    frame_part2.pack(fill=tk.X, pady=(10, 0))

    label_NegPrompts = tk.Label(frame_part2, text="Negative Prompts")
    label_NegPrompts.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche


    entry_NegPrompts = tk.Text(frame_part2, width=50, height=5)
    entry_NegPrompts.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
    entry_NegPrompts.bind("<KeyRelease>", lambda event: print("Negative Prompts : " + entry_NegPrompts.get("1.0", tk.END)))
    entry_NegPrompts.insert(tk.END, "cartoon,  illustration,  drawing,  painting,  digital art,  2D, CGI,  VFX")

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
    def send_request():
        prompt = entry_Prompts.get("1.0", tk.END)
        negPrompt = entry_NegPrompts.get("1.0", tk.END)
        steps = round(slider0.get())
        batchcount = round(slider1.get())
        batchsize = round(slider2.get())
        cfg = round(slider3.get())
        width = round(sliderw.get())
        height = round(sliderh.get())
        samplingMethod = dropdown.get()
        seed = entry_seed.get("1.0", tk.END)
        request_stable_diffusion(prompt, negPrompt, steps, batchcount, batchsize, cfg, width, height, samplingMethod, seed)




    button_send = tk.Button(frame_gray, text="Send Prompt", command=lambda: send_request())

    # button_send = tk.Button(frame_gray, text="Send Prompt", command=lambda: send_command_stablePrompt(create_arg(entry_Prompts.get("1.0", tk.END), entry_NegPrompts.get("1.0", tk.END), round(slider0.get()), round(slider1.get()), round(slider2.get()), round(slider3.get()), round(sliderw.get()), round(sliderh.get()), dropdown.get(), entry_seed.get("1.0", tk.END))))
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
    entry_folder.insert(tk.END, "../dir_stable_images")

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
    entry_output_folder.insert(tk.END, "../dir_face_capture")

    button_browse_output = tk.Button(frame_part1, text="Browse", command=browse_output_folder)
    button_browse_output.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 10))
   

    # Ajout de la liste déroulante
    label_Sampmethod = tk.Label(frame_green, text="Sampling method")
    label_Sampmethod.pack(pady=(10, 0))

    # Ajout du bouton SEND
    def start_face_capture():
        send_command_faceCapture(entry_folder.get(), entry_output_folder.get())


    button_send = tk.Button(frame_gray, text="Send Prompt", command=lambda: start_face_capture())
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
    entry_folder.insert(tk.END, "../dir_face_capture")

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
    entry_output_folder.insert(tk.END, "../dir_face_recognition")

    button_browse_output = tk.Button(frame_part1, text="Browse", command=browse_output_folder)
    button_browse_output.pack(side=tk.TOP, anchor='w', padx=(10, 0), pady=(5, 10))
   

    # Ajout de la liste déroulante
    label_Sampmethod = tk.Label(frame_green, text="Sampling method")
    label_Sampmethod.pack(pady=(10, 0))




    # Afficher le contenu du fichier JSON
    def get_json_content():
        with open("dir_face_recognition/result.json") as f:
            data = json.load(f)
            json_content = json.dumps(data, indent=4)
            return json_content


    # Ajouter les fonctions à appeler lors de l'exécution de la commande send_command_faceRecognition

    # Ajout du bouton SEND
    button_send = tk.Button(frame_gray, text="Send Prompt")
    button_send.configure(command=lambda: [send_command_faceRecognition(entry_folder.get(), entry_output_folder.get()), get_json_content()])

    button_send.pack(padx=10, pady=(45, 15), fill=tk.BOTH, expand=True)
    button_send.configure(height=1, width=15, bd=0, cursor="hand2")
    button_send.place(relx=0.5, rely=1, anchor=tk.S, width=200, height=50)








def correct_paths_in_json(file_path):
    # Lire le fichier JSON
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    corrected_data = {}
    
    for key, value in data.items():
        # Corriger le nom de l'image
        new_key = key.replace('_face_gray', '')
        
        # Corriger les matched_images
        new_matched_images = [img.replace('gallery\\', '').replace('_face_gray', '').replace('../dir_face_capture\\', '') for img in value['matched_images']]
        
        corrected_data[new_key] = {'matched_images': new_matched_images}
    
    # Écrire les données corrigées dans le fichier JSON
    with open(file_path, 'w') as file:
        json.dump(corrected_data, file, indent=4)
    
    print(f"Paths corrected and saved to {file_path}")



def display_photos(container, display_folder):
    # Supprimer les anciennes photos affichées
    for widget in container.winfo_children():
        widget.destroy()



    if (display_folder == "dir_face_recognition"):
        print("display_folder == -dir_face_recognition- start ")

        pathjson = "dir_face_recognition/result.json"
        correct_paths_in_json(pathjson)
        images_folder = "dir_stable_images"

        display_json_images2(container, pathjson, images_folder)
        return



    # Créer les frames pour la grande image et les petites images
    container2 = tk.Frame(container)
    container2.pack(fill="both", expand=True)

     # Frame pour la grande image
    large_image_frame = tk.Frame(container2)
    if (display_folder == "dir_stable_images"):
        large_image_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nw")

    # Frame pour les petites images avec scrollbar
    small_images_frame = tk.Frame(container2)
    small_images_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

    canvas = tk.Canvas(small_images_frame, width=420, height=410)
    if (display_folder == "dir_face_capture"):
        canvas.config(width=620, height=300)
    scrollbar = ttk.Scrollbar(small_images_frame, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Positionner le canvas et la scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Récupérer la liste des fichiers dans le dossier à afficher
    files = os.listdir(display_folder)
    files.sort()
    if(display_folder != "dir_face_capture"):
        # Afficher la dernière photo créée en plus gros
        if files:
            last_photo = files[-1]
            image = Image.open(os.path.join(display_folder, last_photo))
            image = image.resize((400, 400))  # Redimensionner l'image
            photo = ImageTk.PhotoImage(image)
            photo_label = tk.Label(large_image_frame, image=photo)
            photo_label.image = photo
            photo_label.grid(row=0, column=0, padx=10, pady=10)  # Afficher la grande image à gauche

            # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
            delete_button = tk.Button(large_image_frame, text="X", command=lambda: delete_photo(last_photo, display_folder))
            delete_button.grid(row=0, column=0, sticky="NE", padx=5, pady=5)

    # Afficher les quatre dernières petites photos
    countfile = 0
    for i, file in enumerate(reversed(files[:-1])):
        image = Image.open(os.path.join(display_folder, file))
        image = image.resize((200, 200))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(scroll_frame, image=photo)
        photo_label.image = photo
                
        # Calculer la position en grille pour les petites photos
        row = countfile // 2
        column = countfile % 2  # Ajuster pour qu'elles soient à droite de la grande photo
        photo_label.grid(row=row, column=column, padx=5, pady=5)
        if (display_folder == "dir_face_capture"):
            row = countfile // 3
            column = countfile % 3
            photo_label.grid(row=row, column=column, padx=5, pady=5)
       

        # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
        delete_button = tk.Button(scroll_frame, text="X", command=lambda file=file: delete_photo(file, display_folder), bg="red")
        delete_button.grid(row=row, column=column, sticky="NE", padx=5, pady=5)

        countfile += 1


def delete_photo(file, folder):
    # Supprimer le fichier de la photo
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print("del picture   :", file_path)




def display_json_images2(contenair, json_file, display_folder="dir_stable_images"):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Create a new frame to hold the images
    image_box = tk.Frame(contenair)
    image_box.pack(fill="both", expand=True)
    
    # Create a canvas and scrollbar to enable scrolling
    canvas = tk.Canvas(image_box, width=1020, height=460)
    scroll_y = ttk.Scrollbar(image_box, orient="vertical", command=canvas.yview)
    scroll_x = ttk.Scrollbar(image_box, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    canvas.config(width=1520, height=350)
    
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    
    chemin_actuel = os.getcwd()
    print("Le chemin actuel est :", chemin_actuel)
    # Load and display images
    row = 0
    for main_image_path, value in data.items():
        ref_image_path = os.path.join(display_folder, main_image_path)
        if(verifier_image(ref_image_path)):
            img = Image.open(ref_image_path)
            img = img.resize((120, 120), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            
            label = tk.Label(scrollable_frame, image=img)
            label.image = img  # Keep a reference to avoid garbage collection
            label.grid(row=row, column=0, padx=5, pady=5)

            # delete_button = tk.Button(scrollable_frame, text="X", command=lambda file=file: delete_photo(ref_image_path, canvas, display_folder), bg="red")
            # delete_button.grid(row=row, column=col, sticky="NE", padx=5, pady=5)
            
        # Load and display matched images
        col = 1
        for matched_image_path in value["matched_images"]:
            mtd_image_path = os.path.join(display_folder, matched_image_path)
            if(verifier_image(mtd_image_path) and mtd_image_path != ref_image_path):
                matched_img = Image.open(mtd_image_path)
                matched_img = matched_img.resize((100, 100), Image.ANTIALIAS)
                matched_img = ImageTk.PhotoImage(matched_img)
                
                matched_label = tk.Label(scrollable_frame, image=matched_img)
                matched_label.image = matched_img  # Keep a reference to avoid garbage collection
                matched_label.grid(row=row, column=col, padx=5, pady=5)
                 # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
                delete_button = tk.Button(scrollable_frame, text="X", command=lambda file=file: delete_photo(matched_image_path, display_folder), bg="red")
                delete_button.grid(row=row, column=col, sticky="NE", padx=5, pady=5)
            
                col += 1
        row += 1


import os

def verifier_image(path):
    if os.path.isfile(path):
        extension = os.path.splitext(path)[1]
        if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            print("l'image est introuvable  :", path)
            return True
    return False



def request_stable_diffusion(prompt, negative_prompt, steps, batch_count,  batch_size, scale_cfg, width, height, sampler_name, seed):
    url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'

    payload = {
        "sampler_index": sampler_name,
        "prompt": prompt,
        "negativeprompt": negative_prompt,
        "steps": steps,
        "batch_size": batch_size,
        "batch_count": batch_count,
        "cfg_scale": scale_cfg,
        "seed": seed,
        "width": width,
        "height": height
    }


    current_time = datetime.datetime.now()
    datecurrent = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    # print(datecurrent)
    x = requests.post(url, json=payload)
    if "error" in x.text:
        print(x.text)

    output_dir = "dir_stable_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    r = x.json()
    for i in enumerate(r["images"]):
        img_name = os.path.join(output_dir, f"{datecurrent}_{i[0]}.png")
        img = i[1].split(",",1)[0]
        image = Image.open(io.BytesIO(base64.b64decode(img)))
        image.save(img_name)

    print("Done!")