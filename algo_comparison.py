import numpy as np
import matplotlib.pyplot as plt
import evaluation_representation as evaluation
import plot_evaluation
import get_evaluation
import os


def get_list_runs(method_names, nb_runs=10, deltas=(600, 660, 675)):
    list_runs = []
    for delta in deltas:
        list_method = []
        for method_name in method_names:

            # Runs for evaluation of a method
            get_evaluation.clear_method(method_name)
            for k in range(nb_runs):
                os.system("python snp.py -p False --solver {}".format(method_name))

            # get_data from our runs
            runs = get_evaluation.get_data(method_name)
            list_method.append(runs)

        list_runs.append(list_method)
    return list_runs


@plot_evaluation.context_plot
def compare_ert(method_names, nb_runs=10, deltas=(600, 660, 675)):
    list_runs = get_list_runs(method_names, nb_runs=10, deltas=(600, 660, 675))

    list_ert = [[evaluation.create_ert(runs, delta) for runs in list_runs] for delta in deltas]
    for ind_delta, delta in enumerate(deltas):
        for ind_method, ert in enumerate(method_names):
            plt.plot(list_ert[ind_delta][ind_method], label=f"{method_names}: delta = {delta}")

    return list_ert
