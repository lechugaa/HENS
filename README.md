# Performance effects of greedily calculated big-M constraints on exact models for heat recovery network synthesis

## Introduction
Heat Exchanger Network Synthesis (HENS) is one of the most important tasks in power, refining and chemical industries as well as emerging industries derived from environmental engineering. HENS is used in every process design as it has proven to be useful for reducing a process cost and increasing operability and controllability. Nevertheless, state-of-the-art algorithmic methods for HENS cannot solve moderately large problem instances as it constitutes a NP-Hard problem in the strong sense. The computational bottleneck of this task is the minimum number of matches optimization problem which is formulated as a mixed-integer linear optimization problem with big-M parameters. Commonly, these big-M parameters represent an additional layer of complexity if they are not tightly calculated, but an exact computation of them is time consuming and mostly requires solving the initial optimization problem first to obtain the precise values. I explore in this work a tighter computation of these parameters compared to traditional methods by using a greedy algorithm in order to perform the calculation swiftly as it is needed. Fifteen benchmark instances of HENS were solved using both the transportation and transshipment models with their big-M parameters calculated both in the trivial traditional manner and with the proposed greedy algorithm. The experimental results show that in complex HENS problem instances, the greedy proposed big-M parameters outperform the ones calculated trivially. 

## Repository Conents
* `data` – input data for the problems.
* `lib` – required code for solving the proposed problems
    * `classes` – object representation of important problem entities
        * **Minimum Utility Problem Class** – encapsulates all the necessary elements of a minimum utility cost problem
        * **Network Class** – abstacts the necessary items for a Min Number of Matches Problem
        * **Process Stream Class** – abstracts a process stream (including hot and cold utilities)
        * **Stream Class** – abstracts a stream 
        * **Temperature Interval Class** – abstracts the idea of a temperature interval 
        * **Utility Class** – encapsulates hot and cold utilities
    * `solvers` – necesary scripts for solving the problems
        * **Greedy Max Heat** – greedy algorithm that calculates the maximum amount of heat that can be possibly exchanged between two stream h and c in T temperature intervals
        * **Greedy Min Delta** – it selects matches between hot stream "h" and cold stream "c" iteratively util it ends up with a feasible set of M matches exchanging sum(hi) units of heat. 
        * **Minimization of Utility Solver** – optimization script that minimizes utility cost
        * **Minimization of Matches Solver via Transport Model** – optimization script that minimizes number of matches using the Transport Model
        * **Minimization of Matches Solver via Transshipment Model** – optimization script that minimizes number of matches using the Transshipment Model


## Acknowledges
This project mainly replicates the investigation done by Letsios, Kouyialis and Misener using as reference both their [article](https://doi.org/10.1016/j.compchemeng.2018.03.002) and their [repository](https://github.com/dimletsios/min_matches_heuristics) available at GitHub. 

The mathematical optimization models and heuristics are implemented using Python 2.7.16 and Pyomo 5.6.7 using their [book](https://www.springer.com/gp/book/9783319588193) as main reference for this package.

## References
1. W. D. Seider, J. D.  Seader, D. R. Lewin and S. Widagdo, Product and Process Design Principles: Synthesis, Analysis and Evaluation, 3rd ed., John Wiley & Sons, Inc, 2009, pp.  252–280
1. S. A. Papoulias and I.E. Grossmann, “A structural optimization approach in process synthesis II”. Comput. Chem. Eng, vol 7, pp. 707–721,  January 1983.
1.	Y. Chen  and R. Nicole, “Computational strategies for large-scale MILP transshipment models for heat exchanger network synthesis”. Comput. Chem. Eng, vol 82, pp. 68–83,  November 2015. 
1.	K. C. Furman and N. V Sahinidis. “Computational complexity of heat exchanger network synthesis”. Comput. Chem. Eng, vol 25, pp. 1371–1390,  September 2001.
1.	K. C. Furman and N. V Sahinidis. “A creitical review and annotated bibliography for Heat Exchanger Netwrok Synthesis in the 20th Century”. Ind. Eng. Chem. Res, vol 41, pp. 2335–2370, 2002.
1.	D. Letsios, G. Kouyialis and R. Misener. “Heuristics with performance guarantees for the minimum number of matches problem in heat recovery network design”.  Comput. Chem. Eng, vol. 113, pp. 57–85,  May 2018.
1.	J. Cerda and A. W.Westerburg. “Synthesizing heat exchanger networks having restricted stream/stream matches using transportation problem formulations”. Chem. Eng. Sci, vol 38, pp. 1723–1740, October 2001.
1.	T. Gundersen, P. Traedal and A. Hashemi-Ahmady. “Improved sequential strategy for the synthesis of near-optimal heat exchanger networks”. Comput. Chem. Eng, vol. 21, pp. S59–S64,  May 1997.
1.	W. E. Hart, C. D Laird, J. P. Watson, D. L. Woodruff, G. A. Hackebeil, B. L. Nicholson and J. D. Siirola. Pyomo – Optimization Modeling in Python. Second Edition.  Vol. 67. Springer, 2017.
1.	D. Letsios, G. Kouyialis and R. Misener. 2017. Source Code. https://github.com/dimletsios/min_matches_heuristics.
