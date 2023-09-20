"""
Main file for linear programming solver. 
Will generate a solver object from a dict and a list of constraints.
"""
import logging
from helper_functions import gen_solver, solve


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    objective_func = {"maximize": "50*x1 + 20*x2 + 25*x3"}

    solvah = gen_solver(
        objective_func,
        [
            "9*x1 + 3*x2 + 5*x3 <= 500",
            "5*x1 + 4*x2 <= 350",
            "3*x1 + 2*x3 <= 150",
            "x1 >= 0",
            "x2 >= 0",
            "0 <= x3 <= 20",
        ],
        epsilon=0.7,
    )
    solve(solvah, "down", next(iter(objective_func.values())))
