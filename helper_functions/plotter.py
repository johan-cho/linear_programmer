"""Module for plotting linear equations and inequalities using plotly."""
import os
import random


from flask import url_for
import numpy as np
import matplotlib.pyplot as plt
from .constraint_ops import get_constant
from .os_helper import goback, delete_all

# pylint: disable=eval-used
x = y = np.linspace(0, 15, 400)
X, Y = np.meshgrid(x, y)

COLOR_LIST = [
    "#FF5733",
    "#33FF57",
    "#3373FF",
    "#FF33A1",
    "#FF5733",
    "#33FFFF",
    "#AA33FF",
    "#FF5733",
    "#33FFAA",
    "#FF33E1",
]

PATH_TO_GRAPHS = os.path.join(goback(__file__, 2), "static", "graph")


def plot(equations: list[str]) -> str:
    """Plot linear equations and inequalities using matplotlib

    Args:
        equations (list[str]): List of equations
    Returns:
        path (str): Path to the image"""

    constants = [get_constant(eq) for eq in equations]
    fig = plt.figure(figsize=(8, 8))

    plt.imshow(
        eval(
            " & ".join(
                f'({eq.replace("x1", "X").replace("x2", "Y").upper()})'
                for eq in equations
            )
        ).astype(int),
        # eval(eval(eq.replace("x1", "X").replace("x2", "Y")) for eq in equations),
        extent=(X.min(), X.max(), Y.min(), Y.max()),
        origin="lower",
        cmap="Greys",
        alpha=0.3,
    )

    for equ in equations:
        plt.contour(
            X,
            Y,
            eval(equ.replace("x1", "X").replace("x2", "Y").upper()),
            levels=[0],
            colors=random.choice(COLOR_LIST),
        )

        # plt.clabel(contour, inline=1, fontsize=10)
        # for col in contour.collections:
        #     col.set_label(equ)
        # plt.plot(X, Y, eval(eq.replace("x1", "X").replace("x2", "Y")), label=eq)

    plt.xlim(0, max(constants))
    plt.ylim(0, max(constants))
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.title("Solution Space")
    plt.xlabel(r"$x (x1)$")
    plt.ylabel(r"$y (x2)$")
    # plt.show()

    if not os.path.exists(PATH_TO_GRAPHS):
        os.makedirs(PATH_TO_GRAPHS)
    delete_all(PATH_TO_GRAPHS)
    f_name = f"{'-'.join(equations).replace('*', '').replace('+', '').replace('>', '').replace('<', '')}.png"
    fig.savefig(os.path.join(PATH_TO_GRAPHS, f_name))
    return url_for("static", filename="graph/" + f_name)


# def graph_as_img(equations: list[str]) -> io.StringIO:
#     """Return a graph as an image

#     Args:
#         equations (list[str]): List of equations
#     Returns:
#         bytes: StringIO object"""

#     img = io.StringIO()
#     fig = plot(equations)
#     fig.savefig(img, format="png")
#     img.seek(0)
#     return img


if __name__ == "__main__":
    figg = plot(["x1+x2<=6", "-2*x1+3*x2<=-6", "8*x1-4*x2>=8", "x1>=0", "x2>=0"])
    # figg.savefig("test.png")
