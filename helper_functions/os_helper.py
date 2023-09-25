"""Helper functions for os module"""

import os


def goback(file: str = None, levels: int = 1) -> str:
    """Return a path that is levels above the current path

    Args:
        file (str): __file__ from the current file
        levels (int, optional): Number of levels to go back. Defaults to 1.

    Returns:
        str: Path that is levels above the current path
    """
    return os.path.normpath(
        (file or __file__) + "".join(os.sep + os.pardir for _ in range(levels))
    )


if __name__ == "__main__":
    goback()
