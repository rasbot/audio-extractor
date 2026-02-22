"""Abstract base class defining the interface for all file processors."""

import abc


class ProcessClass(abc.ABC):
    """Abstract base class enforcing a process_file method on all subclasses."""

    @abc.abstractmethod
    def process_file(self) -> None:
        """Process a file."""
        pass
