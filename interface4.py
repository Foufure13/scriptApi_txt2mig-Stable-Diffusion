import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import io
import datetime
import base64
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

class StableDiffusionController:
    def __init__(self, root):
        self.root = root
        self.last_files = set()
        
        # Appeler la fonction pour vérifier/configurer le chemin
        self.stable_diffusion_path = check_config()
        
        # Vérifier le service web et exécuter le script si nécessaire
        if self.stable_diffusion_path:
            self.service_url = "http://localhost:7860"  # Remplacez par l'URL de votre service web
            check_webservice_and_run_script(self.stable_diffusion_path, self.service_url)
        
        self.setup_ui()
        self.update_photos()
        self.root.after(10000, self.update_photos)
        
    def setup_ui(self):
        self.root.title("Stable Diffusion Controller")
        
        # Création d'un Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Créer les trois pages
        self.page1 = ttk.Frame(self.notebook)
        self.page2 = ttk.Frame(self.notebook)
        self.page3 = ttk.Frame(self.notebook)
        
        create_page_stablePrompt(self.page1)
        create_page_faceCapture(self.page2)
        create_page_faceRecognition(self.page3)
        
        self.notebook.add(self.page1, text="Stable Prompt")
        self.notebook.add(self.page2, text="Face Capture")
        self.notebook.add(self.page3, text="Face Recognition")
        
        # Ajouter un événement pour détecter le changement d'onglet
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # -----------------------------------------------------------------
        #---------------------------- RESULT ------------------------------
        # -----------------------------------------------------------------
        
        frame_blue = tk.Frame(self.root)
        frame_blue.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Ajouter la zone d'affichage des photos
        self.photo_frame = tk.Frame(frame_blue)
        self.photo_frame.pack(padx=10, pady=5)
        
        # Initialiser last_files avec les fichiers du dossier par défaut
        self.last_files = set(os.listdir("dir_stable_images"))
        display_photos(self.photo_frame, "dir_stable_images")
    
    def update_photos(self):
        display_folder = self.get_current_output_folder()
        current_files = set(os.listdir(display_folder))
        
        # Réinitialiser la vue pour afficher les nouvelles images
        if current_files != self.last_files:
            self.last_files = current_files
            display_photos(self.photo_frame, display_folder)
            
    def get_current_output_folder(self):
        # Déterminer le dossier à afficher en fonction de l'onglet actif
        selected_tab = self.notebook.index(self.notebook.select())
        print("selected_tab --> " + str(selected_tab))
        if selected_tab == 0:
            return "dir_stable_images"
        elif selected_tab == 1:
            return "dir_face_capture"
        elif selected_tab == 2:
            return "dir_face_recognition"
        else:
            return "dir_stable_images"  # Valeur par défaut
        
    def on_tab_change(self, event):
        self.update_photos()



    
def main():
    root = ttk.Window(themename="superhero")
    app = StableDiffusionController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
