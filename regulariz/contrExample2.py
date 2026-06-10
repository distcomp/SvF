import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

T_max = 10.0

def x_of_t(t, omega):
    return t + np.sin(omega * t) / (omega ** 2)

def dxdt(t, omega):
    return 1.0 + np.cos(omega * t) / omega

def f_prime_prime_analytic(t, omega):
    xdot = dxdt(t, omega)
    term1 = -omega * np.cos(omega * t) / (xdot ** 2)
    term2 = - (np.sin(omega * t) ** 2) / (xdot ** 3)
    return term1 + term2

def inverse_t(x_val, omega, t_min=0.0, t_max=T_max, tol=1e-10):
    x_min = x_of_t(t_min, omega)
    x_max = x_of_t(t_max, omega)
    if not (x_min <= x_val <= x_max):
        return t_min if x_val < x_min else t_max
    while t_max - t_min > tol:
        t_mid = (t_min + t_max) / 2.0
        x_mid = x_of_t(t_mid, omega)
        if x_mid < x_val:
            t_min = t_mid
        else:
            t_max = t_mid
    return (t_min + t_max) / 2.0

def compute_fpp_diff(t_vals, omega):
    """Вычисляет f''(x) методом конечных разностей на сетке t_vals."""
    x_vals = x_of_t(t_vals, omega)
    f_vals = dxdt(t_vals, omega)
    fpp = np.zeros_like(f_vals)
    for i in range(1, len(t_vals)-1):
        dx_left = x_vals[i] - x_vals[i-1]
        dx_right = x_vals[i+1] - x_vals[i]
        df_left = (f_vals[i] - f_vals[i-1]) / dx_left
        df_right = (f_vals[i+1] - f_vals[i]) / dx_right
        fpp[i] = 2.0 * (df_right - df_left) / (dx_left + dx_right)
    fpp[0] = fpp[1]
    fpp[-1] = fpp[-2]
    return fpp

