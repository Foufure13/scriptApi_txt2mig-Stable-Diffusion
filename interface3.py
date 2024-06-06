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

def display_photos(photo_frame, display_folder):
    # Supprimer les anciennes photos affichées
    for widget in photo_frame.winfo_children():
        widget.destroy()



    if (display_folder == "dir_face_recognition"):
        print("display_folder == -dir_face_recognition- start ")

        correct_paths_in_json("FaceReco/result.json")
        images_folder = "dir_stable_images"

            # Lire le fichier JSON
        with open("FaceReco/result.json", 'r') as file:
            data = json.load(file)

        # Créer une frame pour contenir le Canvas et la scrollbar
        container = ttk.Frame(photo_frame)
        container.pack(fill="both", expand=True)

        # Créer un Canvas
        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        # Ajouter une scrollbar verticale au Canvas
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configurer le Canvas pour utiliser la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Créer une frame à l'intérieur du Canvas pour contenir les images
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        row_index = 0  # Pour positionner les images en ligne
            
        for key, value in data.items():
            # Frame pour chaque ligne d'images
            line_frame = tk.Frame(container)
            line_frame.pack(fill="x", padx=5, pady=5)

            # Afficher la photo de référence en plus grande taille
            ref_image_path = os.path.join(images_folder, key)
            if os.path.exists(ref_image_path):
                ref_image = Image.open(ref_image_path)
                ref_image = ref_image.resize((200, 200))  # Taille de l'image de référence
                ref_photo = ImageTk.PhotoImage(ref_image)
                ref_photo_label = tk.Label(line_frame, image=ref_photo)
                ref_photo_label.image = ref_photo
                ref_photo_label.pack(side="left", padx=5, pady=5)
            
            # Afficher les matched_images à droite en taille normale
            for matched_image in value['matched_images']:
                matched_image_path = os.path.join(images_folder, matched_image)
                if os.path.exists(matched_image_path):
                    img = Image.open(matched_image_path)
                    img = img.resize((100, 100))  # Taille des images correspondantes
                    photo = ImageTk.PhotoImage(img)
                    photo_label = tk.Label(line_frame, image=photo)
                    photo_label.image = photo
                    photo_label.pack(side="left", padx=5, pady=5)
                    
        return





    # Créer les frames pour la grande image et les petites images
    container = tk.Frame(photo_frame)
    container.pack(fill="both", expand=True)

     # Frame pour la grande image
    large_image_frame = tk.Frame(container)
    if (display_folder == "dir_stable_images"):
        large_image_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nw")

    # Frame pour les petites images avec scrollbar
    small_images_frame = tk.Frame(container)
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
            delete_button = tk.Button(large_image_frame, text="X", command=lambda: delete_photo(last_photo, photo_frame, display_folder))
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
       

        # Ajouter le bouton croix pour supprimer la photo dans le coin haut droit
        delete_button = tk.Button(scroll_frame, text="X", command=lambda file=file: delete_photo(file, photo_frame, display_folder), bg="red")
        delete_button.grid(row=row, column=column, sticky="NE", padx=5, pady=5)

        countfile += 1

def delete_photo(file, photo_frame, folder):
    # Supprimer le fichier de la photo
    file_path = os.path.join(folder, file)
    os.remove(file_path)

    # Mettre à jour l'affichage des photos
    display_photos(photo_frame, folder)

def update_photos():
    global last_files
    display_folder = get_current_output_folder()
    current_files = set(os.listdir(display_folder))

    # Réinitialiser la vue pour afficher les nouvelles images
    if current_files != last_files:
        last_files = current_files
        display_photos(photo_frame, display_folder)
        
    root.after(10000, update_photos)

def get_current_output_folder():
    # Déterminer le dossier à afficher en fonction de l'onglet actif
    selected_tab = notebook.index(notebook.select())
    print("selected_tab --> " + str(selected_tab))
    if selected_tab == 0:
        return "dir_stable_images"
    elif selected_tab == 1:
        return "dir_face_capture"
    elif selected_tab == 2:
        return "dir_face_recognition"
    else:
        return "dir_stable_images"  # Valeur par défaut

def on_tab_change(event):
    update_photos()

# Création de la fenêtre principale
root = ttk.Window(themename="superhero")
root.title("Stable Diffusion Controller")

# Création d'un Notebook pour les onglets
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Créer les trois pages
page1 = ttk.Frame(notebook)
page2 = ttk.Frame(notebook)
page3 = ttk.Frame(notebook)

create_page_stablePrompt(page1)
create_page_faceCapture(page2)
create_page_faceRecognition(page3)

notebook.add(page1, text="Stable Prompt")
notebook.add(page2, text="Face Capture")
notebook.add(page3, text="Face Recognition")

# Ajouter un événement pour détecter le changement d'onglet
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

# -----------------------------------------------------------------
#---------------------------- RESULT ------------------------------
# -----------------------------------------------------------------

frame_blue = tk.Frame(root)
frame_blue.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Ajouter la zone d'affichage des photos
photo_frame = tk.Frame(frame_blue)
photo_frame.pack(padx=10, pady=5)

# Initialiser last_files avec les fichiers du dossier par défaut
last_files = set(os.listdir("dir_stable_images"))
display_photos(photo_frame, "dir_stable_images")
update_photos()

# Démarrer la surveillance des nouveaux fichiers
root.after(10000, update_photos)

# Lancement de la boucle principale
root.mainloop()
