from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class BaseTask(Protocol[T_co]):
    """A protocol for defining tasks."""

    def __init__(self, *args: tuple[T_co], **kwargs: dict[str, T_co]) -> None:
        """Initialize the task with given arguments."""

    def run(self) -> None:
        """Execute the task.

        Raises:
            NotImplementedError: If the method is not implemented.

        """
        raise NotImplementedError
