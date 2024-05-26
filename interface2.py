import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import json
import subprocess
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image  # Import the Image module from the PIL package
from ttkbootstrap.widgets import Meter


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
        subprocess.Popen([script_path], cwd=sd_path, shell=True)
    else:
        print("Le script webui-user.bat n'a pas été trouvé dans le chemin donné.")
        return False

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

# Appeler la fonction pour vérifier/configurer le chemin
stable_diffusion_path = check_config()

# Vérifier le service web et exécuter le script si nécessaire
if stable_diffusion_path:
    service_url = "http://localhost:7860"  # Remplacez par l'URL de votre service web
    check_webservice_and_run_script(stable_diffusion_path, service_url)


def send_command():
    # Placeholder function for sending command
    print("Command sent")

def on_slider_change(event):
    # Placeholder function for slider change
    print("Slider value:", event)

def on_dropdown_change(event):
    # Placeholder function for dropdown change
    print("Dropdown value:", event)




# Création de la fenêtre principale
# root = tk.Tk()

# root.configure(bg="#1A62A7")  # Définit la couleur de fond de la fenêtre principale

root = ttk.Window(themename="superhero")
root.title("Interface test")





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
frame_gray = tk.Frame(root, bg="gray")
frame_gray.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_green = tk.Frame(root, bg="#1A62A7")
frame_green.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False, ipadx=20)


frame_blue = tk.Frame(root, bg="#509DA4")
frame_blue.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame_orange = tk.Frame(frame_gray, bg="orange")
frame_orange.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, pady=(0, 0))

label_blue = tk.Label(frame_blue, text="Résultat", bg="#509DA4")
label_blue.pack(pady=(10, 0))




# Partir 1
frame_part1 = tk.Frame(frame_gray, bg="gray")
frame_part1.pack(fill=tk.X, pady=(10, 0))

label_top1 = tk.Label(frame_part1, text="Prompts", bg="gray")
label_top1.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche

entry_top1 = tk.Entry(frame_part1, width=50)
entry_top1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5, ipady=25)  # La zone d'écriture en dessous du titre

# Partir 2
frame_part2 = tk.Frame(frame_gray, bg="gray")
frame_part2.pack(fill=tk.X, pady=(10, 0))

label_top2 = tk.Label(frame_part2, text="Negative Prompts", bg="gray")
label_top2.pack(side=tk.TOP, anchor='w', padx=(10))  # Aligne le titre à gauche

entry_top2 = tk.Entry(frame_part2, width=50)
entry_top2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5, ipady=25)





# Ajout des sliders
label_steps = tk.Label(frame_green, text="Sampling steps : 20", bg="#1A62A7")
label_steps.pack()
slider0 = ttk.Scale(frame_green, from_=1, to=150, length=100, command=lambda value: label_steps.config(text="Sampling steps : "+str(round(float(value)))))
slider0.pack(padx=10, pady=5)
slider0.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider0.get()))


label_batchcount = tk.Label(frame_green, text="Batch count : 1", bg="#1A62A7")
label_batchcount.pack(pady=(10, 0))
slider1 = ttk.Scale(frame_green, from_=1, to=100, length=100, command=lambda value: label_batchcount.config(text="Batch count : "+str(round(float(value)))))
slider1.pack(padx=10, pady=5)
slider1.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider1.get()))

label_batchsize = tk.Label(frame_green, text="Batch size : 1", bg="#1A62A7")
label_batchsize.pack(pady=(10, 0))
slider2 = ttk.Scale(frame_green, from_=1, to=8, length=100, command=lambda value: label_batchsize.config(text="Batch size : "+str(round(float(value)))))
slider2.pack(padx=10, pady=5)
slider2.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider2.get()))

label_cfg = tk.Label(frame_green, text="CFG Scale : 4", bg="#1A62A7")
label_cfg.pack(pady=(10, 0))
slider3 = ttk.Scale(frame_green, from_=1, to=100, length=100, command=lambda value: label_cfg.config(text="CFG Scale : "+str(round(float(value)))))
slider3.pack(padx=10, pady=5)
slider3.bind("<ButtonRelease-1>", lambda event: on_slider_change(slider3.get()))

# Ajout de la liste déroulante
options = ["Option 1", "Option 2", "Option 3"]
dropdown = ttk.Combobox(frame_green, values=options, width=15)
dropdown.pack(padx=10, pady=5)
dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_change(dropdown.get()))

# Ajout du bouton SEND
button_send = tk.Button(frame_orange, text="Send Prompt", command=send_command)
button_send.pack(padx=10, pady=5)

# Lancement de la boucle principale
root.mainloop()
