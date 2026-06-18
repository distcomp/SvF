import pyomo.environ as pyo
from pyomo.opt import SolverFactory, TerminationCondition
import math

def generate_maximin(A, B, C, v, V, K = 6, alpha_max=10, beta_max=10, time_limit=60, initial=[], debug = False):
    """
    Генерирует K точек (α, β) внутри области
    v ≤ Aα² + 2Bαβ + Cβ² ≤ V, α,β ≥ 0,
    максимизируя минимальное попарное евклидово расстояние (максимин).

    Параметры:
        A, B, C : коэффициенты квадратичной формы
        v, V    : нижняя и верхняя границы формы (v < V)
        K       : число точек (K >= 2)
        alpha_max, beta_max : верхние границы для переменных (опционально)
        time_limit : ограничение по времени для решателя (секунды)
        initial : начальные значения (опционально)

    Возвращает:
        list of tuples: [(α1, β1), (α2, β2), ...] или пустой список, если решение не найдено.
    """
    if v > V:
        raise ValueError("v должно быть <= V")
    if K < 2:
        raise ValueError("K должно быть >= 2")

    # Создаём модель
    model = pyo.ConcreteModel()

    # Индексы точек
    model.I = pyo.RangeSet(K)

    # Индексы пар точек
    pairs = [(i, j) for i in model.I for j in model.I if i < j]
    model.IJ = pyo.Set(dimen=2, initialize=pairs)

    # Переменные: координаты точек
    model.alpha = pyo.Var(model.I, bounds=(0, alpha_max))
    model.beta = pyo.Var(model.I, bounds=(0,beta_max))

    # Переменная для минимального расстояния (максимизируем)
    model.d = pyo.Var(within=pyo.NonNegativeReals)

    # Опциональные верхние границы для координат
    # Ограничения: каждая точка должна лежать в заданной области
    def quad_lower_rule(model, i):
        return v <= A * model.alpha[i]**2 + 2 * B * model.alpha[i] * model.beta[i] + C * model.beta[i]**2
    model.quad_lower = pyo.Constraint(model.I, rule=quad_lower_rule)

    def quad_upper_rule(model, i):
        return A * model.alpha[i]**2 + 2 * B * model.alpha[i] * model.beta[i] + C * model.beta[i]**2 <= V
    model.quad_upper = pyo.Constraint(model.I, rule=quad_upper_rule)

    # Ограничения: расстояние между каждой парой точек >= d
    def distance_rule(model, i, j):
        return (model.alpha[i] - model.alpha[j])**2 + (model.beta[i] - model.beta[j])**2 >= model.d
    model.dist_constraints = pyo.Constraint(model.IJ, rule=distance_rule)

    # Целевая функция: максимизировать d
    model.obj = pyo.Objective(expr=model.d, sense=pyo.maximize)

    # Выбор решателя
    solver = SolverFactory('/usr/local/bin/ipopt') # /usr/local/bin/ipopt /opt/scipopt921/bin/ipopt

    # Опции решателя: ограничение по времени и отключение вывода
    solver.options['max_cpu_time'] = time_limit
    solver.options['print_user_options'] = 'yes'
    solver.options['print_level'] = 4  # 0 - минимум вывода, 5 - стандартный вывод

    # Задание начальных значений
    if len(initial)>0:
        for i in model.I:
            if  i > len(initial):
                break
            (model.alpha[i].value, model.beta[i].value ) = initial[i-1]
        model.d.value = 0.

    if debug:
        model.pprint()
    # Решение задачи

    results = solver.solve(model, load_solutions=True, tee=True)

    # Проверка статуса решения
    if results.solver.termination_condition != TerminationCondition.optimal:
        print(f"Предупреждение: решатель не нашёл оптимальное решение. Статус: {results.solver.termination_condition}")
        # Можно попытаться вернуть лучшее найденное решение, даже если оно не оптимально
        if results.solver.termination_condition == TerminationCondition.maxIterations:
            print("Возвращается допустимое (не оптимальное) решение.")
        else:
            return ([], None)

    # Извлечение координат
    points = []
    for i in model.I:
        alpha_val = pyo.value(model.alpha[i])
        beta_val = pyo.value(model.beta[i])
        points.append((alpha_val, beta_val))

    return (points, math.sqrt(pyo.value(model.d)))

if __name__ == '__main__':
    examples = [ # A, B, C, d, dm, dM, amax, bmax
        (1.0, 0.0, 1.0, 0.05, .5, 2., 0.3, 0.3),   # эллипс (окружность)
        (2.0, 0.5, 1.0, 0.05, .5, 2., 0.3, 0.3),   # эллипс
        (0.0, 0.5, 0.6, 0.05, .5, 2., 1.0, 1.0), # гипербола  (0.0, 1.0, 1.0, 0.05, 1.0, 1.0),
        (1.0, 1.0, 0.0, 0.05, .5, 2., 1.0, 1.0),   # α^2 + 2αβ = d
        (0.0, 0.0, 1.0, 0.05, .5, 2., 0.3, 0.6),   # β^2 = d
        (1.0, 2.0, 1.0, 0.01, .5, 2., 0.1, 0.1)
    ]

    from testInitCoeffBelt import generate_points_band

    (A, B, C, d, dm, dM, amax, bmax) = examples[3] # 3 0
    print (A, B, C, d, dm, dM, amax, bmax)
    v = dm * d
    V = dM * d
    points = []
    K = 8
    points = generate_points_band(A, B, C, v, V, num_points=4)
    (points, maxmindist) = generate_maximin(A, B, C, v, V, K=K, alpha_max=amax, beta_max=bmax, time_limit=300, initial=points)
    print(f'dist={maxmindist}, d={maxmindist**2}')
    for (a, b) in points:
        # print(alpha_val, beta_val)
        print(f'a={a},b={b}')