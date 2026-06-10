import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider


def compute_F(x, y, d):
    part1 = (5*x - 5) ** 2 # np.sin(4*np.pi*x-5*np.pi/2) + 15.*(x-1)**2 + 1       #(x - 1) ** 2
    diff = y - 1 / x
    term1 = part1 + 1000 * diff / (diff - d)
    term2 = part1 + 1000 * diff / (diff + d)
    return np.maximum(term1, term2)


# Сетка
N = 100
x_vals = np.linspace(0.5, 1.5, N)
y_vals = np.linspace(2 / 3, 2, N)
X, Y = np.meshgrid(x_vals, y_vals)

init_d = 3.5
Z = compute_F(X, Y, init_d)

# Создаём 3D-фигуру
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Поверхность
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.7)

# Контуры на нижней плоскости
z_offset = np.nanmin(Z) - 0.2 * (np.nanmax(Z) - np.nanmin(Z))
cont = ax.contour(X, Y, Z, levels=30, colors='black', linewidths=0.8, offset=z_offset)

# Настройка осей
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('F(x,y)')
ax.set_title(f'F(x, y) при d = {init_d}')
ax.set_zlim(z_offset, np.nanmax(Z))

# Colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

# Слайдер
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'd', 2.0, 5.0, valinit=init_d, valstep=0.01)


def update(val):
    global surf, cont
    d = slider.val
    Z_new = compute_F(X, Y, d)
    z_offset_new = np.nanmin(Z_new) - 0.2 * (np.nanmax(Z_new) - np.nanmin(Z_new))

    # Удаляем старые элементы
    surf.remove()
    cont.remove()  # для 3D-контура работает remove()

    # Создаём новые
    surf = ax.plot_surface(X, Y, Z_new, cmap='viridis', edgecolor='none', alpha=0.7)
    cont = ax.contour(X, Y, Z_new, levels=30, colors='black', linewidths=0.8, offset=z_offset_new)

    # Обновляем пределы оси Z и colorbar
    ax.set_zlim(z_offset_new, np.nanmax(Z_new))
    ax.set_title(f'F(x, y) при d = {d:.2f}')
    cbar.mappable.set_array(Z_new)
    cbar.mappable.set_clim(vmin=np.nanmin(Z_new), vmax=np.nanmax(Z_new))
    cbar.update_normal(cbar.mappable)

    fig.canvas.draw_idle()


slider.on_changed(update)
plt.show()