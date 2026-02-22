import abc


class ProcessClass(abc.ABC):
    """Enforce the ProcessClasses to have a process_file method.
    """
    @abc.abstractmethod
    def process_file(self) -> None:
        """Method called to process a file by a ProcessClass.
        """
        pass
