# Requiere: pip install vpython numpy
# Coloca junto al .py (si usas texturas locales):
#   - moon.jpg
#   - asteroid.png
#   - satellite_body.png
#   - solar_panel.jpg
from vpython import *
import numpy as np, os

# ---------- Utilidad: textura local con fallback ----------
def tex_kwargs(path, fallback_texture=None, fallback_color=None):
    # Retorna kwargs para pasar a objetos VPython:
    #   {'texture': path} si existe; si no, {'texture': fallback_texture} o {'color': fallback_color}
    if path and os.path.exists(path):
        return {'texture': path}
    elif fallback_texture is not None:
        return {'texture': fallback_texture}
    elif fallback_color is not None:
        return {'color': fallback_color}
    else:
        return {}

# ---------- Trayectoria del asteroide ----------
N = 600
t = np.linspace(0, 2*np.pi, N)
r = 38.0 / (1.0 + 0.25*np.cos(t))
x = r*np.cos(t); y = r*np.sin(t); z = 50.0*np.sin(t)

# ---------- Escena / cámara ----------
scene.background = color.black
scene.width = 900; scene.height = 650
scene.center = vector(0,0,0)
default_forward = vector(-1, -0.6, -1)
scene.forward = default_forward
scene.fov = 60 * pi/180
scene.autoscale = False

# ---------- Estrellas (points: radio en píxeles) ----------
np.random.seed(3)
S = 500; R = 400.0
u = np.random.uniform(-1,1,S)
theta = np.random.uniform(0, 2*np.pi, S)
phi = np.arccos(u)
xs = R*np.sin(phi)*np.cos(theta)
ys = R*np.sin(phi)*np.sin(theta)
zs = R*np.cos(phi)
stars = points(
    pos=[vector(xs[i],ys[i],zs[i]) for i in range(S)],
    radius=2, size_units='pixels', color=vector(1,1,1), emissive=True
)

# ---------- Sol de fondo ----------
sun_pos = vector(-140, 60, -160)
sun = sphere(pos=sun_pos, radius=30, color=color.orange, emissive=True)
local_light(pos=sun_pos, color=color.yellow)

# ---------- Tierra ----------
earth = sphere(pos=vector(0,0,0), radius=12,
               texture=textures.earth, shininess=0.2)

# ---------- Luna y satélite orbitando la Tierra (texturizados) ----------
R_moon = 34.0     # radio de órbita de la Luna
R_sat  = 20.0     # radio de órbita del satélite

# Luna (textura local moon.jpg si existe, si no gris)
moon = sphere(pos=earth.pos + vector(R_moon,0,0),
              radius=3.2, shininess=0.1,
              **tex_kwargs('moon.jpg', fallback_color=vector(0.7,0.7,0.75)))

# Satélite compuesto con texturas
def build_satellite(center):
    body = box(pos=center, size=vector(2.0,1.0,1.0),
               shininess=0.5,
               **tex_kwargs('satellite_body.png', fallback_color=vector(0.8,0.8,0.85)))
    panel_offset = 2.0
    panel_size = vector(0.15, 4.0, 1.4)
    pL = box(pos=center + vector(0, +panel_offset, 0), size=panel_size,
             shininess=0.2,
             **tex_kwargs('solar_panel.jpg', fallback_color=vector(0.1,0.2,0.8)))
    pR = box(pos=center + vector(0, -panel_offset, 0), size=panel_size,
             shininess=0.2,
             **tex_kwargs('solar_panel.jpg', fallback_color=vector(0.1,0.2,0.8)))
    dish = cone(pos=center + vector(1.4,0,0), axis=vector(1.2,0,0),
                radius=0.5, color=vector(0.85,0.85,0.9), shininess=0.4)
    return compound([body, pL, pR, dish], origin=center)

sat = build_satellite(earth.pos + vector(R_sat,0,0))

# Órbitas de referencia (opcionales)
moon_orbit = ring(pos=earth.pos, axis=vector(0,0,1), radius=R_moon, thickness=0.05, color=vector(0.8,0.8,0.8))
sat_orbit  = ring(pos=earth.pos, axis=vector(0,0,1), radius=R_sat,  thickness=0.04, color=vector(0.7,0.7,0.2))

# Velocidades/ángulos e inclinaciones
om_moon = 0.01; om_sat = 0.05
ang_moon = 0.0; ang_sat = 0.0
incl_moon = 0.22; incl_sat = -0.35

# ---------- Órbita roja y delgada del asteroide ----------
orbit = curve(color=color.red, radius=0)
for i in range(N):
    orbit.append(pos=vector(x[i], y[i], z[i]))

# ---------- Asteroide (textura local o rock integrada) ----------
asteroid = sphere(pos=vector(x[0], y[0], z[0]),
                  radius=1.6, shininess=0.05,
                  **tex_kwargs('asteroid.png', fallback_texture=textures.rock, fallback_color=vector(0.6,0.55,0.5)))

