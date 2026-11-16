# Prova Blender: un muro che mostra gli strati del lavoro, da sinistra a destra.
# Uso: blender -b -P blender/test_muro.py -- <uscita.png> [campioni] [larghezza]
import bpy, bmesh, math, random, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = argv[0] if argv else '/tmp/test_muro.png'
SAMPLES = int(argv[1]) if len(argv) > 1 else 64
W = int(argv[2]) if len(argv) > 2 else 960
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene

# ---------- materiali ----------
def mat(name, color, rough=0.8, bump=0.0, bump_scale=40.0, noise_col=0.0, scale_col=8.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links
    bsdf = n['Principled BSDF']
    bsdf.inputs['Roughness'].default_value = rough
    if noise_col > 0:
        tex = n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = scale_col; tex.inputs['Detail'].default_value = 6
        ramp = n.new('ShaderNodeValToRGB')
        c0 = [max(0, c * (1 - noise_col)) for c in color[:3]] + [1]
        c1 = [min(1, c * (1 + noise_col * 0.6)) for c in color[:3]] + [1]
        ramp.color_ramp.elements[0].color = c0; ramp.color_ramp.elements[1].color = c1
        l.new(tex.outputs['Fac'], ramp.inputs['Fac']); l.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    else:
        bsdf.inputs['Base Color'].default_value = color
    if bump > 0:
        nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = bump_scale; nz.inputs['Detail'].default_value = 8
        bp = n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.002
        l.new(nz.outputs['Fac'], bp.inputs['Height']); l.new(bp.outputs['Normal'], bsdf.inputs['Normal'])
    return m

M_BRICK = [mat(f'mattone{i}', (0.42 + random.uniform(-.05, .05), 0.17 + random.uniform(-.03, .03), 0.09, 1), 0.85, bump=0.35, bump_scale=60, noise_col=0.25, scale_col=20) for i in range(4)]
M_MALTA = mat('malta', (0.55, 0.53, 0.5, 1), 0.95, bump=0.4, bump_scale=120, noise_col=0.15, scale_col=40)
M_INTONACO = mat('intonaco', (0.30, 0.30, 0.29, 1), 0.95, bump=0.5, bump_scale=30, noise_col=0.12, scale_col=6)
M_RASATURA = mat('rasatura', (0.70, 0.70, 0.68, 1), 0.6, bump=0.05, bump_scale=8, noise_col=0.04, scale_col=3)
M_PITTURA = mat('pittura', (0.80, 0.74, 0.62, 1), 0.75, bump=0.02, bump_scale=200)
M_PAV = mat('pavimento', (0.36, 0.35, 0.33, 1), 0.7, bump=0.15, bump_scale=15, noise_col=0.2, scale_col=2)
M_STANZA = mat('stanza', (0.78, 0.77, 0.74, 1), 0.8)
M_INFISSO = mat('infisso', (0.15, 0.16, 0.17, 1), 0.4)

def box(name, loc, size, m):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m); return o

# ---------- muro con gli strati (asse X, faccia verso -Y) ----------
H, T = 2.7, 0.12              # altezza, spessore mattone
ZONE = [0.0, 1.6, 3.0, 4.3, 5.6]  # mattoni | intonaco | rasatura | pittura
# malta di fondo dietro i mattoni (per tutta la lunghezza)
box('malta', (ZONE[-1] / 2, T / 2, H / 2), (ZONE[-1], T * 0.92, H), M_MALTA)
# mattoni veri, con giunti
bw, bh, g = 0.25, 0.085, 0.012
row = 0; z = 0.0
while z < H - 0.01:
    off = (bw + g) / 2 if row % 2 else 0
    x = -off
    while x < ZONE[1] + bw:
        x0, x1 = max(x, 0), min(x + bw, ZONE[-1])
        if x1 - x0 > 0.03 and x0 < ZONE[1] + 0.02:
            b = box('m', ((x0 + x1) / 2, T / 2 - 0.004 + random.uniform(-.002, .002), z + bh / 2), (x1 - x0, T, bh), random.choice(M_BRICK))
            b.rotation_euler[2] = random.uniform(-0.004, 0.004)
        x += bw + g
    z += bh + g; row += 1
