"""Run the application."""
from flask import Flask, request, render_template
from helper_functions import gen_solver, solve


def create_app():
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


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
