import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Definir la función r(θ)
def r(theta):
    return 38 / (1 + 0.25 * np.cos(theta))

# Crear ventana principal
root = tk.Tk()
root.title("Simulación de órbita elíptica")

# Crear figura de Matplotlib
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.set_title("Órbita del asteroide")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Establecer los límites de los ejes a -50 y 50
ax.set_xlim(-60, 60)
ax.set_ylim(-60, 60)

# Generar datos
theta = np.linspace(0, 2 * np.pi, 1000)
r_vals = r(theta)
x = r_vals * np.cos(theta)
y = r_vals * np.sin(theta)

# Graficar
ax.plot(x, y, label=r"$r(\theta)=\frac{38}{1+0.25\cos\theta}$")
ax.legend()
ax.grid(True)

# Insertar figura en Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Botón para cerrar
btn = tk.Button(root, text="Cerrar", command=root.destroy)
btn.pack()

# Ejecutar ventana
root.mainloop()