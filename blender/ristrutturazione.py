# Scena Blender: una stanza di un appartamento anni '60 che passa da vecchia a finita.
# Camera ferma. 8 fasi, una per servizio di El Gammal. Texture CC0 di Poly Haven in blender/tex.
#
# Uso:
#   blender -b -P blender/ristrutturazione.py -- --out DIR [--frames 0-199] [--step 1]
#           [--w 1280] [--samples 64] [--frame-list 10,40,70]
import bpy, math, os, random, sys
from mathutils import Vector

# ------------------------------------------------------------------ argomenti
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
OUT = arg('--out', '/tmp/ristr')
FR = arg('--frames', '0-199')
STEP = int(arg('--step', '1'))
W = int(arg('--w', '1280'))
SAMPLES = int(arg('--samples', '64'))
FLIST = arg('--frame-list', '')
ASPECT = arg('--aspect', '16:9')
HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'tex')
random.seed(11)

# ------------------------------------------------------------------ fasi (fotogrammi)
# 0 sopralluogo | 1 si comincia | 2 muratura | 3 impianti | 4 intonaci | 5 cartongesso | 6 rasatura | 7 casa tua
P = {
    'p0': (0, 15), 'p1': (16, 39), 'p2': (40, 71), 'p3': (72, 95),
    'p4': (96, 119), 'p5': (120, 143), 'p6': (144, 163), 'p7': (164, 199),
}
FEND = 199

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.frame_start, scn.frame_end = 0, FEND

# ------------------------------------------------------------------ utilità
def key_hide(o, visible_from=None, hidden_from=None):
    """Visibilità per fotogramma: compare da visible_from, sparisce da hidden_from."""
    def setk(f, hide):
        o.hide_render = hide; o.hide_viewport = hide
        o.keyframe_insert('hide_render', frame=f); o.keyframe_insert('hide_viewport', frame=f)
    if visible_from is not None:
        setk(0, True); setk(visible_from, False)
    else:
        setk(0, False)
    if hidden_from is not None:
        setk(hidden_from, True)
    for fc in (o.animation_data.action.fcurves if o.animation_data and o.animation_data.action else []):
        for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'

def key_value(socket, pairs):
    for f, v in pairs:
        socket.default_value = v; socket.keyframe_insert('default_value', frame=f)

def smooth_keys(id_data):
    ad = id_data.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points:
                if kp.interpolation != 'CONSTANT': kp.interpolation = 'BEZIER'; kp.easing = 'EASE_IN_OUT'

def img(path, non_color=False):
    full = os.path.join(TEX, path)
    if not os.path.exists(full): return None
    im = bpy.data.images.load(full, check_existing=True)
    if non_color: im.colorspace_settings.name = 'Non-Color'
    return im

def tex_set(nt, name, scale, coord_out, x=-900):
    """Nodi immagine (colore, rugosità, normale) per un materiale Poly Haven."""
    n, l = nt.nodes, nt.links
    mp = n.new('ShaderNodeMapping'); mp.location = (x - 250, 0)
    mp.inputs['Scale'].default_value = (1 / scale, 1 / scale, 1 / scale)
    l.new(coord_out, mp.inputs['Vector'])
    out = {}
    for kind, nc in (('diff', False), ('rough', True), ('nor', True)):
        im = img(f'{name}_{kind}.jpg', nc)
        if im is None: out[kind] = None; continue
        t = n.new('ShaderNodeTexImage'); t.image = im; t.location = (x, 0)
        l.new(mp.outputs['Vector'], t.inputs['Vector']); out[kind] = t.outputs['Color']
    return out

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree

# ------------------------------------------------------------------ materiale a strati con "passata"
def layered_material(name, layers, tex_scale_m=1.0, base_transparent=False, rough_add=0.0):
    """layers: lista di (nome_texture o colore, fotogramma_inizio, fotogramma_fine, tinta)
    Ogni strato copre il precedente con una passata lungo la lunghezza della superficie (coordinata Generated X)."""
    m, nt = new_mat(name); n, l = nt.nodes, nt.links
    bsdf = n['Principled BSDF']; out = n['Material Output']
    tc = n.new('ShaderNodeTexCoord'); tc.location = (-1600, 0)
    sep = n.new('ShaderNodeSeparateXYZ'); l.new(tc.outputs['Generated'], sep.inputs['Vector'])
    # irregolarità del bordo della passata (come una spatola)
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6; l.new(tc.outputs['Generated'], nz.inputs['Vector'])
    jit = n.new('ShaderNodeMath'); jit.operation = 'MULTIPLY_ADD'
    l.new(nz.outputs['Fac'], jit.inputs[0]); jit.inputs[1].default_value = 0.08; l.new(sep.outputs['X'], jit.inputs[2])
    col = rough = nor = None; alpha = None
    for i, (tname, f0, f1, tint) in enumerate(layers):
        if isinstance(tname, tuple):
            c = n.new('ShaderNodeRGB'); c.outputs[0].default_value = tname
            rg = n.new('ShaderNodeRGB'); rg.outputs[0].default_value = (0.82, 0.82, 0.82, 1)   # pittura opaca
            fn = n.new('ShaderNodeRGB'); fn.outputs[0].default_value = (0.5, 0.5, 1.0, 1)      # superficie liscia
            t = {'diff': c.outputs[0], 'rough': rg.outputs[0], 'nor': fn.outputs[0]}
        else:
            t = tex_set(nt, tname, tex_scale_m, tc.outputs['Object'], x=-900 - i * 60)
        tcol = t['diff']
        if tint is not None and tcol is not None:
            mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
            l.new(tcol, mx.inputs['A']); mx.inputs['B'].default_value = tint; tcol = mx.outputs['Result']
        if i == 0:
            col, rough, nor = tcol, t['rough'], t['nor']; continue
        # fattore della passata: 0 prima, 1 dopo; il bordo scorre da -0.2 a 1.2
        edge = n.new('ShaderNodeValue'); key_value(edge.outputs[0], [(f0, -0.25), (f1, 1.25)])
        sub = n.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'
        l.new(edge.outputs[0], sub.inputs[0]); l.new(jit.outputs[0], sub.inputs[1])
        fac = n.new('ShaderNodeMath'); fac.operation = 'MULTIPLY'; fac.use_clamp = True
        l.new(sub.outputs[0], fac.inputs[0]); fac.inputs[1].default_value = 40
        def mixc(a, b, data='RGBA'):
            if a is None: return b
            if b is None: return a
            mx = n.new('ShaderNodeMix'); mx.data_type = data
            l.new(fac.outputs[0], mx.inputs['Factor']); l.new(a, mx.inputs['A' if data == 'RGBA' else 2]); l.new(b, mx.inputs['B' if data == 'RGBA' else 3])
            return mx.outputs['Result' if data == 'RGBA' else 0]
        col = mixc(col, tcol); rough = mixc(rough, t['rough']); nor = mixc(nor, t['nor'])
        if base_transparent and i == 1: alpha = fac.outputs[0]
    l.new(col, bsdf.inputs['Base Color'])
    if rough is not None:
        rr = n.new('ShaderNodeSeparateColor'); l.new(rough, rr.inputs[0])
        ra = n.new('ShaderNodeMath'); ra.operation = 'ADD'; ra.use_clamp = True; ra.inputs[1].default_value = rough_add
        l.new(rr.outputs[0], ra.inputs[0]); l.new(ra.outputs[0], bsdf.inputs['Roughness'])
    if nor is not None:
        nm = n.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.8
        l.new(nor, nm.inputs['Color']); l.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
    if alpha is not None:
        l.new(alpha, bsdf.inputs['Alpha'])
    for nd in nt.nodes:
        if nd.bl_idname == 'ShaderNodeValue': pass
    return m

