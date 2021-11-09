from scipy import stats
import numpy as np
import get_evaluation
import csv
import os
import matplotlib.pyplot as plt


class ExperimentDesign:
    def __init__(self, list_methods: list, list_parameters: list, budget: int = 60, nb_runs: int = 10):
        """
        Initializer of the class. 
        
        :param list_methods: List of strings designating the different methods 
        :param list_parameters: List of parameters of the problems 
        :param budget: Integer for the budget at which we want to get the experiment design
        :param nb_runs: Number of runs for the different estimators
        """""
        self.list_methods = list_methods
        self.parameters = list_parameters

        self.budget = budget
        self.nb_runs = nb_runs

        self.medians = []
        self.iqrs = []

    def __str__(self):
        return f"Experiment Design: \n" \
               f"Methods: \n" \
               f"{self.list_methods}\n" \
               f"Parameters: \n" \
               f"{self.parameters}"

    def __repr__(self):
        return self.__str__()

    def compute_median(self, runs):
        """Compute the median of runs performance at a given call budget."""
        list_performance = [run[1][min(self.budget, len(run[1]) - 1)] for run in runs]
        median = np.median(list_performance)
        print(list_performance)
        print(median)
        return median

    def compute_iqr(self, runs):
        """
        Compute the Inter-Quartile of the performance of runs at a given budget.
        :param runs: list of run (list of qualities)
        :return: iqr: double
        """
        list_performance = [run[1][min(self.budget, len(run[1]) - 1)] for run in runs]
        iqr = stats.iqr(list_performance)
        return iqr

    def get_runs(self, method, params):
        # Gets the runs according to a certain problem and a method
        get_evaluation.clear_method(method)
        for k in range(self.nb_runs):
            os.system(f"python snp.py "
                      f"-n {params['nb-sensors']} "
                      f"-r {params['sensor-range']} "
                      f"-w {params['domain-width']} "
                      f"--solver {method} "
                      f"--iters {self.budget} "
                      f"--evaluation True"

                      )
        return get_evaluation.get_data(method)

    def bench_medians(self):
        """Create a csv file to register the medians of the methods"""
        self.medians = []

        n_methods = len(self.list_methods)
        n_parameters = len(self.parameters)

        for method in self.list_methods:
            print(f"GETTING DATA FOR METHOD {method}")
            for params in self.parameters:
                print(f"Parameters: {params}")
                # Get the median of the runs
                runs = self.get_runs(method, params)
                result = self.compute_median(runs)
                self.medians.append(result)

        self.medians = np.array(self.medians).reshape((n_methods, n_parameters))

        return None

    def bench_iqrs(self):
        """Create a csv file to register the medians of the methods"""
        self.iqrs = []

        n_methods = len(self.list_methods)
        n_parameters = len(self.parameters)

        for method in self.list_methods:
            for params in self.parameters:

                # Get the median of the runs
                runs = self.get_runs(method, params)
                result = self.compute_iqrs(runs)
                self.iqrs.append(result)

        self.iqrs = np.array(self.iqrs).reshape((n_methods, n_parameters))

        return None

    def plot_medians(self):
        fig, ax = plt.subplots()
        ax.imshow(self.medians)

        ax.set_yticklabels(self.list_methods)
        ax.set_xticklabels(self.parameters)
        ax.set_title("Medians Study")
        ax.set_xlabel("Problems parameters")
        ax.set_ylabel("Algorithm")

        plt.show()
        return fig, ax

    def plot_iqrs(self):
        fig, ax = plt.subplots()
        ax.imshow(self.iqrs)
        ax.set_yticklabels(self.list_methods)
        ax.set_xticklabels(self.parameters)
        ax.set_title("Inter-Quartiles Study")
        ax.set_xlabel("Problems parameters")
        ax.set_ylabel("Algorithm")

        plt.show()
        return fig, ax

    def evaluate_bench_median(self):
        self.bench_medians()
        self.plot_medians()
        return self.medians
