"""Run the application."""
import ast
import logging
import traceback
from typing import Union
from flask import Flask, request, render_template, redirect, Response, url_for
from helper_functions import gen_solver, solve, NoSolutionError

# pylint: disable=broad-except

logging.getLogger().setLevel(logging.INFO)


def test_solve() -> str:
    """Test the solve function"""
    objective_func = {"minimize": "2*x1 + 5*x2"}

    solvah = gen_solver(
        objective_func,
        ["x1 + x2 == 10", "-2*x1+3*x2 <= -6", "8*x1 - 4*x2 >= 8"],
        epsilon=0.7,
    )
    return solve(solvah, "auto", next(iter(objective_func.values())))


def create_app() -> Flask:
    """Create a Flask application"""
    __app = Flask(__name__)

    @__app.route("/missing_objective", methods=["GET"])
    def missing_objective() -> str:
        """Return a page that tells the user that they are missing an objective function"""
        return render_template(
            "missing_objective.html", _obj_func=request.args.get("obj_func")
        )

    @__app.route("/error", methods=["GET"])
    def error() -> str:
        """Return a page that tells the user that there was an error"""
        return render_template(
            "error.html",
            _error=request.args.get("_error"),
            _traceback=request.args.get("_traceback"),
        )

    @__app.route("/no_solution", methods=["GET"])
    def no_solution() -> str:
        """Return a page that tells the user that there was no solution"""
        return render_template(
            "no_solution.html",
            _error=request.args.get("_error"),
            _traceback=request.args.get("_traceback"),
        )

    @__app.route("/result", methods=["GET"])
    def result() -> str:
        """Return a result page"""
        return render_template(
            "result.html",
            solution=request.args.get("solution"),
            rounded_solution=request.args.get("rounded_solution"),
            variables=ast.literal_eval(request.args.get("variables")),
        )

    @__app.route("/", methods=["GET", "POST"])
    def form() -> Union[str, Response]:
        """Return a greeting to the user

        Returns:
            str: a rendered template"""

        if request.method == "POST":
            obj_func = request.form.get("obj_func")
            if not obj_func:
                return redirect(url_for(".missing_objective", _obj_func=obj_func))

            try:
                solver = gen_solver(
                    {request.form.get("goal"): obj_func},
                    request.form.get("constraints").split("\r\n"),
                    request.form.get("method"),
                    request.form.get("epsilon", 0, float),
                )

                solved = solve(solver, request.form.get("round"), obj_func)

                # return solve(solver, request.form.get("round"), obj_func)

                return redirect(
                    url_for(
                        ".result",
                        solution=solved["solution"],
                        rounded_solution=solved["rounded_solution"],
                        variables=solved["variables"],
                    )
                )

            except NoSolutionError as error:
                logging.error(error)
                return redirect(
                    url_for(
                        ".no_solution",
                        _error=error,
                        _traceback=traceback.format_exc(),
                    )
                )
            except Exception as error:
                logging.error(error)
                return redirect(
                    url_for(
                        ".error",
                        _error=error,
                        _traceback=traceback.format_exc(),
                    )
                )
        return render_template("index.html")

    return __app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
    # test_solve()
