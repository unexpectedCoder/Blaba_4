import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    N, P, Q, W, D, M = 5, .95, .1, .05, .25, 1_000_000
    p_all_collected = []
    p_destroyed = []
    p_super_weapon = []
    n_list = []

    print("Моделирование для N =", N)
    res = modeling(N, P, Q, W, D, M)
    p_all_collected.append(res.loc['p_all_collected'])
    p_destroyed.append(res.loc['p_destroyed'])
    p_super_weapon.append(res.loc['p_super_weapon'])
    n_list.append(N)
    print(res)

    N = 20
    print("Моделирование для N =", N)
    res = modeling(N, P, Q, W, D, M)
    p_all_collected.append(res.loc['p_all_collected'])
    p_destroyed.append(res.loc['p_destroyed'])
    p_super_weapon.append(res.loc['p_super_weapon'])
    n_list.append(N)
    print(res)

    N = 100
    print("Моделирование для N =", N)
    res = modeling(N, P, Q, W, D, M)
    p_all_collected.append(res.loc['p_all_collected'])
    p_destroyed.append(res.loc['p_destroyed'])
    p_super_weapon.append(res.loc['p_super_weapon'])
    n_list.append(N)
    print(res)

    labels = [r"Вероятность сбора всех грузов", "Вероятность уничтожения БПЛА", "Вероятность собрать супер-оружие"]
    show(p_all_collected, p_destroyed, p_super_weapon, labels, n_list)

    return 0


def modeling(N: int, P: float, Q: float, W: float, D: float, M: int) -> pd.Series:
    """Функция моделирования.

    :param N: количество точек сбора компонент супер-оружия.
    :param P: вероятность собрать супер-оружие без одного компонента.
    :param Q: вероятность искать компонент по неверным координатам.
    :param W: вероятность засады на точке сбора.
    :param D: вероятность уничтожения дрона в засаде.
    :param M: число "прогонок".
    """
    collected_list = []
    destroyed = 0

    for _ in range(M):
        collected = 0
        for n in range(N):
            if np.random.random() <= W and np.random.random() <= D:
                collected = 0
                destroyed += 1
                break
            if np.random.random() > Q:
                collected += 1
        collected_list.append(collected)
    collected = np.array(collected_list)

    p_all_collected = collected[collected == N].size / M                # вероятность нахождения всех N частей
    p_super_weapon = np.mean(np.power(np.full(M, P), N - collected))    # вероятность собрать супер-оружие
    p_destroyed = destroyed / M                                         # вероятность уничтожения БПЛА

    return pd.Series({
        'p_all_collected': p_all_collected,
        'p_super_weapon': p_super_weapon,
        'p_destroyed': p_destroyed,
        'M': M
    })


def show(*results):
    probs = results[:-2]
    n_list = results[-1]
    labels = results[-2]

    fig = plt.figure("Results", figsize=(8, 8))

    for i in range(len(n_list)):
        plt.plot(n_list, probs[i], ls=':', marker='x', label=labels[i])
    plt.xlabel(r"$N$")
    plt.ylabel(r"$P$")
    plt.legend()
    plt.grid(True)

    plt.savefig('results.png')
    plt.close(fig)


if __name__ == '__main__':
    main()
