import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Meter


def check_config():
    config_file = 'config.conf'
    path_to_sd = None

    # Vérifier si le fichier de configuration existe
    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            path_to_sd = config_data.get('stable_diffusion_path')

    if not path_to_sd or not os.path.isfile(os.path.join(path_to_sd, 'webui-user.bat')):
        # Créer la fenêtre pour entrer le chemin
        def save_path():
            entered_path = path_entry.get()
            if os.path.isfile(os.path.join(entered_path, 'webui-user.bat')):
                with open(config_file, 'w') as file:
                    json.dump({'stable_diffusion_path': entered_path}, file)
                messagebox.showinfo("Succès", "Le chemin a été validé et sauvegardé.")
                window.destroy()
            else:
                messagebox.showerror("Erreur", "Le fichier 'webui-user.bat' n'a pas été trouvé dans le chemin donné.")

        window = ttk.Window(themename="superhero")
        window.title("Entrer le chemin de Stable Diffusion")

        label = ttk.Label(window, text="Entrez le chemin vers Stable Diffusion :")
        label.pack(pady=10)

        path_entry = ttk.Entry(window, width=50)
        path_entry.pack(pady=5)

        validate_button = ttk.Button(window, text="Valider", command=save_path, bootstyle=SUCCESS)
        validate_button.pack(pady=20)

        window.mainloop()
    else:
        print("Chemin de Stable Diffusion trouvé :", path_to_sd)
        return path_to_sd
    

def check_webservice_and_run_script(sd_path, url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("Le service web est actif.")
            return True
        else:
            print("Le service web a répondu avec un code de statut non 200.")
    except requests.RequestException:
        print("Le service web n'est pas actif.")

    # Exécuter le script si le service web n'est pas actif
    script_path = os.path.join(sd_path, 'webui-user.bat')
    if os.path.isfile(script_path):
        print("Exécution du script webui-user.bat...")
        # subprocess.Popen([script_path], cwd=sd_path, shell=True)
    else:
        print("Le script webui-user.bat n'a pas été trouvé dans le chemin donné.")
        return False
