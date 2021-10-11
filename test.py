"""
Plot the distribution of the algorithms run in snp.py for evaluation
"""
import get_evaluation
import evaluation_representation


if __name__ == "__main__":
    N_RUNS = 10
    METHOD_NAME = "num_annealing"
    get_evaluation.create_evaluation(N_RUNS, METHOD_NAME)
    runs = get_evaluation.get_data(METHOD_NAME)
    evaluation_representation.plot_runs(runs, title=METHOD_NAME)

    eah = evaluation_representation.create_eah(runs, 100, 100)
    evaluation_representation.plot_eah(eah, title=METHOD_NAME + "_eah")

