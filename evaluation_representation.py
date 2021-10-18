import numpy as np
import matplotlib.pyplot as plt


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
    plt.imshow(eah, cmap="Oranges")


def create_eah(runs, nb_steps_costs=10, nb_steps_quality=10):
    eah = np.zeros((nb_steps_costs, nb_steps_quality))

    cost_min = min([min(run[0]) for run in runs])
    cost_max = max([max(run[0]) for run in runs])
    quality_min = min([min(run[1]) for run in runs])
    quality_max = max([max(run[1]) for run in runs])

    def get_ind_cost(cost):
        """
        Computes the index of eah corresponding to the cost
        """
        step = (cost_max - cost_min) * 1.5 / nb_steps_costs
        ind = cost // step
        return ind

    def get_ind_quality(quality):
        """
        Computes the index of eah corresponding to the quality
        """
        step = (quality_max - quality_min) * 1.5 / nb_steps_costs
        ind = quality // step
        return ind

    for run in runs:
        eah_run = np.zeros((nb_steps_costs, nb_steps_quality))
        run_points = zip(*run)
        for point in run_points:
            # Find the edge of the histogram
            point_tab = (get_ind_cost(point[0]), get_ind_quality(point[1]))

            # Update of the run_eah
            for i in range(int(point_tab[1]), nb_steps_quality):
                for j in range(int(point_tab[0]), nb_steps_costs):
                    eah_run[i, j] = 1
        eah += eah_run

    return eah


def create_eaf(runs, title):
    # TODO: To be implemented
    raise NotImplementedError