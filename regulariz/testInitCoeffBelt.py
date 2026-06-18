import numpy as np
import matplotlib.pyplot as plt

def plot_band_region(A, B, C, d, dm=0.5, dM=2., alpha_max=1.0, beta_max=1.0, n_points=500, ax=None):
    """
    Рисует кривую A*α^2 + 2B*α*β + C*β^2 = d и закрашивает область,
    где 0.5*d < F < 2*d.
    """
    alpha = np.linspace(0, alpha_max, n_points)
    beta = np.linspace(0, beta_max, n_points)
    Alpha, Beta = np.meshgrid(alpha, beta)
    F = A * Alpha**2 + 2 * B * Alpha * Beta + C * Beta**2

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 5))

    # Закрашиваем область: 0.5*d < F < 2*d
    levels = [dm*d, dM*d]
    # Цвет для полосы – светло-зелёный, прозрачность 0.5
    ax.contourf(Alpha, Beta, F, levels=levels, colors='lightgreen', alpha=0.5)
    # Рисуем основную кривую F = d
    ax.contour(Alpha, Beta, F, levels=[d], colors='red', linewidths=2)

    ax.set_xlabel(r'$\alpha$', fontsize=12)
    ax.set_ylabel(r'$\beta$', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_xlim(-.02, alpha_max*1.02)
    ax.set_ylim(-.02, beta_max*1.02)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    # Тип кривой
    D = A*C - B*B
    if D > 0:
        curve_type = '$AC - B^2 > 0$'
    elif D == 0:
        curve_type = '$AC - B^2 = 0$'
    else:
        curve_type = '$AC - B^2 < 0$'
    ax.text(0.1, 0.05, curve_type, transform=ax.transAxes,
            ha='right', va='bottom', fontsize=9, bbox=dict(facecolor='white', alpha=0.8))

    return ax


def generate_points_band(A, B, C, v, V, num_points=6):
    """
    Генерирует num_points точек (α, β) внутри области
    v ≤ Aα² + 2Bαβ + Cβ² ≤ V, α,β ≥ 0.
    Точки лежат на средней поверхности Q = (v+V)/2 и равномерно распределены по углу.
    Сейчас - по очереди лежат на границах Q = v или Q = V
    """
    points = []
    # Углы от 0 до π/2, исключая края (0 и π/2), где форма может вырождаться
    angles = np.linspace(0, np.pi / 2, num_points + 2)[1:-1]
    k = 0
    for phi in angles:
        cosphi = np.cos(phi)
        sinphi = np.sin(phi)
        R = A * cosphi ** 2 + 2 * B * cosphi * sinphi + C * sinphi ** 2
        if R <= 1e-12:
            continue  # на этом луче Q=0, область пуста (т.к. v>0)
        k += 1
        # t = np.sqrt((v + V) / (2.*R))
        # t = (dm/dM)*t if 2*int(k/2) == k else (dM/dm)*t
        t = np.sqrt((V + V) / (2.*R)) if 2 * int(k / 2) == k else np.sqrt((v + v) / (2.*R))
        alpha = t * cosphi
        beta = t * sinphi
        points.append((alpha, beta))

    # Если точек меньше требуемого (из-за вырожденных углов), добавим случайные
    while len(points) < num_points:
        # Грубая оценка максимального α,β: из верхней границы при R минимальном
        # Просто возьмём достаточно большой диапазон
        max_coord = 2 * np.sqrt(V / min(A, C, 1e-9))  # запас
        alpha = np.random.uniform(0, max_coord)
        beta = np.random.uniform(0, max_coord)
        Q = A * alpha ** 2 + 2 * B * alpha * beta + C * beta ** 2
        if v <= Q <= V:
            points.append((alpha, beta))

    return points[:num_points]


if __name__ == "__main__":
    # Те же примеры, что и ранее
    examples = [ # A, B, C, d, dm, dM, amax, bmax
        (1.0, 0.0, 1.0, 0.05, .5, 2., 0.3, 0.3),   # эллипс (окружность)
        (2.0, 0.5, 1.0, 0.05, .5, 2., 0.3, 0.3),   # эллипс
        (0.0, 0.5, 0.6, 0.05, .5, 2., 1.0, 1.0), # гипербола  (0.0, 1.0, 1.0, 0.05, 1.0, 1.0),
        (1.0, 1.0, 0.0, 0.05, .5, 2., 1.0, 1.0),   # α^2 + 2αβ = d
        (0.0, 0.0, 1.0, 0.05, .5, 2., 0.3, 0.6),   # β^2 = d
        (1.0, 2.0, 1.0, 0.01, .5, 2., 0.1, 0.1)
    ]

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()

    import initmaxmin

    for idx, (A, B, C, d, dm, dM, amax, bmax) in enumerate(examples):
        ax = axes[idx]
        plot_band_region(A, B, C, d, dm=dm, dM=dM, alpha_max=amax, beta_max=bmax, ax=ax)
        ax.set_title(f'{idx+1}: A={A}, B={B}, C={C}, d={d}, dm={dm}, dM={dM}', fontsize=9)
        # Генерация точек внутри полосы (v = dm*d, V = dM*d)
        v = dm * d
        V = dM * d
        K = 8
        init_points = generate_points_band(A, B, C, v, V, num_points = K)
        (points, maxmindist) = initmaxmin.generate_maximin(A, B, C, v, V, K = K, alpha_max=amax, beta_max=bmax, time_limit=300, initial=init_points)
        print(f'n={idx + 1}, dist={maxmindist}, d={maxmindist**2}')
        for (a, b) in points:
            print(f'a={a},b={b}')

        # Отображаем точки чёрным цветом
        for (alpha, beta) in points:
            ax.plot(alpha, beta, 'o', color='black', markersize=4)


    # Удаляем неиспользуемые подграфики
    for j in range(len(examples), len(axes)):
        axes[j].axis('off')

    # Общий заголовок
    fig.suptitle(f'Полоса $dm{{\\cdot}}d < \\mathcal{{R}}(\\alpha,\\beta) = A\\alpha^2 + 2B\\alpha\\beta + C\\beta^2 < dM{{\\cdot}}d$ (залита зелёным)\nКривая $\\mathcal{{R}}(\\alpha,\\beta) = d$ – красная линия', fontsize=12)
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.savefig('regularizCoeffBelt.png')
    plt.show()

