"""
Plot the distribution of the algorithms run in snp.py for evaluation
"""
import get_evaluation

if __name__ == "__main__":
    N_RUNS = 50
    METHOD_NAME = "num_annealing"
    get_evaluation.create_evaluation(N_RUNS, METHOD_NAME)
    runs = get_evaluation.get_data(METHOD_NAME)
    print(runs)


