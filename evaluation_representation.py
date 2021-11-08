import numpy as np


def create_eaf(runs, nb_steps_costs=10, nb_steps_quality=10, reverse_eah=False):
    eah = np.zeros((nb_steps_costs, nb_steps_quality))

    # Cost borders
    cost_min = min([min(run[0]) for run in runs])
    cost_max = max([max(run[0]) for run in runs])

    # Quality borders
    quality_min = min([min(run[1]) for run in runs])
    quality_max = max([max(run[1]) for run in runs])

    def get_ind_cost(cost):
        """
        Computes the index of eah corresponding to the cost
        """
        step = (cost_max - cost_min) / (nb_steps_costs - 1)
        ind = (cost - cost_min) // step

        # print(f"Cost index: {ind}")
        if ind >= nb_steps_costs:
            print(cost)
            print(cost_max)
            raise Exception("Error step definition of Cost")

        return int(ind)

    def get_ind_quality(quality):
        """
        Computes the index of eah corresponding to the quality
        """
        step = (quality_max - quality_min) / (nb_steps_quality - 1)
        ind = (quality - quality_min) // step

        # print(f"Quality index: {ind}")
        if ind >= nb_steps_quality:
            raise Exception("Error step definition of Quality")

        return int(ind)

    for number, run in enumerate(runs):
        eah_run = np.zeros((nb_steps_costs, nb_steps_quality))
        run_points = zip(*run)
        for point in run_points:
            # Find the edge of the histogram
            cost_ind, quality_ind = (get_ind_cost(point[0]), get_ind_quality(point[1]))
            point_tab = cost_ind, quality_ind

            # Update of the run_eah
            for i in range(quality_ind):
                for j in range(cost_ind, nb_steps_costs):
                    eah_run[i, j] = 1

        eah += eah_run
    if reverse_eah:
        eah = np.abs(eah - np.max(eah))
    return eah


def create_ert(runs, delta):

    cost_max = max([len(run[0]) for run in runs])
    ert_tranche = np.zeros(int(cost_max))

    n = len(runs)

    for run in runs:
        costs, qualities = run
        ert_run = np.array(list(map(lambda x: x > delta, qualities)))
        if len(ert_run) < cost_max:
            ert__run = np.zeros(int(cost_max))

            # Rallongement de la liste
            ert__run[:len(ert_run)] = ert_run
            ert__run[len(ert_run):] = ert_run[-1]
            ert_run = ert__run

        # Ajout des échantillons bien trouvés
        ert_tranche += ert_run
    ert_tranche /= n
    return ert_tranche


def create_eah(runs, nb_steps_probability=10):
    quality_min = min([min(run[1]) for run in runs])
    quality_max = max([max(run[1]) for run in runs])

    deltas = np.linspace(quality_min, quality_max, nb_steps_probability)
    eaf = np.array(list(map(lambda d: create_ert(runs, d), deltas)))
    costs = np.arange(len(eaf[0]))
    qualities = deltas

    x, y = np.meshgrid(costs, qualities)

    return x, y, eaf