def simple_mat(name, color, rough=0.6, metal=0.0, emit=None):
    m, nt = new_mat(name); b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = color; b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emit is not None:
        b.inputs['Emission Color'].default_value = emit[0]; b.inputs['Emission Strength'].default_value = emit[1]
    return m

def tex_mat(name, tname, scale, tint=None, rough_mult=1.0):
    m, nt = new_mat(name); n, l = nt.nodes, nt.links; b = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); t = tex_set(nt, tname, scale, tc.outputs['Object'])
    c = t['diff']
    if tint is not None and c is not None:
        mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1
        l.new(c, mx.inputs['A']); mx.inputs['B'].default_value = tint; c = mx.outputs['Result']
    if c is not None: l.new(c, b.inputs['Base Color'])
    elif tint is not None: b.inputs['Base Color'].default_value = tint
    if t['rough'] is not None:
        rr = n.new('ShaderNodeSeparateColor'); l.new(t['rough'], rr.inputs[0])
        mm = n.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.use_clamp = True; mm.inputs[1].default_value = rough_mult
        l.new(rr.outputs[0], mm.inputs[0]); l.new(mm.outputs[0], b.inputs['Roughness'])
    if t['nor'] is not None:
        nm = n.new('ShaderNodeNormalMap'); l.new(t['nor'], nm.inputs['Color']); l.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m

def fabric_mat(name, color, scale=0.4):
    m, nt = new_mat(name); n, l = nt.nodes, nt.links; b = n['Principled BSDF']
    b.inputs['Base Color'].default_value = color; b.inputs['Roughness'].default_value = 0.95
    b.inputs['Sheen Weight'].default_value = 0.1
    tc = n.new('ShaderNodeTexCoord'); t = tex_set(nt, 'rough_linen', scale, tc.outputs['Object'])
    if t['nor'] is not None:
        nm = n.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.6
        l.new(t['nor'], nm.inputs['Color']); l.new(nm.outputs['Normal'], b.inputs['Normal'])
    return m

def fade_material(m, f_in=None, f_out=None):
    """Dissolvenza dell'oggetto tramite alpha (entrata e/o uscita)."""
    b = m.node_tree.nodes['Principled BSDF']; pairs = []
    if f_in: pairs += [(f_in[0], 0.0), (f_in[1], 1.0)]
    else: pairs += [(0, 1.0)]
    if f_out: pairs += [(f_out[0], 1.0), (f_out[1], 0.0)]
    key_value(b.inputs['Alpha'], pairs)

# ------------------------------------------------------------------ geometria
def box(name, loc, size, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if m: o.data.materials.append(m)
    if bevel > 0:
        md = o.modifiers.new('bev', 'BEVEL'); md.width = bevel; md.segments = 3
    return o

def plane(name, center, size, rot, m):
    """Piano con X locale lungo la lunghezza (per la passata) e Y locale lungo l'altezza."""
    bpy.ops.mesh.primitive_plane_add(location=center)
    o = bpy.context.object; o.name = name
    o.scale = (size[0] / 2, size[1] / 2, 1); o.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True, rotation=False)
    o.data.materials.append(m)
    return o

def cyl(name, loc, r, depth, rot, m, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); return o

# ------------------------------------------------------------------ stanza
RW, RD, RH = 4.6, 5.2, 2.8           # larghezza (x), profondità (y), altezza (z)
WIN_X0, WIN_X1, WIN_Z0, WIN_Z1 = 1.25, 2.95, 0.85, 2.45  # finestra sulla parete di fondo
TX = 3.35                             # tramezzo nuovo: x costante, da y=2.7 alla parete di fondo
TY0, TY1 = 2.7, RD
DOOR_Y0, DOOR_Y1, DOOR_H = 3.15, 4.0, 2.1

