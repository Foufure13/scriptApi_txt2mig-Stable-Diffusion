from scipy import linalg
import glob
import numpy as np
import argparse
import os
import json

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 11:20:01 2017
Updated on Sun Feb 05 15:41:07 2017
Updated on May 28 2024
@author: Marc Silanus
Note : Le dossier doit travail doit contenir 
- eigenfaces.py
- gallery : contient les photos de références
- a_tester : contient les photos des visages à identifier
- eingenfaces : Contiendra les eigenfaces
- reconst : Contiendra les essais de reconstruction
- reconst2 : Contiendra les essais de reconstruction avec un nombre limité d'eigenfaces
"""

import imageio.v2 as imageio
import matplotlib.pyplot as plt

def is_grayscale(image_path):
    img = imageio.imread(image_path)
    if len(img.shape) == 2:
        return True
    elif len(img.shape) == 3 and img.shape[2] == 1:
        return True
    else:
        return False

def load_images_from_folder(folder):
    pngs = glob.glob(os.path.join(folder, '*.png'))
    if not pngs:
        raise ValueError(f"No PNG images found in the folder: {folder}")
    for png in pngs:
        if not is_grayscale(png):
            raise ValueError(f"Image {png} is not in grayscale.")
    images = np.array([imageio.imread(i, mode='F').flatten() for i in pngs])
    return images, imageio.imread(pngs[0], mode='F').shape, pngs

def recognize_faces(gallery_folder, image_to_find):
    seuil = 6
    threshold = seuil*1000  

    if not is_grayscale(image_to_find):
        raise ValueError(f"Image {image_to_find} is not in grayscale.")

    # Create necessary directories if they don't exist
    os.makedirs("eigenfaces", exist_ok=True)
    os.makedirs("reconst", exist_ok=True)
    os.makedirs("reconst2", exist_ok=True)

    # Acquisition des images
    imgs, (heigh, length), img_paths = load_images_from_folder(gallery_folder)

    print(f"Dimensions des images : {heigh} x {length}")

    N = len(imgs)
    for i in range(N):
        print(f"imgs[{i}]={imgs[i]}")

    print(" --------------------------------")
    # Calcul, affichage et enregistrement de la moyenne des images 
    moyenne = np.mean(imgs, 0)
    print(f"moyenne={moyenne}")
    moyenne_image = moyenne.reshape(heigh, length)
    moyenne_image = ((moyenne_image - moyenne_image.min()) / (moyenne_image.max() - moyenne_image.min()) * 255).astype(np.uint8)
    imageio.imwrite("average.png", moyenne_image)

    phi = imgs - moyenne

    eigenfaces, sigma, v = linalg.svd(phi.transpose(), full_matrices=False)

    for i in range(eigenfaces.shape[1]):
        eigenface_image = ((eigenfaces[:, i].reshape(heigh, length) - eigenfaces[:, i].min()) / 
                           (eigenfaces[:, i].max() - eigenfaces[:, i].min()) * 255).astype(np.uint8)
        imageio.imwrite(f"eigenfaces/eigenfaces{i}.png", eigenface_image)

    weights = np.dot(phi, eigenfaces)

    results = {}

    for p in range(N):
        recon = moyenne + np.dot(weights[p, :15], eigenfaces[:, :15].T)
        img_id = f"{p}"
        recon_image = ((recon.reshape(heigh, length) - recon.min()) / 
                       (recon.max() - recon.min()) * 255).astype(np.uint8)
        imageio.imwrite(f"reconst2/img_{img_id}.png", recon_image)

        img2find = np.array(imageio.imread(image_to_find, mode='F').flatten())
        phi2 = img2find - moyenne
        w2 = np.dot(phi2, eigenfaces)
        dist = np.sqrt(np.sum((weights - w2) ** 2, axis=1))
        indices = np.where(dist <= threshold)[0]
        matched_images = [img_paths[i] for i in indices]
        results[os.path.basename(image_to_find)] = matched_images

    return results

def main(gallery_folder, images_folder):
    result = {}
    for image_file in os.listdir(images_folder):
        if image_file.endswith(".png"):
            image_path = os.path.join(images_folder, image_file)
            results_for_image = recognize_faces(gallery_folder, image_path)
            result.update(results_for_image)

    with open("result.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Result saved to result.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face Recognition using Eigenfaces")
    parser.add_argument('--gallery', type=str, required=True, help="Path to the gallery folder containing reference images.")
    parser.add_argument('--images_folder', type=str, required=True, help="Path to the folder containing images to recognize.")
    args = parser.parse_args()
    main(args.gallery, args.images_folder)
