"""Abstract base class defining the interface for all file processors."""

import abc

__all__ = ["ProcessClass"]


class ProcessClass(abc.ABC):
    """Abstract base class enforcing a process_file method on all subclasses."""

    @abc.abstractmethod
    def process_file(self) -> None:
        """Process a single file and write its output to the appropriate directory.

        Implementations must load the file at the path provided during construction,
        apply the relevant transformation (extraction, normalisation, tagging, etc.),
        and persist the result. Implementations should raise a specific exception on
        failure rather than silently suppressing errors.

        Raises:
            FileNotFoundError: If the source file cannot be found.
            ValueError: If the source file is corrupt or in an unsupported format.
        """
