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


def delete_all(__path: str, limit: int = 5) -> None:
    """Delete all files and folders in a path

    Args:
        __path (str): Path to delete"""

    for root, dirs, files in os.walk(__path):
        for __files in (dirs, files):
            if len(__files) < limit:
                continue
        for file in files:
            os.remove(os.path.join(root, file))
        for _dir in dirs:
            os.rmdir(os.path.join(root, _dir))


if __name__ == "__main__":
    goback()
