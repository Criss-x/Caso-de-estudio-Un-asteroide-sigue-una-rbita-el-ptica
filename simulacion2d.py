import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import os

# ==============================
# Verificar si las imágenes existen
# ==============================
if not os.path.exists("earth.png"):
    print("❌ No se encontró 'earth.png'")
if not os.path.exists("asteroid.png"):
    print("❌ No se encontró 'asteroid.png'")

#Imagen de fondo



# ==============================
# Definir la función r(θ)
# ==============================
def r(theta):
    return 38 / (1 + 0.25 * np.cos(theta))

# ==============================
# Crear ventana principal
# ==============================
root = tk.Tk()
root.title("Simulación de órbita elíptica")


# Crear figura de Matplotlib con estilo oscuro
#MODO OSCURO
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-60, 60)   # eje X
ax.set_ylim(-60, 60)   # eje Y
ax.set_aspect("equal")
ax.set_title("Órbita del asteroide", color="white")
ax.set_xlabel("X", color="white")
ax.set_ylabel("Y", color="white")
ax.grid(color="gray")

# Cargar imagen de fondo
bg_img = mpimg.imread("fondo_espacio.jpg")  # asegúrate que esté en la misma carpeta
ax.imshow(bg_img, extent=[-60, 60, -60, 60], aspect="equal", zorder=-1)

# Generar datos de la órbita
theta = np.linspace(0, 2 * np.pi, 1000)
r_vals = r(theta)
x = r_vals * np.cos(theta)
y = r_vals * np.sin(theta)

# Graficar la órbita
ax.plot(x, y, label="Órbita elíptica")
ax.legend()
ax.grid(True)

# ==============================
# Insertar imágenes
# ==============================
earth_img = mpimg.imread("earth.png")
asteroid_img = mpimg.imread("asteroid.png")

# Tierra en el centro
earth_imagebox = OffsetImage(earth_img, zoom=0.15)
earth_ab = AnnotationBbox(earth_imagebox, (0, 0), frameon=False)
ax.add_artist(earth_ab)

# Asteroide en posición inicial
asteroid_imagebox = OffsetImage(asteroid_img, zoom=0.07)
asteroid_ab = AnnotationBbox(asteroid_imagebox, (x[0], y[0]), frameon=False)
ax.add_artist(asteroid_ab)

# ==============================
# Animación del asteroide
# ==============================
def update(frame):
    asteroid_ab.xybox = (x[frame], y[frame])
    return asteroid_ab,

#Fondo Color negro
#fig.patch.set_facecolor("black")   # fondo de toda la figura
#ax.set_facecolor("black")          # fondo de los ejes
#ax.tick_params(colors="white")     # números de los ejes en blanco
#ax.xaxis.label.set_color("white")  # etiqueta eje X blanca
#ax.yaxis.label.set_color("white")  # etiqueta eje Y blanca
#ax.title.set_color("white")        # título en blanco
#ax.grid(color="gray")              # grilla gris


ani = FuncAnimation(fig, update, frames=len(x), interval=1, blit=True, repeat=True)

# Insertar figura en Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Botón para cerrar
btn = tk.Button(root, text="Cerrar", command=root.destroy)
btn.pack()

# Ejecutar ventana
root.mainloop()
