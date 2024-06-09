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


def update_photos():
    global last_files
    display_folder = get_current_output_folder()
    current_files = set(os.listdir(display_folder))

    # Réinitialiser la vue pour afficher les nouvelles images
    if current_files != last_files:
        last_files = current_files
        display_photos(photo_frame, display_folder)
        

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

# # Démarrer la surveillance des nouveaux fichiers
root.after(10000, update_photos)

# Lancement de la boucle principale
root.mainloop()
