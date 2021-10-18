import numpy as np
import matplotlib.pyplot as plt
from time import sleep


def context_plot(plotter):
    def wrapped(*args, **kwargs):
        plotter(*args)
        plt.xlabel("Budget")
        plt.ylabel("Quality")
        plt.title(kwargs["title"])
        plt.show()
        return None

    return wrapped


@context_plot
def plot_runs(runs):
    """
    Plot every runs on the same figure
    """
    for run in runs:
        costs, qualities = run
        plt.plot(costs, qualities)


@context_plot
def plot_eah(eah):
    plt.imshow(eah, cmap="Oranges", origin="lower")


def create_eah(runs, nb_steps_costs=10, nb_steps_quality=10):
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

        print(f"Cost index: {ind}")
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

        print(f"Quality index: {ind}")
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
                for j in range(cost_ind):
                    eah_run[i, j] = 1

        eah += eah_run
    eah = np.abs(eah - np.max(eah))
    return eah


def create_eaf(runs, title):
    # TODO: To be implemented
    raise NotImplementedError
