import requests
import io
import base64
import json
from PIL import Image, PngImagePlugin
import datetime
import os
import argparse


url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'

parser = argparse.ArgumentParser(description='API txt2img script')
parser.add_argument('--sampler_name', type=int, default='DPM++ 2M Karras', help='Sampler name')
parser.add_argument('--prompt', type=str, required=True, help='Prompt')
parser.add_argument('--NegativePrompt', type=str, default='', help='Negative prompt')
parser.add_argument('--steps', type=int, default=30, help='Number of steps')
parser.add_argument('--batch_size', type=int, default=1, help='Batch size')
parser.add_argument('--batch_count', type=int, default=1, help='Batch count')
parser.add_argument('--scale_cfg', type=int, default=4, help='Scale configuration')
parser.add_argument('--seed', type=int, default=-1, help='Seed')
parser.add_argument('--width', type=int, default=720, help='Image width')
parser.add_argument('--height', type=int, default=720, help='Image height')

args = parser.parse_args()

sampler_name_list = ['DPM++ 2M Karras','DPM++ SDE Karras','DPM++ 2M SDE Exponential','DPM++ 2M SDE Karras', 'Euler a','Euler', 'LMS', 'Heun', 'DPM2', 'DPM2 a' ,'DPM++ 2S a','DPM++ 2M','DPM++ SDE','DPM++ 2M SDE','DPM++ 2M SDE Heun','DPM++ 2M SDE Heun Karras','DPM++ 2M SDE Heun Exponential','DPM++ 3M SDE','DPM++ 3M SDE Karras','DPM++ 3M SDE Exponential','DPM fast','DPM adaptive','LMS Karras','DPM2 Karras','DPM2 a Karras','DPM2 a Karras','DPM++ 2S a Karras','Restart','DDIM','PLMS','UniPC',]
sampler_name = sampler_name_list[args.sampler_name]

payload = {
    "sampler_index": sampler_name,
    "prompt": args.prompt,
    "negativeprompt": args.NegativePrompt,
    "steps": args.steps,
    "batch_size": args.batch_size,
    "batch_count": args.batch_count,
    "cfg_scale": args.scale_cfg,
    "seed": args.seed,
    "width": args.width,
    "height": args.height
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

