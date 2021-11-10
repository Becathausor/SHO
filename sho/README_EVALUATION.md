README_EVALUATION
========

What have been done in the SHO project:
--------------------------------------
Implementation of simulated annealing algorithm
Implementation of a population-based (genetical) algorithm
Implementation of an ERT-ECDF
Implementation of an EAF
Implementation of a design of experiment and determination of the best solver
Determination of the best solver

Design of Experiment
-------------------------------------
 Instances of Algorithm
 - Greedy (no parameter)
 - Simulated Annealing : 
   - T_init = 2000, alpha = 50, beta = 1.1
 - Population based (population_size: size of population, selection_size: number of samples selected):
   - pop_size = 15, selection_size = 5


Instances of the problem
   - nb_sensors = 3, sensor-range = 0.3, domain-width = 30
   - nb_sensors = 4, sensor-range = 0.3, domain-width = 30

 
Results
-------------

Following the Design of Experiment, we concluded that the **num_genetical** solver would give better results. To conclude this, we compared the the medians of each instance of the Algorithms.

How to run the project
------------------------

In the terminal, write the following command “python **test.py**”. It will run the implemented algorithms to solve the problems and plots EAF, ERT at probability 0.5 and run a benchmark to compute the medians of our algorithms.   

You can modify the different parameters in the file in the first section of test.py (PARAMETERS section). Notice that boolean variables are given to run specifically the different parts of the algorithm evaluation.

Information about modified or created files
-----------------------------------------
- snp.py (modified)
- algo.py (modified) : you will find the implementation of the simulated annealing and the population-based algorithms.
- test.py (created) : python file that allows to display the EAF, the ERT and the design of the experiment.
- plot_evaluation.py (created) : python file that allows to plot the EAF and the ERT.
- num_stochastic.csv (created) 
- num_greedy.csv (created)
- num_genetical.csv (created)
- num_annealing.csv (created)
- num_stochastic.txt (created)
- num_greedy.txt (created)
- num_genetical.txt (created)
- num_annealing.txt (created)
- get_evaluation.py (created) : 

    Python file that allows to keep in memory the costs and qualities over a run and store them in a Text file.

- ExperimentDesign.py (created) : 

    Python file defining the class to carry the design of Experiment.

- evaluation_representation.py (created) : 

  Python file that allows the creation of the EAF and the ERT in matrix format.
  algo_comparison.py (created)

The file make.py has not been modified so you can replace the objective function as you wish.

> Some arguments in the parser have been added :
> 
> - You can decide if you want to display the sensors and optimization curve when running snp.py with the argument --plot (True: the plots will appear, False: otherwise).
> - You can decide how to register the run (under the list format or the best value) with the argument --evaluation (True: return a list, False: return the best value).
> - You can decide on the living population size with the argument --pop_size when considering a population-based algorithm.





