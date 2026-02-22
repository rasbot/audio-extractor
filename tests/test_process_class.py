import pytest
from process_class import ProcessClass


class TestProcessClass:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            ProcessClass()

    def test_concrete_subclass_without_process_file_raises(self):
        class Incomplete(ProcessClass):
            pass

        with pytest.raises(TypeError):
            Incomplete()

    def test_concrete_subclass_implementing_process_file_works(self):
        class Concrete(ProcessClass):
            def process_file(self):
                return "processed"

        obj = Concrete()
        assert obj.process_file() == "processed"