# materiale delle pareti esistenti: carta da parati -> intonaco rovinato -> intonaco grigio -> rasatura -> pittura
WALL_LAYERS = [
    ('decrepit_wallpaper', 0, 0, None),
    ('damaged_plaster', P['p1'][0], P['p1'][0] + 18, None),
    ('grey_plaster', P['p4'][0], P['p4'][1] - 2, (0.78, 0.78, 0.78, 1)),
    ((0.74, 0.74, 0.73, 1), P['p6'][0], P['p6'][1] - 2, None),
    ((0.84, 0.8, 0.73, 1), P['p7'][0], P['p7'][0] + 14, None),
]
M_WALL_BACK = layered_material('parete_fondo', WALL_LAYERS, 2.9)
M_WALL_LEFT = layered_material('parete_sx', WALL_LAYERS, 2.9)
M_WALL_RIGHT = layered_material('parete_dx', WALL_LAYERS, 2.9)
M_WALL_FRONT = layered_material('parete_fronte', WALL_LAYERS, 2.9)
# tramezzo nuovo: niente -> intonaco -> rasatura -> pittura (trasparente finché non arriva l'intonaco)
NEW_LAYERS = [
    ((0.5, 0.5, 0.5, 1), 0, 0, None),
    ('grey_plaster', P['p4'][0] + 4, P['p4'][1], (0.78, 0.78, 0.78, 1)),
    ((0.74, 0.74, 0.73, 1), P['p6'][0] + 2, P['p6'][1], None),
    ((0.84, 0.8, 0.73, 1), P['p7'][0], P['p7'][0] + 14, None),
]
M_TRAMEZZO = layered_material('tramezzo_finitura', NEW_LAYERS, 1.6, base_transparent=True)
# soffitto vecchio: intonaco macchiato -> bianco
M_CEIL = layered_material('soffitto', [
    ('white_plaster_02', 0, 0, (0.78, 0.74, 0.66, 1)),
    ((0.76, 0.76, 0.75, 1), P['p6'][0], P['p6'][1], None),
    ((0.86, 0.84, 0.8, 1), P['p7'][0], P['p7'][0] + 14, None),
], 3.0)
# pavimento: graniglia -> parquet
M_FLOOR = layered_material('pavimento', [
    ('terrazzo_tiles', 0, 0, None),
    ('laminate_floor_02', P['p7'][0] + 6, P['p7'][0] + 24, None),
], 2.0, rough_add=0.1)

# struttura (gusci) delle pareti, invisibili dall'interno ma servono a chiudere la luce
M_SHELL = simple_mat('guscio', (0.5, 0.5, 0.5, 1), 0.9)
T = 0.25
box('guscio_fondo_a', (WIN_X0 / 2, RD + T / 2, RH / 2), (WIN_X0, T, RH), M_SHELL)
box('guscio_fondo_b', ((WIN_X1 + RW) / 2, RD + T / 2, RH / 2), (RW - WIN_X1, T, RH), M_SHELL)
box('guscio_fondo_c', ((WIN_X0 + WIN_X1) / 2, RD + T / 2, WIN_Z0 / 2), (WIN_X1 - WIN_X0, T, WIN_Z0), M_SHELL)
box('guscio_fondo_d', ((WIN_X0 + WIN_X1) / 2, RD + T / 2, (WIN_Z1 + RH) / 2), (WIN_X1 - WIN_X0, T, RH - WIN_Z1), M_SHELL)
box('guscio_sx', (-T / 2, RD / 2, RH / 2), (T, RD + 1, RH), M_SHELL)
box('guscio_dx', (RW + T / 2, RD / 2, RH / 2), (T, RD + 1, RH), M_SHELL)
box('guscio_soffitto', (RW / 2, RD / 2, RH + T / 2), (RW + 1, RD + 1, T), M_SHELL)
box('guscio_pavimento', (RW / 2, RD / 2, -T / 2), (RW + 1, RD + 1, T), M_SHELL)
box('guscio_fronte', (RW / 2, -0.6 - T / 2, RH / 2), (RW + 1, T, RH), M_SHELL)

# superfici interne con i materiali a strati (piccolo distacco dai gusci)
e = 0.002
def back_piece(name, x0, x1, z0, z1):
    return plane(name, ((x0 + x1) / 2, RD - e, (z0 + z1) / 2), (x1 - x0, z1 - z0), (math.radians(90), 0, 0), M_WALL_BACK)
# la parete di fondo è fatta di pezzi attorno alla finestra: coordinate Generated diverse, ma la passata resta credibile
back_piece('fondo_sx', 0, WIN_X0, 0, RH)
back_piece('fondo_dx', WIN_X1, RW, 0, RH)
back_piece('fondo_sotto', WIN_X0, WIN_X1, 0, WIN_Z0)
back_piece('fondo_sopra', WIN_X0, WIN_X1, WIN_Z1, RH)
plane('sx', (e, RD / 2 - 0.3, RH / 2), (RD + 0.6, RH), (math.radians(90), 0, math.radians(-90)), M_WALL_LEFT)
plane('dx', (RW - e, RD / 2 - 0.3, RH / 2), (RD + 0.6, RH), (math.radians(90), 0, math.radians(90)), M_WALL_RIGHT)
plane('fronte', (RW / 2, -0.6 + e, RH / 2), (RW, RH), (math.radians(90), 0, math.radians(180)), M_WALL_FRONT)
plane('soffitto', (RW / 2, RD / 2 - 0.3, RH - e), (RW, RD + 0.6), (math.radians(180), 0, 0), M_CEIL)
plane('pavimento', (RW / 2, RD / 2 - 0.3, e), (RW, RD + 0.6), (0, 0, 0), M_FLOOR)

