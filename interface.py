import os
import tkinter as tk
from tkinter import ttk

def send_data(arg):
    os.system('python Api_txt2img.py'+arg)
    pass

# Créer la fenêtre principale
window = tk.Tk()
window.geometry("800x500")  # Ajustement de la taille de la fenêtre
window.title("Ma Interface")

# Créer la boîte pour les champs texte
text_box = tk.Frame(window, bg="grey", width=0.7*window.winfo_width(), height=300)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

text_label1 = tk.Label(text_box, text="Input 1:")
text_label1.pack()
text_input1 = tk.Entry(text_box)
text_input1.pack()

text_label2 = tk.Label(text_box, text="Input 2:")
text_label2.pack()
text_input2 = tk.Entry(text_box)
text_input2.pack()

# Créer la zone pour les sliders
slider_frame = tk.Frame(window, bg="maroon", width=0.1*window.winfo_width())
slider_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

slider_label = tk.Label(slider_frame, text="Slider:")
slider_label.pack()

slider = tk.Scale(slider_frame, from_=0, to=40, orient=tk.HORIZONTAL)
slider.pack(fill=tk.BOTH, expand=True)


slider_label = tk.Label(slider_frame, text="Slider:")
slider_label.pack()

slider2 = tk.Scale(slider_frame, from_=0, to=40, orient=tk.HORIZONTAL)
slider2.pack(fill=tk.BOTH, expand=True)


# Créer les autres éléments
dropdown_label = tk.Label(window, text="Dropdown:")
dropdown_label.pack()
dropdown_values = ['Option 1', 'Option 2', 'Option 3']
dropdown = ttk.Combobox(window, values=dropdown_values)
dropdown.pack()

# button = tk.Button(window, text='Send', command=send_data(""))
# button.pack()

# Create the button
button = tk.Button(window, text='Send', command=lambda: send_data(""))
button.pack()


# Créer la zone d'affichage d'image
image = tk.Label(window)
image.pack()

# Lancer la boucle principale
window.mainloop()
