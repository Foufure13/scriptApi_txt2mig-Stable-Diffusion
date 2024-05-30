import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import json
import subprocess
import requests
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the Image module from the PIL package
from ttkbootstrap.widgets import Meter



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



def display_photos(photo_frame):
    # Supprimer les anciennes photos affichées
    for widget in photo_frame.winfo_children():
        widget.destroy()

    # Créer les frames pour la grande image et les petites images
    main_frame = tk.Frame(photo_frame)
    main_frame.pack(fill="both", expand=True)

    # Frame pour la grande image
    large_image_frame = tk.Frame(main_frame)
    large_image_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nw")

    # Frame pour les petites images avec scrollbar
    small_images_frame = tk.Frame(main_frame)
    small_images_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

    canvas = tk.Canvas(small_images_frame, width=420, height=410)
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

    # Récupérer la liste des fichiers dans le dossier output
    output_folder = "dir_stable_images"
    files = os.listdir(output_folder)
    files.sort()

    # Afficher la dernière photo créée en plus gros
    if files:
        last_photo = files[-1]
        image = Image.open(os.path.join(output_folder, last_photo))
        image = image.resize((400, 400))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(large_image_frame, image=photo)
        photo_label.image = photo
        photo_label.grid(row=0, column=0, padx=10, pady=10)  # Afficher la grande image à gauche

        # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
        delete_button = tk.Button(large_image_frame, text="X", command=lambda: delete_photo(last_photo, photo_frame))
        delete_button.grid(row=0, column=0, sticky="NE", padx=5, pady=5)

    # Afficher les quatre dernières petites photos
    countfile = 0
    for i, file in enumerate(reversed(files[:-1])):
        image = Image.open(os.path.join(output_folder, file))
        image = image.resize((200, 200))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(scroll_frame, image=photo)
        photo_label.image = photo

        # Calculer la position en grille pour les petites photos
        row = countfile // 2
        column = countfile % 2  # Ajuster pour qu'elles soient à droite de la grande photo
        photo_label.grid(row=row, column=column, padx=5, pady=5)

        # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
        delete_button = tk.Button(scroll_frame, text="X", command=lambda file=file: delete_photo(file, photo_frame), bg="red")
        delete_button.grid(row=row, column=column, sticky="NE", padx=5, pady=5)

        countfile += 1





def delete_photo(file, photo_frame):
    # Supprimer le fichier de la photo
    output_folder = "dir_stable_images"
    file_path = os.path.join(output_folder, file)
    os.remove(file_path)

    # Mettre à jour l'affichage des photos
    display_photos(photo_frame)