# spalle della finestra (spessore muro) e infisso
M_REVEAL = layered_material('spalle', WALL_LAYERS, 2.9)
plane('spalla_sx', (WIN_X0 + e, RD + T / 2, (WIN_Z0 + WIN_Z1) / 2), (T, WIN_Z1 - WIN_Z0), (math.radians(90), 0, math.radians(-90)), M_REVEAL)
plane('spalla_dx', (WIN_X1 - e, RD + T / 2, (WIN_Z0 + WIN_Z1) / 2), (T, WIN_Z1 - WIN_Z0), (math.radians(90), 0, math.radians(90)), M_REVEAL)
plane('spalla_sotto', ((WIN_X0 + WIN_X1) / 2, RD + T / 2, WIN_Z0 + e), (WIN_X1 - WIN_X0, T), (0, 0, 0), simple_mat('davanzale', (0.55, 0.53, 0.5, 1), 0.5))
plane('spalla_sopra', ((WIN_X0 + WIN_X1) / 2, RD + T / 2, WIN_Z1 - e), (WIN_X1 - WIN_X0, T), (math.radians(180), 0, 0), M_REVEAL)
M_FRAME_OLD = simple_mat('infisso', (0.22, 0.2, 0.18, 1), 0.5)
fy = RD + T * 0.7
for nm, loc, sz in [
    ('inf_basso', ((WIN_X0 + WIN_X1) / 2, fy, WIN_Z0 + 0.03), (WIN_X1 - WIN_X0, 0.06, 0.06)),
    ('inf_alto', ((WIN_X0 + WIN_X1) / 2, fy, WIN_Z1 - 0.03), (WIN_X1 - WIN_X0, 0.06, 0.06)),
    ('inf_sx', (WIN_X0 + 0.03, fy, (WIN_Z0 + WIN_Z1) / 2), (0.06, 0.06, WIN_Z1 - WIN_Z0)),
    ('inf_dx', (WIN_X1 - 0.03, fy, (WIN_Z0 + WIN_Z1) / 2), (0.06, 0.06, WIN_Z1 - WIN_Z0)),
    ('inf_centro', ((WIN_X0 + WIN_X1) / 2, fy, (WIN_Z0 + WIN_Z1) / 2), (0.06, 0.06, WIN_Z1 - WIN_Z0)),
]:
    box(nm, loc, sz, M_FRAME_OLD)

# battiscopa (solo alla fine)
M_SKIRT = simple_mat('battiscopa', (0.92, 0.9, 0.86, 1), 0.4)
for nm, loc, sz in [('bs_fondo_sx', (WIN_X0 / 2, RD - 0.006, 0.04), (WIN_X0, 0.012, 0.08)),
                    ('bs_fondo_dx', ((WIN_X1 + RW) / 2, RD - 0.006, 0.04), (RW - WIN_X1, 0.012, 0.08)),
                    ('bs_fondo_c', ((WIN_X0 + WIN_X1) / 2, RD - 0.006, 0.04), (WIN_X1 - WIN_X0, 0.012, 0.08)),
                    ('bs_sx', (0.006, RD / 2, 0.04), (0.012, RD, 0.08))]:
    key_hide(box(nm, loc, sz, M_SKIRT), visible_from=P['p7'][0] + 22)

# modelli 3D veri (Poly Haven, CC0) in blender/modelli
MOD = os.path.join(HERE, 'modelli')
def importa(nome, loc, rz=0.0, scala=1.0, visible_from=None, hidden_from=None, rx=0.0, appoggia=None):
    import glob
    f = glob.glob(os.path.join(MOD, nome, '*.blend'))
    if not f: print('MANCA', nome); return []
    with bpy.data.libraries.load(f[0], link=False) as (src, dst):
        dst.objects = src.objects
    obs = [o for o in dst.objects if o is not None and o.type in ('MESH', 'EMPTY')]
    root = bpy.data.objects.new(nome, None); scn.collection.objects.link(root)
    for o in obs:
        scn.collection.objects.link(o)
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler = (rx, 0, rz); root.scale = (scala,) * 3
    if appoggia is not None:  # porta il punto piu basso del modello esattamente a quota 'appoggia'
        from mathutils import Vector
        bpy.context.view_layer.update()
        zmin = min((o.matrix_world @ Vector(c)).z for o in obs if o.type == 'MESH' for c in o.bound_box)
        root.location.z += appoggia - zmin
    for o in obs:
        if o.type == 'MESH': key_hide(o, visible_from=visible_from, hidden_from=hidden_from)
    return obs

