from enum import auto

from pandos.utils.custom_enum_types import TextEnum


def test_enum_instance():

    class ABC(TextEnum):
        A = auto()
        B = auto()
        C = auto()

    assert ABC.A.value == "a"
    assert ABC.B.value == "b"
    assert ABC.C.value == "c"
