# Converte i fotogrammi PNG renderizzati in WebP leggeri per il sito.
# Uso: python3 blender/converti.py blender/out/hd public/sequenza
import os, sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
files = sorted(f for f in os.listdir(src) if f.endswith('.png'))
os.makedirs(os.path.join(dst, 'hd'), exist_ok=True)
os.makedirs(os.path.join(dst, 'sm'), exist_ok=True)
for i, f in enumerate(files):
    im = Image.open(os.path.join(src, f)).convert('RGB')
    hd = im.resize((1280, 720), Image.LANCZOS) if im.width != 1280 else im
    hd.save(os.path.join(dst, 'hd', f'f{i:03d}.webp'), 'WEBP', quality=72, method=6)
    im.resize((960, 540), Image.LANCZOS).save(os.path.join(dst, 'sm', f'f{i:03d}.webp'), 'WEBP', quality=68, method=6)
print(len(files), 'fotogrammi convertiti')