# ------------------------------------------------------------------ fase 0: vecchio
M_RAD_OLD = simple_mat('termosifone_vecchio', (0.62, 0.6, 0.56, 1), 0.45, metal=0.3)
for i in range(12):
    o = box(f'rad_vecchio{i}', (1.55 + i * 0.09, RD - 0.12, 0.45), (0.06, 0.16, 0.62), M_RAD_OLD, bevel=0.01)
    key_hide(o, hidden_from=P['p3'][0] + 4 + i // 3)
rbar = box('rad_vecchio_tubo', (2.05, RD - 0.12, 0.13), (1.1, 0.03, 0.03), M_RAD_OLD)
key_hide(rbar, hidden_from=P['p3'][0] + 8)

# ------------------------------------------------------------------ fase 1: telo protettivo e sacchi
M_SHEET = fabric_mat('telo', (0.2, 0.2, 0.19, 1), 0.6)
fade_material(M_SHEET, f_in=(P['p1'][0] + 2, P['p1'][0] + 10), f_out=(P['p7'][0] + 2, P['p7'][0] + 10))
M_SHEET.blend_method = 'BLEND' if hasattr(M_SHEET, 'blend_method') else None
sh = plane('telo', (RW / 2, RD / 2 - 0.2, 0.03), (RW - 0.1, RD - 0.2), (0, 0, 0), M_SHEET)
key_hide(sh, visible_from=P['p1'][0] + 1, hidden_from=P['p7'][0] + 11)
md = sh.modifiers.new('sub', 'SUBSURF'); md.subdivision_type = 'SIMPLE'; md.levels = 5; md.render_levels = 6
dsp = sh.modifiers.new('onde', 'DISPLACE'); tx = bpy.data.textures.new('onde_telo', 'CLOUDS'); tx.noise_scale = 0.6; dsp.texture = tx; dsp.strength = 0.02; dsp.mid_level = 0.0
for i, (x, y, r) in enumerate([(0.4, 2.3, 0.3), (0.95, 2.15, -0.5), (0.45, 2.9, 1.2), (1.0, 2.75, 2.4)]):
    importa('trashbag', (x, y, 0.03), rz=r, scala=0.95, visible_from=P['p1'][0] + 10 + i * 3, hidden_from=P['p4'][0] + 2 + i)
# attrezzi di cantiere: compaiono con il lavoro, spariscono prima della consegna
FINE = P['p7'][0]
importa('cement_bag', (3.0, 2.25, 0.03), rz=0.2, visible_from=P['p2'][0], hidden_from=P['p4'][1])
importa('cement_bag', (3.05, 2.2, 0.21), rz=-0.15, visible_from=P['p2'][0], hidden_from=P['p4'][0] + 12)
importa('plastic_crate_01', (2.45, 2.5, 0.03), rz=0.5, visible_from=P['p2'][0] + 2, hidden_from=FINE)
importa('trowel_01', (2.45, 2.5, 0.3), rz=1.9, rx=math.radians(90), visible_from=P['p2'][0] + 2, hidden_from=FINE)
importa('Drill_01', (1.5, 3.3, 0.03), rz=2.2, visible_from=P['p3'][0], hidden_from=FINE)
importa('wooden_ladder_02', (2.85, 3.25, 0.03), rz=0.9, visible_from=P['p3'][0] + 2, hidden_from=FINE)
importa('cardboard_box_01', (0.5, 3.4, 0.2), rz=0.3, visible_from=P['p5'][0], hidden_from=FINE)

# ------------------------------------------------------------------ fase 2: tramezzo in mattoni che sale fila per fila
M_BRICKS = [simple_mat(f'mattone{i}', (0.42 + random.uniform(-.06, .05), 0.17 + random.uniform(-.03, .03), 0.09, 1), 0.85) for i in range(5)]
nb = M_BRICKS[0].node_tree
for mb in M_BRICKS:  # rugosità e grana del laterizio
    nt = mb.node_tree; n, l = nt.nodes, nt.links; b = n['Principled BSDF']
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 80; nz.inputs['Detail'].default_value = 8
    bp = n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35; l.new(nz.outputs['Fac'], bp.inputs['Height']); l.new(bp.outputs['Normal'], b.inputs['Normal'])
M_MORTAR = simple_mat('malta', (0.56, 0.54, 0.5, 1), 0.95)
BL, BH, BT, G = 0.25, 0.085, 0.12, 0.012
rows = int((RH - 0.02) // (BH + G))
f0, f1 = P['p2'][0], P['p2'][1] - 2
for r in range(rows):
    z = r * (BH + G)
    frame = f0 + int((f1 - f0) * r / max(1, rows - 1))
    off = (BL + G) / 2 if r % 2 else 0
    y = TY0 - off
    while y < TY1:
        ya, yb = max(y, TY0), min(y + BL, TY1)
        in_door = (yb > DOOR_Y0 and ya < DOOR_Y1 and z < DOOR_H)
        if yb - ya > 0.04 and not in_door:
            o = box('m', (TX, (ya + yb) / 2, z + BH / 2), (BT, yb - ya, BH), random.choice(M_BRICKS))
            key_hide(o, visible_from=frame)
        y += BL + G
    # malta della fila (dietro i mattoni)
    for (ya, yb) in ([(TY0, DOOR_Y0), (DOOR_Y1, TY1)] if z < DOOR_H else [(TY0, TY1)]):
        mo = box('malta', (TX, (ya + yb) / 2, z + (BH + G) / 2), (BT * 0.9, yb - ya, BH + G), M_MORTAR)
        key_hide(mo, visible_from=frame)
# architrave della porta
arch = box('architrave', (TX, (DOOR_Y0 + DOOR_Y1) / 2, DOOR_H + 0.06), (BT, DOOR_Y1 - DOOR_Y0 + 0.3, 0.12), simple_mat('architrave', (0.6, 0.58, 0.55, 1), 0.9))
key_hide(arch, visible_from=f0 + int((f1 - f0) * (DOOR_H / RH)) + 1)
# finitura del tramezzo (due facce + testa + spalle porta)
for side, xs in (('a', TX - BT / 2 - 0.01), ('b', TX + BT / 2 + 0.01)):
    rot = (math.radians(90), 0, math.radians(-90 if side == 'a' else 90))
    for nm, (ya, yb, za, zb) in {
        'sx': (TY0, DOOR_Y0, 0, RH), 'dx': (DOOR_Y1, TY1, 0, RH), 'sopra': (DOOR_Y0, DOOR_Y1, DOOR_H, RH)}.items():
        o = plane(f'tram_{side}_{nm}', (xs, (ya + yb) / 2, (za + zb) / 2), (yb - ya, zb - za), rot, M_TRAMEZZO)
        key_hide(o, visible_from=P['p4'][0] + 3)
o = plane('tram_testa', (TX, TY0 - 0.01, RH / 2), (BT + 0.02, RH), (math.radians(90), 0, 0), M_TRAMEZZO)
key_hide(o, visible_from=P['p4'][0] + 3)

# ------------------------------------------------------------------ fase 3: tracce e impianti
M_GROOVE = simple_mat('traccia', (0.16, 0.14, 0.13, 1), 0.95)
M_TUBE = simple_mat('corrugato', (0.45, 0.47, 0.49, 1), 0.6)
M_TUBE2 = simple_mat('multistrato', (0.85, 0.85, 0.83, 1), 0.3)
M_BOX = simple_mat('scatola', (0.82, 0.8, 0.75, 1), 0.5)
tracce = []
# verticali e orizzontali sulla parete di fondo e sinistra (posizione, misure, parete, materiale tubo)
spec = [
    ('b', 0.5, 0.3, 0.06, 2.1), ('b', 3.8, 0.3, 0.06, 2.1), ('bh', 0.5, 1.1, 3.3, 0.06),
    ('b', 3.0, 0.15, 0.06, 0.5), ('l', 3.4, 0.3, 0.06, 2.1), ('l', 4.6, 0.3, 0.06, 1.0), ('lh', 3.4, 2.35, 1.2, 0.06),
]
for k, (wall, a, z0, w, h) in enumerate(spec):
    if wall.startswith('b'):
        loc = (a + w / 2 if wall == 'bh' else a, RD - 0.004, z0 + h / 2) if wall == 'b' else (a + w / 2, RD - 0.004, z0)
        size = (w, 0.006, h) if wall == 'b' else (w, 0.006, 0.05)
        if wall == 'bh': loc = (a + w / 2, RD - 0.004, z0); size = (w, 0.006, 0.05)
        tube = cyl(f'tubo{k}', (loc[0], RD - 0.012, loc[2]), 0.012, max(size[0], size[2]), (0, math.radians(90) if wall == 'bh' else 0, 0), M_TUBE)
    else:
        loc = (0.004, a, z0 + h / 2) if wall == 'l' else (0.004, a + w / 2, z0)
        size = (0.006, w, h) if wall == 'l' else (0.006, w, 0.05)
        tube = cyl(f'tubo{k}', (0.012, loc[1], loc[2]), 0.012, max(size[1], size[2]), (math.radians(90) if wall == 'lh' else 0, 0, 0), M_TUBE)
    g = box(f'traccia{k}', loc, size, M_GROOVE)
    fa = P['p3'][0] + 2 + k * 2
    # le tracce vengono coperte dall'intonaco quando passa la passata
    key_hide(g, visible_from=fa, hidden_from=P['p4'][0] + 10)
    key_hide(tube, visible_from=fa + 2, hidden_from=P['p4'][0] + 10)
# scatole elettriche
for k, (x, z) in enumerate([(0.5, 0.3), (0.5, 1.1), (3.8, 0.3), (3.8, 1.1), (3.8, 2.1)]):
    o = box(f'scatola{k}', (x, RD - 0.01, z), (0.1, 0.02, 0.07), M_BOX)
    key_hide(o, visible_from=P['p3'][0] + 12 + k, hidden_from=P['p4'][0] + 12)
# tubi del nuovo termosifone sotto la finestra
for k, x in enumerate([1.7, 2.6]):
    o = cyl(f'tubo_rad{k}', (x, RD - 0.03, 0.12), 0.009, 0.24, (0, 0, 0), M_TUBE2)
    key_hide(o, visible_from=P['p3'][0] + 16)

# placche e prese finali (dopo la pittura)
M_PLATE = simple_mat('placca', (0.95, 0.94, 0.92, 1), 0.3)
for k, (x, z) in enumerate([(0.5, 0.3), (0.5, 1.1), (3.8, 0.3), (3.8, 1.1)]):
    o = box(f'placca{k}', (x, RD - 0.008, z), (0.12, 0.01, 0.085), M_PLATE)
    key_hide(o, visible_from=P['p7'][0] + 16)

# ------------------------------------------------------------------ fase 5: controsoffitto
M_PROFILE = simple_mat('profilo', (0.7, 0.72, 0.74, 1), 0.3, metal=0.9)
CZ = 2.58
f0, f1 = P['p5'][0], P['p5'][0] + 10
nprof = 8
for i in range(nprof):
    y = 0.2 + i * (RD - 0.4) / (nprof - 1)
    o = box(f'profilo{i}', (RW / 2, y, CZ + 0.02), (RW - 0.05, 0.027, 0.027), M_PROFILE)
    key_hide(o, visible_from=f0 + int((f1 - f0) * i / nprof), hidden_from=P['p5'][1] - 2)
M_BOARD = layered_material('lastre', [
    ((0.5, 0.5, 0.5, 1), 0, 0, None),
    ((0.74, 0.76, 0.78, 1), P['p5'][0] + 8, P['p5'][1] - 2, None),
    ((0.76, 0.76, 0.75, 1), P['p6'][0], P['p6'][1], None),
    ((0.86, 0.84, 0.8, 1), P['p7'][0], P['p7'][0] + 14, None),
], 1.5, base_transparent=True)
f0, f1 = P['p5'][0] + 8, P['p5'][1] - 2
panels = []
PW, PL = 1.2, 2.0
nx, ny = math.ceil(RW / PW), math.ceil((RD + 0.6) / PL)
idx = 0
for j in range(ny):
    for i in range(nx):
        x0, x1 = i * PW, min(RW, (i + 1) * PW); y0, y1 = -0.6 + j * PL, min(RD, -0.6 + (j + 1) * PL)
        if x1 - x0 < 0.05 or y1 - y0 < 0.05: continue
        o = box(f'lastra{idx}', ((x0 + x1) / 2, (y0 + y1) / 2, CZ), (x1 - x0 - 0.0008, y1 - y0 - 0.0008, 0.0125), M_BOARD)
        panels.append(o); idx += 1
for o in panels: bpy.data.objects.remove(o)
lastra = box('controsoffitto', (RW / 2, (RD - 0.6) / 2, CZ), (RW, RD + 0.6, 0.0125), M_BOARD)
key_hide(lastra, visible_from=P['p5'][0] + 6)
# veletta lungo la parete di fondo
vel = box('veletta', (RW / 2, RD - 0.2, CZ - 0.15), (RW, 0.4, 0.3), M_BOARD)
key_hide(vel, visible_from=P['p5'][1] - 4)
# faretti incassati
M_SPOT = simple_mat('faretto', (0.1, 0.1, 0.1, 1), 0.3, emit=((1.0, 0.78, 0.55, 1), 0.0))
key_value(M_SPOT.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], [(P['p7'][0] + 18, 0.0), (P['p7'][0] + 26, 40.0)])
spots = []
for k, x in enumerate([0.8, 1.9, 3.0, 4.0]):
    o = cyl(f'faretto{k}', (x, RD - 0.2, CZ - 0.31), 0.04, 0.01, (0, 0, 0), M_SPOT)
    key_hide(o, visible_from=P['p5'][1] - 3)
    L = bpy.data.lights.new(f'luce_faretto{k}', 'SPOT'); L.spot_size = math.radians(70); L.spot_blend = 0.6; L.color = (1.0, 0.76, 0.52)
    key_value_obj = L
    L.energy = 0; L.keyframe_insert('energy', frame=P['p7'][0] + 18); L.energy = 60; L.keyframe_insert('energy', frame=P['p7'][0] + 26)
    lo = bpy.data.objects.new(f'luce_faretto{k}', L); scn.collection.objects.link(lo)
    lo.location = (x, RD - 0.2, CZ - 0.33); lo.rotation_euler = (0, 0, 0)

# ------------------------------------------------------------------ fase 7: casa tua
M_RAD_NEW = simple_mat('termosifone_nuovo', (0.93, 0.93, 0.92, 1), 0.3)
rad = box('termosifone_nuovo', (2.15, RD - 0.07, 0.42), (1.0, 0.06, 0.5), M_RAD_NEW, bevel=0.01)
key_hide(rad, visible_from=P['p7'][0] + 20)
importa('Sofa_01', (1.95, 2.4, 0.01), rz=0.0, scala=1.3, visible_from=P['p7'][0] + 22)
importa('throw_pillows_01', (1.55, 2.55, 0.5), rz=0.15, scala=0.8, appoggia=0.56, visible_from=P['p7'][0] + 26)
M_RUG = fabric_mat('tappeto', (0.42, 0.38, 0.33, 1), 0.25)
fade_material(M_RUG, f_in=(P['p7'][0] + 20, P['p7'][0] + 28))
rug = box('tappeto', (1.95, 1.35, 0.008), (2.4, 1.7, 0.012), M_RUG, bevel=0.004)
key_hide(rug, visible_from=P['p7'][0] + 20)
importa('side_table_01', (3.45, 2.3, 0.01), rz=-0.3, scala=0.95, visible_from=P['p7'][0] + 24)
importa('potted_plant_04', (3.45, 2.3, 0.53), scala=1.3, visible_from=P['p7'][0] + 28)
M_BLACK = simple_mat('metallo_nero', (0.05, 0.05, 0.05, 1), 0.35, metal=0.8)
fade_material(M_BLACK, f_in=(P['p7'][0] + 24, P['p7'][0] + 32))
lamp = [cyl('lamp_base', (3.9, 2.4, 0.01), 0.14, 0.02, (0, 0, 0), M_BLACK), cyl('lamp_asta', (3.9, 2.4, 0.75), 0.012, 1.5, (0, 0, 0), M_BLACK)]
M_SHADE = simple_mat('paralume', (0.95, 0.9, 0.8, 1), 0.6, emit=((1.0, 0.75, 0.5, 1), 0.0))
key_value(M_SHADE.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'], [(P['p7'][0] + 24, 0.0), (P['p7'][0] + 32, 4.0)])
lamp.append(cyl('lamp_paralume', (3.9, 2.4, 1.55), 0.2, 0.3, (0, 0, 0), M_SHADE, verts=32))
for o in lamp: key_hide(o, visible_from=P['p7'][0] + 24)
LL = bpy.data.lights.new('luce_lampada', 'POINT'); LL.shadow_soft_size = 0.15; LL.color = (1.0, 0.72, 0.45)
LL.energy = 0; LL.keyframe_insert('energy', frame=P['p7'][0] + 24); LL.energy = 45; LL.keyframe_insert('energy', frame=P['p7'][0] + 32)
lo = bpy.data.objects.new('luce_lampada', LL); scn.collection.objects.link(lo); lo.location = (3.9, 2.4, 1.5)
# pianta
importa('potted_plant_02', (0.5, 3.6, 0.0), rz=0.6, scala=1.35, appoggia=0.01, visible_from=P['p7'][0] + 26)

# ------------------------------------------------------------------ luce: mattina -> tramonto
world = bpy.data.worlds.new('mondo'); scn.world = world; world.use_nodes = True
wn, wl = world.node_tree.nodes, world.node_tree.links
env = wn.new('ShaderNodeTexEnvironment')
env.image = bpy.data.images.load(os.path.join(HERE, 'hdri', 'piazza_bologni_4k.exr'))
etc = wn.new('ShaderNodeTexCoord'); emp = wn.new('ShaderNodeMapping')
emp.inputs['Rotation'].default_value = (0, 0, math.radians(float(arg('--hdri-rot', '0'))))
wl.new(etc.outputs['Generated'], emp.inputs['Vector']); wl.new(emp.outputs['Vector'], env.inputs['Vector'])
tint = wn.new('ShaderNodeMix'); tint.data_type = 'RGBA'; tint.blend_type = 'MULTIPLY'
wl.new(env.outputs['Color'], tint.inputs['A'])
bg = wn['Background']; wl.new(tint.outputs['Result'], bg.inputs['Color'])
for f, st, col, fac in [(0, 0.9, (1, 1, 1, 1), 0.0), (P['p7'][0], 0.9, (1, 1, 1, 1), 0.0),
                        (P['p7'][0] + 26, 0.75, (1.0, 0.62, 0.42, 1), 1.0), (FEND, 0.75, (1.0, 0.6, 0.4, 1), 1.0)]:
    bg.inputs['Strength'].default_value = st; bg.inputs['Strength'].keyframe_insert('default_value', frame=f)
    tint.inputs['B'].default_value = col; tint.inputs['B'].keyframe_insert('default_value', frame=f)
    tint.inputs['Factor'].default_value = fac; tint.inputs['Factor'].keyframe_insert('default_value', frame=f)
sun = bpy.data.lights.new('sole', 'SUN'); sun.angle = math.radians(1.2)
so = bpy.data.objects.new('sole', sun); scn.collection.objects.link(so)
for f, col, en, rx, rz in [(0, (1.0, 0.95, 0.88), 3.2, 62, 160), (P['p7'][0], (1.0, 0.95, 0.88), 3.2, 62, 160),
                           (P['p7'][0] + 26, (1.0, 0.62, 0.36), 3.6, 80, 172), (FEND, (1.0, 0.58, 0.33), 3.6, 81, 174)]:
    sun.color = col; sun.energy = en; sun.keyframe_insert('color', frame=f); sun.keyframe_insert('energy', frame=f)
    so.rotation_euler = (math.radians(rx), 0, math.radians(rz)); so.keyframe_insert('rotation_euler', frame=f)
# riempimento dalla finestra (portale di luce morbida) e dalla stanza
fl = bpy.data.lights.new('finestra', 'AREA'); fl.shape = 'RECTANGLE'; fl.size = WIN_X1 - WIN_X0; fl.size_y = WIN_Z1 - WIN_Z0
for f, en, col in [(0, 260, (0.92, 0.95, 1.0)), (P['p7'][0], 260, (0.92, 0.95, 1.0)), (P['p7'][0] + 26, 220, (1.0, 0.8, 0.62)), (FEND, 220, (1.0, 0.8, 0.62))]:
    fl.energy = en; fl.color = col; fl.keyframe_insert('energy', frame=f); fl.keyframe_insert('color', frame=f)
flo = bpy.data.objects.new('finestra', fl); scn.collection.objects.link(flo)
flo.location = ((WIN_X0 + WIN_X1) / 2, RD - 0.05, (WIN_Z0 + WIN_Z1) / 2); flo.rotation_euler = (math.radians(-90), 0, 0)
flo.visible_camera = False
rf = bpy.data.lights.new('riempimento', 'AREA'); rf.size = 3; rf.color = (0.95, 0.95, 1.0)
for f, en in [(0, 50), (P['p7'][0], 50), (P['p7'][0] + 26, 110), (FEND, 110)]:
    rf.energy = en; rf.keyframe_insert('energy', frame=f)
rfo = bpy.data.objects.new('riempimento', rf); scn.collection.objects.link(rfo)
rfo.location = (RW / 2, 0.2, 2.2); rfo.rotation_euler = (math.radians(70), 0, 0); rfo.visible_camera = False

for m in bpy.data.materials:
    if m.node_tree and m.node_tree.animation_data: smooth_keys(m.node_tree)
for d in [world.node_tree, sun, so, fl]:
    if getattr(d, 'animation_data', None): smooth_keys(d)

# ------------------------------------------------------------------ camera
cam = bpy.data.cameras.new('cam'); cam.lens = 19; cam.sensor_width = 36
co = bpy.data.objects.new('cam', cam); scn.collection.objects.link(co); scn.camera = co
co.location = (0.95, -0.35, 1.42)
target = Vector((2.55, RD, 1.22))
co.rotation_euler = (target - co.location).to_track_quat('-Z', 'Y').to_euler()
cam.shift_y = 0.02

# ------------------------------------------------------------------ render
scn.render.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.cycles.samples = SAMPLES
scn.cycles.use_adaptive_sampling = True; scn.cycles.adaptive_threshold = 0.02
scn.cycles.use_denoising = True; scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.max_bounces = 8; scn.cycles.diffuse_bounces = 4; scn.cycles.glossy_bounces = 2; scn.cycles.transparent_max_bounces = 16
scn.cycles.blur_glossy = 1.0; scn.cycles.sample_clamp_indirect = 8
if ASPECT == '9:16':
    scn.render.resolution_x = W; scn.render.resolution_y = int(W * 16 / 9)
    cam.lens = 14; co.location = (1.6, -0.45, 1.42); co.rotation_euler = (Vector((2.2, RD, 1.25)) - co.location).to_track_quat('-Z', 'Y').to_euler()
else:
    scn.render.resolution_x = W; scn.render.resolution_y = int(W * 9 / 16)
scn.render.resolution_percentage = 100
scn.view_settings.view_transform = 'AgX'; scn.view_settings.look = 'AgX - Medium High Contrast'
scn.view_settings.exposure = 0.2
for f, ex in [(0, 0.2), (P['p7'][0], 0.2), (P['p7'][0] + 26, 0.55), (FEND, 0.55)]:
    scn.view_settings.exposure = ex; scn.view_settings.keyframe_insert('exposure', frame=f)
scn.render.image_settings.file_format = 'PNG'; scn.render.image_settings.color_mode = 'RGB'
os.makedirs(OUT, exist_ok=True)

frames = [int(x) for x in FLIST.split(',')] if FLIST else list(range(int(FR.split('-')[0]), int(FR.split('-')[1]) + 1, STEP))
for f in frames:
    path = os.path.join(OUT, f'f{f:04d}.png')
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        continue
    scn.frame_set(f)
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('FATTO', f, flush=True)
print('RENDER COMPLETO')
