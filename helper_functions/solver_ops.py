"""Solver operations module"""

import re
import math
import logging
from typing import Union
from ortools.linear_solver.pywraplp import Solver, Objective, Variable
from .constraint_ops import yeild_constraints
from .exceptions import NoSolutionError

# pylint: disable=line-too-long
# pylint: disable=eval-used
ROUND_METHS = {
    "down": math.floor,
    "floor": math.floor,
    "up": math.ceil,
    "ceil": math.ceil,
    "ceiling": math.ceil,
}


def gen_solver(
    object_func: dict[str, str],
    constraints: list[str],
    method: str = "GLOP",
    epsilon: float = 0.00001,
) -> Solver:
    """Generate a solver object. Will return first solver object created from dict.
        If a variable is a constraint but
        doesn't appear in the objective function, set it to 0*x1 in the objective function. If key is invalid, will minimize.

    Args:
        object_func (dict[str, str]): Objective function. eg. {"maximize": "3*x1 + x2"}. Note: "max" and "maximize" are both valid.
        constraints (list[str], optional): List of constraints. eg. ["x1 + 3*x2 <= 24"].
        method (str, optional): Method to use. Defaults to "GLOP".
        epsilon (float, optional): Epsilon value to implement <, > and !=. Defaults to 0.00001.
    Returns:
        Solver: Solver object
    """
    logging.info("Generating solver object for %s", object_func)

    for objective, equation in object_func.items():
        solver: Solver = Solver.CreateSolver(method.upper())
        variable_dict = {
            var: solver.NumVar(0, solver.infinity(), var)
            for var in re.findall(r"\b([a-zA-Z][a-zA-Z0-9_]*)\b", equation)
        }
        if objective.lower() in ["max", "maximize"]:
            solver.Maximize(eval(equation.replace(" ", ""), variable_dict))
        else:
            solver.Minimize(eval(equation.replace(" ", ""), variable_dict))

        for constr in constraints:
            for constraint in yeild_constraints(constr, epsilon):
                solver.Add(eval(constraint, variable_dict))

        return solver


def solve(
    solver: Solver,
    __round: Union[int, str, None] = None,
    __obj_func: Union[None, str] = None,
) -> dict[str, Union[float, str, dict[str, Union[float, list]]]]:
    """Solve the solver object. Will print the solution and the rounded solution if __round is not None.
    Args:
        solver (Solver): Solver object
        __round (int | str | None, optional): Round the solution values. Defaults to None. If 'down' or 'floor', will floor the solution values.
        __obj_func (None | str, optional): Objective function. Defaults to None.
    Returns:
        str: HTML string
    """

    status = solver.Solve()

    if not status == Solver.OPTIMAL:
        logging.error("Solver status: %s", status)
        raise NoSolutionError(f"No solution found for {__obj_func}")

    objective: Objective = solver.Objective()
    solution = objective.Value()

    logging.info("Solution: for %s", __obj_func)
    logging.info("Objective value = %f", solution)

    variable_dict = {}
    rounded_dict = {}
    variable: Variable
    for variable in solver.variables():
        value = variable.solution_value()
        name = variable.name()
        rounded_value = (
            ROUND_METHS[__round.lower()](value)
            if isinstance(__round, str) and __round.lower() in ROUND_METHS
            else round(value, __round)
            if isinstance(__round, int)
            else round(value)
        )
        variable_dict[name] = value
        rounded_dict[name] = rounded_value
        logging.info("%s = %s, rounded as %s", name, value, rounded_value)

    return {
        "solution": solution,
        "rounded_solution": eval(__obj_func, rounded_dict)
        if __obj_func is not None
        else "",
        "variables": dict_mash(variable_dict, rounded_dict),
    }


def dict_mash(_d1: dict[str], _d2: dict[str], *args) -> dict[str, list]:
    """Return a dictionary with all keys from all dictionaries

    Args:
        _d1 (dict[str]): Dictionary 1
        _d2 (dict[str]): Dictionary 2
        *args (dict[str]): Dictionaries

    Returns:
        dict[str]: Mashed dictionary
    """

    __d: dict[str, list] = {}
    for _dict in [_d1, _d2, *args]:
        for key, value in _dict.items():
            if key == "__builtins__":
                continue
            if key not in __d:
                __d[key] = []
            __d[key].append(value)
    return __d
