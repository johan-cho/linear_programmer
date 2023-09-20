"""Run the application."""
import logging
from flask import Flask, request, render_template
from helper_functions import gen_solver, solve


def test_solve() -> str:
    """Test the solve function"""
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
    return solve(solvah, "down", next(iter(objective_func.values())))


def create_app() -> Flask:
    """Create a Flask application"""
    __app = Flask(__name__)

    @__app.route("/", methods=["GET", "POST"])
    def form() -> str:
        """Return a greeting to the user

        Returns:
            str: Greeting to the user"""

        if request.method == "POST":
            obj_func = request.form.get("obj_func")
            if not obj_func:
                return render_template("missing_objective.html")
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


app = create_app()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    app.run(debug=True)
