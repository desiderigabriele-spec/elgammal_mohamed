# Scarica modelli 3D e HDRI CC0 di Poly Haven usati dalla scena.
# Uso: python3 blender/scarica_modelli.py
import json, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
MODELLI = ['Sofa_01', 'potted_plant_04', 'potted_plant_02', 'throw_pillows_01', 'side_table_01',
           'wooden_ladder_02', 'cement_bag', 'trashbag', 'trowel_01', 'plastic_crate_01', 'Drill_01', 'cardboard_box_01']
HDRI = ['piazza_bologni']

UA = {'User-Agent': 'scene-downloader/1.0'}

def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0: return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as r, open(path + '.part', 'wb') as f:
        f.write(r.read())
    os.replace(path + '.part', path)

def api(p):
    with urllib.request.urlopen(urllib.request.Request('https://api.polyhaven.com/' + p, headers=UA)) as r: return json.load(r)

crediti = {}
for m in MODELLI:
    b = api('files/' + m)['blend']['1k']['blend']
    d = os.path.join(HERE, 'modelli', m)
    get(b['url'], os.path.join(d, os.path.basename(b['url'])))
    for rel, inc in b.get('include', {}).items():
        get(inc['url'], os.path.join(d, rel))
    info = api('info/' + m); crediti[m] = {'autori': list(info.get('authors', {}).keys()), 'licenza': 'CC0', 'fonte': 'https://polyhaven.com/a/' + m}
    print('ok', m)
for h in HDRI:
    f = api('files/' + h)['hdri']['4k']['exr']
    get(f['url'], os.path.join(HERE, 'hdri', h + '_4k.exr'))
    info = api('info/' + h); crediti[h] = {'autori': list(info.get('authors', {}).keys()), 'licenza': 'CC0', 'fonte': 'https://polyhaven.com/a/' + h}
    print('ok', h)
json.dump(crediti, open(os.path.join(HERE, 'modelli', 'crediti.json'), 'w'), indent=1, ensure_ascii=False)