# ---------- Partículas: humo + fuego (tamaño constante, flicker) ----------
smoke, fire = [], []
flick_t = 0.0

def emit(pos, vdir):
    back = -0.7*vdir + vector(0, 0.25, 0)
    # Humo (1 partícula)
    p = sphere(pos=pos, radius=0.8, color=vector(0.6,0.6,0.6), opacity=0.55, shininess=0.0)
    smoke.append({'o':p, 'v':back*0.85, 'life':0.9})
    # Fuego: núcleo + envoltura (2 conos, emisivos)
    c1 = cone(pos=pos, axis=back.norm()*2.2, radius=0.85,
              color=vector(1.0,0.9,0.25), emissive=True, opacity=1.0, shininess=0.4)
    c2 = cone(pos=pos, axis=back.norm()*3.0, radius=1.25,
              color=vector(1.0,0.45,0.08), emissive=True, opacity=0.95, shininess=0.3)
    fire.append({'o':c1, 'v':back*1.25, 'life':0.30, 'core':True})
    fire.append({'o':c2, 'v':back*1.15, 'life':0.36, 'core':False})

def step_particles(dt):
    global flick_t
    flick_t += dt
    flick_core = 0.10*np.sin(13.0*flick_t) + 0.06*np.sin(9.0*flick_t + 0.9)
    flick_env  = 0.08*np.sin(11.0*flick_t + 0.6) + 0.05*np.sin(7.0*flick_t + 1.4)
    # Humo
    for p in list(smoke):
        o=p['o']
        o.pos += p['v']*dt
        o.opacity = max(0.0, o.opacity - 0.6*dt)
        p['life'] -= dt
        if p['life'] <= 0 or o.opacity <= 0.02:
            o.visible = False
            smoke.remove(p)
    # Fuego
    for p in list(fire):
        o=p['o']
        o.pos += p['v']*dt
        if p.get('core', False):
            o.opacity = max(0.0, min(1.0, o.opacity + flick_core))
            o.opacity = max(0.0, o.opacity - 2.2*dt)
        else:
            o.opacity = max(0.0, min(1.0, o.opacity + flick_env))
            o.opacity = max(0.0, o.opacity - 1.8*dt)
        p['life'] -= dt
        if p['life'] <= 0 or o.opacity <= 0.02:
            o.visible = False
            fire.remove(p)

# ---------- Botones de vista X/Y/Z/Default ----------
scene.append_to_caption('\nVistas: ')
def view_x(b=None):
    scene.center = vector(0,0,0); scene.forward = vector(-1, 0, 0); scene.up = vector(0,0,1)
def view_y(b=None):
    scene.center = vector(0,0,0); scene.forward = vector(0, -1, 0); scene.up = vector(0,0,1)
def view_z(b=None):
    scene.center = vector(0,0,0); scene.forward = vector(0, 0, -1); scene.up = vector(0,1,0)
def view_default(b=None):
    scene.center = vector(0,0,0); scene.forward = default_forward; scene.up = vector(0,0,1)
button(text='X', bind=view_x); scene.append_to_caption('  ')
button(text='Y', bind=view_y); scene.append_to_caption('  ')
button(text='Z', bind=view_z); scene.append_to_caption('  ')
button(text='Default', bind=view_default); scene.append_to_caption('\n')

# ---------- Animación (60 fps + interpolación) ----------
fps = 60
kf = 0.0
dk = N / (12.0*fps)
prev = vector(x[0], y[0], z[0])

# Parámetros luna/satélite
om_moon = 0.01; om_sat = 0.05
ang_moon = 0.0; ang_sat = 0.0
incl_moon = 0.22; incl_sat = -0.35

while True:
    rate(fps)
    # Asteroide (interpolado)
    i = int(kf) % N
    j = (i + 1) % N
    a = kf - int(kf)
    pos = vector(x[i]*(1-a)+x[j]*a, y[i]*(1-a)+y[j]*a, z[i]*(1-a)+z[j]*a)
    asteroid.pos = pos
    v = pos - prev
    vdir = v.hat if mag(v) > 1e-9 else vector(1,0,0)
    asteroid.rotate(angle=0.05, axis=vector(0,1,0), origin=pos)
    emit(pos, vdir)
    step_particles(1.0/fps)
    prev = pos
    kf = (kf + dk) % N

    # Luna (órbita inclinada)
    ang_moon += om_moon
    moon.pos = earth.pos + vector(R_moon*np.cos(ang_moon),
                                  R_moon*np.sin(ang_moon)*np.cos(incl_moon),
                                  R_moon*np.sin(ang_moon)*np.sin(incl_moon))

    # Satélite (órbita inclinada)
    ang_sat += om_sat
    sat.pos = earth.pos + vector(R_sat*np.cos(ang_sat),
                                 R_sat*np.sin(ang_sat)*np.cos(incl_sat),
                                 R_sat*np.sin(ang_sat)*np.sin(incl_sat))
    sat.axis = norm(sat.pos - earth.pos)