def plot_functions(omega, N_anal, N_diff, ax1, ax2, ax3, ax4):
    for ax in (ax1, ax2, ax3, ax4):
        ax.clear()

    # Сетка для всех графиков (кроме аналитического f'') - используем N_diff
    t_diff = np.linspace(0, T_max, N_diff)
    dt_diff = t_diff[1] - t_diff[0]
    # Сетка для аналитического вычисления f'' (только для интеграла)
    t_anal = np.linspace(0, T_max, N_anal)
    dt_anal = t_anal[1] - t_anal[0]

    # Данные на сетке N_diff (для отображения x(t), f(x), и разностного f'')
    x_diff = x_of_t(t_diff, omega)
    f_diff = dxdt(t_diff, omega)
    fpp_diff = compute_fpp_diff(t_diff, omega)

    # Аналитические данные на сетке N_anal (только для f''_anal и интеграла)
    fpp_anal = f_prime_prime_analytic(t_anal, omega)

    # 1) x(t) - используем сетку N_diff
    ax1.plot(t_diff, x_diff, 'b-', lw=1.5)
    ax1.set_xlabel('t')
    ax1.set_ylabel('x')
    ax1.set_title(f'$x(t) = t + \\sin({omega}t)/{omega}^2$')
    ax1.grid(True)
    ax1.set_xlim(0, T_max)
    x_min, x_max = x_diff[0], x_diff[-1]
    margin = 0.05 * (x_max - x_min)
    ax1.set_ylim(x_min - margin, x_max + margin)

    # 2) t(x) обратная - строим по данным N_diff (или можно отдельно, неважно)
    x_inv = np.linspace(x_min, x_max, 500)
    t_inv = [inverse_t(x, omega) for x in x_inv]
    ax2.plot(x_inv, t_inv, 'r-', lw=1.5)
    ax2.set_xlabel('x')
    ax2.set_ylabel('t')
    ax2.set_title('Обратная функция $t(x)$')
    ax2.grid(True)
    ax2.set_xlim(x_min - margin, x_max + margin)
    ax2.set_ylim(0, T_max)

    # 3) f(x) - используем сетку N_diff
    ax3.plot(x_diff, f_diff, 'g-', lw=1.5)
    ax3.set_xlabel('x')
    ax3.set_ylabel('f(x)')
    ax3.set_title('Правая часть $f(x) = \\dot{x}(t)$')
    ax3.grid(True)
    ax3.set_xlim(x_min - margin, x_max + margin)
    ax3.relim()
    ax3.autoscale_view(scalex=False, scaley=True)

    # 4) f''(x) - отображаем разностную кривую (по N_diff) и, возможно, аналитическую пунктиром для сравнения
    ax4.plot(x_diff, fpp_diff, 'c-', lw=1.5, label='finite diff')
    # При желании можно добавить аналитическую кривую, но для наглядности используем только разностную
    # (но интеграл аналитический всё равно посчитаем отдельно)
    ax4.set_xlabel('x')
    ax4.set_ylabel('f\'\'(x)')
    ax4.set_title('Вторая производная $f\'\'(x)$ (конечные разности)')
    ax4.grid(True)
    ax4.set_xlim(x_min - margin, x_max + margin)
    ax4.relim()
    ax4.autoscale_view(scalex=False, scaley=True)

    # Интегралы
    integral_analytic = np.sum(fpp_anal ** 2) * dt_anal
    integral_diff = np.sum(fpp_diff ** 2) * dt_diff

    ax4.text(0.95, 0.95,
             f'$I_{{anal}} = {integral_analytic:.3f}$\n$I_{{diff}} = {integral_diff:.3f}$',
             transform=ax4.transAxes, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    plt.draw()

def submit_omega(text):
    # Обработчик только для omega? Лучше общий, но для простоты вызовем обновление
    update_all()

def submit_Nanal(text):
    update_all()

def submit_Ndiff(text):
    update_all()

def update_all():
    try:
        omega = float(text_box_omega.text)
        N_anal = int(text_box_Nanal.text)
        N_diff = int(text_box_Ndiff.text)
        if omega <= 1.0 or N_anal < 3 or N_diff < 3:
            raise ValueError
        plot_functions(omega, N_anal, N_diff, ax1, ax2, ax3, ax4)
        # Обновить отображаемые значения на случай, если было исправление
        text_box_omega.set_val(f"{omega}")
        text_box_Nanal.set_val(f"{N_anal}")
        text_box_Ndiff.set_val(f"{N_diff}")
    except:
        # Восстановление предыдущих корректных значений
        try:
            cur_omega = float(text_box_omega.text) if text_box_omega.text else 5.0
            cur_Nanal = int(text_box_Nanal.text) if text_box_Nanal.text else 500
            cur_Ndiff = int(text_box_Ndiff.text) if text_box_Ndiff.text else 200
        except:
            cur_omega, cur_Nanal, cur_Ndiff = 5.0, 500, 200
        text_box_omega.set_val(f"{cur_omega}")
        text_box_Nanal.set_val(f"{cur_Nanal}")
        text_box_Ndiff.set_val(f"{cur_Ndiff}")
        print("Ошибка: ω>1, N_anal>=3, N_diff>=3")
        plt.draw()

# Создание фигуры
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
plt.subplots_adjust(bottom=0.2)

# Поля ввода
axbox_omega = plt.axes([0.20, 0.05, 0.15, 0.04])
text_box_omega = TextBox(axbox_omega, 'ω = ', initial='5')
axbox_Nanal = plt.axes([0.40, 0.05, 0.15, 0.04])
text_box_Nanal = TextBox(axbox_Nanal, 'N_anal = ', initial='500')
axbox_Ndiff = plt.axes([0.60, 0.05, 0.15, 0.04])
text_box_Ndiff = TextBox(axbox_Ndiff, 'N_diff = ', initial='200')

# Привязываем обработчики
text_box_omega.on_submit(lambda x: update_all())
text_box_Nanal.on_submit(lambda x: update_all())
text_box_Ndiff.on_submit(lambda x: update_all())

update_all()
plt.show()