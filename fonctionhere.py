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



def create_arg(prompt, negprompt, steps, batchcount, batchsize, cfg):
    prompt = prompt.replace("\n", "")
    negprompt = negprompt.replace("\n", "")

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
    
    arg = " ".join(arg_list)
    print("arg created:", arg)
    return arg



def display_photos(photo_frame):
    # Supprimer les anciennes photos affichées
    for widget in photo_frame.winfo_children():
        widget.destroy()

    # Récupérer la liste des fichiers dans le dossier output
    output_folder = "output"
    files = os.listdir(output_folder)
    files.sort()

    # Afficher la dernière photo créée en plus gros
    if files:
        last_photo = files[-1]
        image = Image.open(os.path.join(output_folder, last_photo))
        image = image.resize((400, 400))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(photo_frame, image=photo)
        photo_label.image = photo
        photo_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)  # Afficher la grande image à gauche

        # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
        delete_button = tk.Button(photo_frame, text="X", command=lambda: delete_photo(last_photo, photo_frame))
        delete_button.grid(row=0, column=0, sticky="NE", padx=5, pady=5)

    # Afficher les quatre dernières petites photos
    countfile = 0
    for i, file in enumerate(reversed(files[:-1])):
        if countfile >= 4:
            break
        image = Image.open(os.path.join(output_folder, file))
        image = image.resize((200, 200))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(photo_frame, image=photo)
        photo_label.image = photo

        # Calculer la position en grille pour les petites photos
        row = countfile // 2
        column = countfile % 2 + 1  # Décaler de 1 pour qu'elles soient à droite de la grande photo
        photo_label.grid(row=row, column=column, padx=5, pady=5)

        # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
        delete_button = tk.Button(photo_frame, text="X", command=lambda file=file: delete_photo(file, photo_frame), bg="red")
        delete_button.grid(row=row, column=column, sticky="NE", padx=5, pady=5)

        countfile += 1

def delete_photo(file, photo_frame):
    # Supprimer le fichier de la photo
    output_folder = "output"
    file_path = os.path.join(output_folder, file)
    os.remove(file_path)

    # Mettre à jour l'affichage des photos
    display_photos(photo_frame)
