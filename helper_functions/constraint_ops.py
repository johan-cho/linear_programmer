"""Constraint operations module"""
import re
from typing import Iterable

OPERATOR_MAPPER = {
    "<": "<<",
    ">": ">>",
    "=": "==",
    "=<": "<=",
    "=>": ">=",
    "≥": ">=",
    "≤": "<=",
}


def yield_constraints(constraint: str, epsilon: float = 0.00001) -> Iterable[str]:
    """Return a parsed constraint with an epsilon added to the constant

    Args:
        constraint (str): Constraint string
        epsilon (float, optional): Epsilon value. Defaults to 0.00001.
    Yields:
        Iterable[str]: Constraint with epsilon added to the constant
    """
    constraint = format_equation(constraint)
    operator = re.search(r"([<>=!]+)", constraint).group()
    constraint = constraint.replace(operator, OPERATOR_MAPPER.get(operator, operator))
    operator = OPERATOR_MAPPER.get(operator, operator)

    if operator in ["<<", ">>"]:
        yield mod_constr(constraint, get_constant(constraint), operator, epsilon)
    elif operator == "!=":
        for opr in ["<<", ">>"]:
            yield mod_constr(
                constraint.replace("!=", opr), get_constant(constraint), opr, epsilon
            )
    else:
        yield constraint


def mod_constr(constraint: str, constant: float, operator: str, epsilon: float) -> str:
    """Return a constraint with an epsilon added to the constant

    Args:
        constraint (str): Constraint string
        constant (float): Constant value
        operator (str): Operator
        epsilon (float): Epsilon value
    Returns:
        str: Constraint with epsilon added to the constant
    """

    if operator == "<<":
        return constraint_replace(constraint, constant, operator, epsilon).replace(
            operator, "<="
        )
    return constraint_replace(constraint, constant, operator, epsilon).replace(
        operator, ">="
    )


def constraint_replace(__constr: str, __const: str, __opr: str, __eps: float) -> str:
    """Return a constraint with an epsilon added to the constant

    Args:
        __constr (str): Constraint string
        __const (str): Constant value
        __eps (float): Epsilon value
    Returns:
        str: Constraint with epsilon added to the constant
    """

    new_const = __const - __eps if __opr == "<<" else __const + __eps
    new_constraint = __constr.replace(str(__const), str(new_const))
    if new_constraint == __constr:
        new_constraint = __constr.replace(str(int(__const)), str(new_const))
    return new_constraint


def format_equation(equation: str) -> str:
    """Return a formatted equation

    Args:
        equation (str): Equation string
    Returns:
        str: Formatted equation
    """

    return re.sub(
        r"(\d)([a-zA-Z])", r"\1*\2", equation.replace(" ", "").replace("_", "")
    )


def yield_variables(equation: str) -> Iterable[str]:
    """Return a set of variables in the equation

    Args:
        equation (str): Equation string
    Yields:
        Iterable[str]: Set of variables in the equation
    """

    yield from set(re.findall(r"\b([a-zA-Z][a-zA-Z0-9_]*)\b", equation))


def get_coefficent(equation: str, variable: str) -> float:
    """Return the coefficient of the variable in the equation

    Args:
        equation (str): Equation string
        variable (str): Variable name
    Returns:
        float: Coefficient of the variable in the equation
    """

    return float(re.search(rf"(\d+|\d+\.\d+)({variable})", equation).group(1))


def get_constant(equation: str) -> float:
    """Return the constant in the equation

    Args:
        equation (str): Equation string
    Returns:
        float: Constant in the equation
    """

    return float(re.search(r"[<>=]+(-?\d+)", equation).group(1))
