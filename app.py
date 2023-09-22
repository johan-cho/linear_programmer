"""Run the application."""
import logging
from flask import Flask, request, render_template, redirect, Response
from helper_functions import gen_solver, solve


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
        return render_template("missing_objective.html")

    @__app.route("/", methods=["GET", "POST"])
    def form() -> str | Response:
        """Return a greeting to the user

        Returns:
            str: a rendered template"""

        if request.method == "POST":
            obj_func = request.form.get("obj_func")
            if not obj_func:
                return redirect("/missing_objective")
            return solve(
                gen_solver(
                    {request.form.get("goal"): obj_func},
                    request.form.get("constraints").split("\r\n"),
                    request.form.get("epsilon", 0, float),
                ),
                request.form.get("round"),
                obj_func,
            )
        return render_template("index.html")

    return __app


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    app = create_app()
    app.run(debug=True)
    # test_solve()
