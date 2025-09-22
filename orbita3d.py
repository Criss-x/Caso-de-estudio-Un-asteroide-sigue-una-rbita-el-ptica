# Requiere: pip install matplotlib numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # activa proyección 3D

# Parámetros
t = np.linspace(0, 2*np.pi, 600)
r = 38.0 / (1.0 + 0.25*np.cos(t))
x = r * np.cos(t)
y = r * np.sin(t)
z = 50.0 * np.sin(t)

# Figura 3D
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(projection='3d')
ax.plot3D(x, y, z, color='purple', lw=2, alpha=0.8)
(point_line,) = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='deepskyblue', ms=8)

# Límites/etiquetas
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim(np.min(x)-10, np.max(x)+10)
ax.set_ylim(np.min(y)-10, np.max(y)+10)
ax.set_zlim(np.min(z)-10, np.max(z)+10)
ax.set_title('Curva 3D: r=38/(1+0.25 cos t), z=50 sin t')

# Animación
def update(i):
    point_line.set_data([x[i]], [y[i]])
    point_line.set_3d_properties([z[i]])
    return (point_line,)

ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=True, repeat=True)

plt.show()
# Para guardar: ani.save('curva3d.mp4', fps=30)  # requiere ffmpeg instalado
