"""Module for custom exceptions"""


class NoSolutionError(Exception):
    """Raised when the problem has no solution"""

    def __init__(self, message: str = "No solution found"):
        """Initialize the exception

        Args:
            message (str, optional): Error message. Defaults to "No solution found".
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"