# sotto gli strati la muratura continua: la copriamo con le finiture
inton = box('intonaco', ((ZONE[1] + ZONE[-1]) / 2, -0.008, H / 2), (ZONE[-1] - ZONE[1], 0.018, H), M_INTONACO)
ras = box('rasatura', ((ZONE[2] + ZONE[-1]) / 2, -0.0185, H / 2), (ZONE[-1] - ZONE[2], 0.004, H), M_RASATURA)
pit = box('pittura', ((ZONE[3] + ZONE[-1]) / 2, -0.0210, H / 2), (ZONE[-1] - ZONE[3], 0.0012, H), M_PITTURA)

# ---------- stanza ----------
box('pavimento', (2.8, -2.5, -0.01), (9, 7, 0.02), M_PAV)
box('soffitto', (2.8, -2.5, H + 0.06), (9, 7, 0.12), M_STANZA)
# parete destra
box('parete_dx', (ZONE[-1] + 0.06, -2.5, H / 2), (0.12, 7, H), M_STANZA)
# parete sinistra con finestra (4 pezzi attorno al vano)
wx = -0.06; y0, y1, z0, z1 = -2.6, -1.0, 0.9, 2.4
box('sx_a', (wx, (-6 + y0) / 2, H / 2), (0.12, abs(-6 - y0), H), M_STANZA)
box('sx_b', (wx, (y1 + 0.0) / 2, H / 2), (0.12, abs(y1), H), M_STANZA)
box('sx_c', (wx, (y0 + y1) / 2, z0 / 2), (0.12, y1 - y0, z0), M_STANZA)
box('sx_d', (wx, (y0 + y1) / 2, (z1 + H) / 2), (0.12, y1 - y0, H - z1), M_STANZA)
box('infisso', (wx, (y0 + y1) / 2, z0 + 0.02), (0.14, y1 - y0, 0.04), M_INFISSO)
box('montante', (wx, (y0 + y1) / 2, (z0 + z1) / 2), (0.14, 0.05, z1 - z0), M_INFISSO)

# ---------- luce ----------
world = bpy.data.worlds.new('mondo'); scn.world = world; world.use_nodes = True
sky = world.node_tree.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA'
sky.sun_elevation = math.radians(24); sky.sun_rotation = math.radians(250); sky.sun_intensity = 0.6
bg = world.node_tree.nodes['Background']; bg.inputs['Strength'].default_value = 0.35
world.node_tree.links.new(sky.outputs['Color'], bg.inputs['Color'])
sun = bpy.data.lights.new('sole', 'SUN'); sun.energy = 4.0; sun.angle = math.radians(1.5); sun.color = (1.0, 0.93, 0.82)
so = bpy.data.objects.new('sole', sun); scn.collection.objects.link(so)
so.rotation_euler = (math.radians(62), 0, math.radians(-112))
# luce di riempimento morbida dalla stanza
fill = bpy.data.lights.new('riempimento', 'AREA'); fill.energy = 40; fill.size = 4; fill.color = (0.9, 0.93, 1.0)
fo = bpy.data.objects.new('riempimento', fill); scn.collection.objects.link(fo)
fo.location = (2.8, -5.5, 2.3); fo.rotation_euler = (math.radians(80), 0, 0)

# ---------- camera ----------
cam = bpy.data.cameras.new('cam'); cam.lens = 28
co = bpy.data.objects.new('cam', cam); scn.collection.objects.link(co); scn.camera = co
co.location = (5.2, -2.6, 1.35)
target = Vector((2.0, 0, 1.2))
co.rotation_euler = (target - co.location).to_track_quat('-Z', 'Y').to_euler()

# ---------- render ----------
scn.render.engine = 'CYCLES'
scn.cycles.device = 'CPU'; scn.cycles.samples = SAMPLES; scn.cycles.use_denoising = False
try: scn.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
scn.render.resolution_x = W; scn.render.resolution_y = int(W * 9 / 16); scn.render.resolution_percentage = 100
scn.view_settings.view_transform = 'AgX' if 'AgX' in [i.name for i in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
scn.view_settings.look = 'None'
scn.view_settings.exposure = -0.6
scn.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print('RENDER OK', OUT)
