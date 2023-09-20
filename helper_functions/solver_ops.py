"""Solver operations module"""

import re
import math
import logging
from ortools.linear_solver.pywraplp import Solver
from .constraint_ops import yeild_constraints

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
    object_func: dict[str, str], constraints: list[str], epsilon: float = 0.00001
) -> Solver:
    """Generate a solver object. Will return first solver object created from dict.
        If a variable is a constraint but
        doesn't appear in the objective function, set it to 0*x1 in the objective function. If key is invalid, will minimize.

    Args:
        object_func (dict[str, str]): Objective function. eg. {"maximize": "3*x1 + x2"}. Note: "max" and "maximize" are both valid.
        constraints (list[str], optional): List of constraints. eg. ["x1 + 3*x2 <= 24"].
        epsilon (float, optional): Epsilon value to implement <, > and !=. Defaults to 0.00001.
    Returns:
        Solver: Solver object
    """
    for objective, equation in object_func.items():
        solver: Solver = Solver.CreateSolver("GLOP")
        variable_dict = {
            var: solver.NumVar(0, solver.infinity(), var)
            for var in re.findall(r"\b([a-zA-Z][a-zA-Z0-9_]*)\b", equation)
        }
        if objective.lower() in ["max", "maximize"]:
            solver.Maximize(eval(equation.replace(" ", ""), variable_dict))
        else:
            solver.Minimize(eval(equation.replace(" ", ""), variable_dict))

        for constr in constraints:
            for constraint in yeild_constraints(constr.replace(" ", ""), epsilon):
                solver.Add(eval(constraint, variable_dict))

        return solver


# def solve(
#     solver: Solver,
#     __round: int | str | Literal["down"] | None = None,
#     objective_function: None | str = None,
# ) -> None:
#     """Solve the solver object. Will print the solution and the rounded solution if __round is not None.

#     Args:
#         solver (Solver): Solver object
#         __round (int | str | Literal["down"] | None, optional): Round the solution values. Defaults to None.
#         objective_function (None | str, optional): Objective function. Defaults to None.
#     """
#     solver.Solve()
#     print("Solution:")
#     print("Objective value = ", solver.Objective().Value())
#     variable: Variable
#     variable_dict = {}
#     for variable in solver.variables():
#         if isinstance(__round, int):
#             variable_dict[variable.name()] = round(variable.solution_value(), __round)

#         elif isinstance(__round, str):
#             if __round.lower() in ["down", "floor"]:
#                 variable_dict[variable.name()] = math.floor(variable.solution_value())
#             else:
#                 variable_dict[variable.name()] = round(variable.solution_value())
#         else:
#             variable_dict[variable.name()] = variable.solution_value()

#     for variable, value in variable_dict.items():
#         logging.info("%s = %f", variable, value)
#     if __round is not None and objective_function is not None:
#         logging.info("Rounded Solution: %f", eval(objective_function, variable_dict))


HTML = (
    """<!DOCTYPE html>"""
    """<html>"""
    """<head>"""
    """<meta charset="utf-8" />"""
    """<meta http-equiv="X-UA-Compatible" content="IE=edge" />"""
    """<title></title>"""
    """<meta name="description" content="" />"""
    """<meta name="viewport" content="width=device-width, initial-scale=1" />"""
    """<link rel="stylesheet" href="" />"""
    """</head>"""
    """<body>"""
    """<h1>Optimal Solution: {}</h1>"""
    """<h2>Rounded Solution: {}</h2>"""
    """<table>"""
    """<tr>"""
    """<th>Variable</th>"""
    """<th>Value</th>"""
    """<th>Rounded Value</th>"""
    """</tr>"""
    """{}"""
    """</table>"""
    """</body>"""
    """</html>"""
)


# """
# <!DOCTYPE html>
# <html>
#   <head>
#     <meta charset="utf-8" />
#     <meta http-equiv="X-UA-Compatible" content="IE=edge" />
#     <title></title>
#     <meta name="description" content="" />
#     <meta name="viewport" content="width=device-width, initial-scale=1" />
#     <link rel="stylesheet" href="" />
#   </head>
#   <body>

#   </body>
# </html>
# """


def solve(
    solver: Solver, __round: int | str | None = None, __obj_func: None | str = None
) -> str:
    """Solve the solver object. Will print the solution and the rounded solution if __round is not None.

    Args:
        solver (Solver): Solver object
        __round (int | str | None, optional): Round the solution values. Defaults to None. If 'down' or 'floor', will floor the solution values.
        __obj_func (None | str, optional): Objective function. Defaults to None.
    Returns:
        str: HTML string
    """

    solver.Solve()

    logging.info("Solution: for %s", __obj_func)
    logging.info("Objective value = %f", solver.Objective().Value())

    rounded_dict = {}
    variable_html = ""
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
        rounded_dict[name] = rounded_value
        logging.info("%s = %s, rounded as %s", name, value, rounded_value)
        variable_html += (
            f"<tr><td>{name}</td><td>{value}</td><td>{rounded_value}</td></tr>"
        )
    return HTML.format(
        solver.Objective().Value(),
        eval(__obj_func, rounded_dict) if __obj_func is not None else "",
        variable_html,
    )

    #     variable_dict = {
    #     variable.name(): (
    #         ROUND_METHS[__round.lower()](variable.solution_value())
    #         if isinstance(__round, str) and __round.lower() in ROUND_METHS
    #         else round(variable.solution_value())
    #         if isinstance(__round, str)
    #         else round(variable.solution_value(), __round)
    #         if isinstance(__round, int)
    #         else variable.solution_value()
    #     )
    #     for variable in solver.variables()
    # }
