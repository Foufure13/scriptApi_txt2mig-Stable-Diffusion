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
parser.add_argument('--sampler_name', type=str, default='DPM++ 2M Karras', help='Sampler name')
parser.add_argument('--prompt', type=str, default='A photography of cover photo dark-haired woman, cold colors , beautiful , 3D rendering , realistic,  ultra close up , Sketch drawing style , Backlight, long hair, green eyes, japanese clothes', help='Prompt')
parser.add_argument('--NegativePrompt', type=str, default='cartoon,  illustration,  drawing,  painting,  digital art,  2D, CGI,  VFX', help='Negative prompt')
parser.add_argument('--steps', type=int, default=30, help='Number of steps')
parser.add_argument('--batch_size', type=int, default=1, help='Batch size')
parser.add_argument('--batch_count', type=int, default=1, help='Batch count')
parser.add_argument('--scale_cfg', type=int, default=4, help='Scale configuration')
parser.add_argument('--seed', type=int, default=-1, help='Seed')
parser.add_argument('--width', type=int, default=720, help='Image width')
parser.add_argument('--height', type=int, default=720, help='Image height')

args = parser.parse_args()

payload = {
    "sampler_name": args.sampler_name,
    "prompt": args.prompt,
    "NegativePrompt": args.NegativePrompt,
    "steps": args.steps,
    "batch_size": args.batch_size,
    "batch_count": args.batch_count,
    "scale_cfg": args.scale_cfg,
    "seed": args.seed,
    "width": args.width,
    "height": args.height
}

current_time = datetime.datetime.now()
datecurrent = current_time.strftime("%Y-%m-%d_%H-%M-%S")
# print(datecurrent)
x = requests.post(url, json=payload)

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

r = x.json()
for i in enumerate(r["images"]):
    img_name = os.path.join(output_dir, f"{datecurrent}_{i[0]}.png")
    img = i[1].split(",",1)[0]
    image = Image.open(io.BytesIO(base64.b64decode(img)))
    image.save(img_name)

print("Done!")

