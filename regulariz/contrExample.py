import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

T_max = 10.

# Функция x(t) = t + sin(ω t) / ω^2 , ω > 1
def x_of_t(t, omega):
    return t + np.sin(omega * t) / (omega ** 2)


# Вычисление обратной функции t(x) методом бисекции
def inverse_t(x_val, omega, t_min=0.0, t_max=T_max, tol=1e-10):
    """Возвращает t такое, что x_of_t(t, omega) = x_val."""
    # Проверка, что x_val входит в диапазон
    x_min = x_of_t(t_min, omega)
    x_max = x_of_t(t_max, omega)
    if not (x_min <= x_val <= x_max):
        # Если x_val вне диапазона, возвращаем ближайшую границу
        return t_min if x_val < x_min else t_max
    while t_max - t_min > tol:
        t_mid = (t_min + t_max) / 2.0
        x_mid = x_of_t(t_mid, omega)
        if x_mid < x_val:
            t_min = t_mid
        else:
            t_max = t_mid
    return (t_min + t_max) / 2.0


# Построение графиков
def plot_functions(omega, ax1, ax2):
    # Очистка осей
    ax1.clear()
    ax2.clear()

    # 1) Прямая функция x(t)
    print(f'T_max = {T_max}')
    t_vals = np.linspace(0, T_max, 500)
    x_vals = x_of_t(t_vals, omega)
    ax1.plot(t_vals, x_vals, 'b-', linewidth=2)
    ax1.set_xlabel('t')
    ax1.set_ylabel('x')
    ax1.set_title(f'x(t) = t + sin({omega}·t) / {omega}²')
    ax1.grid(True)
    ax1.set_xlim(0, T_max)
    # Определяем диапазон x для обратной функции
    x_min = x_of_t(0, omega)
    x_max = x_of_t(T_max, omega)
    margin = 0.05 * (x_max - x_min)
    ax1.set_ylim(x_min - margin, x_max + margin)

    # 2) Обратная функция t(x)
    # Выбираем сетку по x (например, 300 точек)
    x_vals_inv = np.linspace(x_min, x_max, 300)
    t_vals_inv = [inverse_t(x, omega) for x in x_vals_inv]
    ax2.plot(x_vals_inv, t_vals_inv, 'r-', linewidth=2)
    ax2.set_xlabel('x')
    ax2.set_ylabel('t')
    ax2.set_title('Обратная функция t(x)')
    ax2.grid(True)
    ax2.set_xlim(x_min - margin, x_max + margin)
    ax2.set_ylim(0, T_max)

    # Обновляем фигуру
    plt.draw()


# Обработчик ввода
def submit(text):
    try:
        new_omega = float(text)
        if new_omega <= 1.0:
            raise ValueError
        plot_functions(new_omega, ax1, ax2)
        text_box.set_val(f"{new_omega}")  # обновляем отображаемое значение
    except:
        text_box.set_val("Ошибка! ω > 1")
        plt.draw()


# Создание фигуры и осей
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)  # место для текстового поля

# Текстовое поле для ввода ω
axbox = plt.axes([0.3, 0.05, 0.4, 0.05])
text_box = TextBox(axbox, 'ω = ', initial='5')
text_box.on_submit(submit)

# Начальный график
plot_functions(5.0, ax1, ax2)

plt.show()