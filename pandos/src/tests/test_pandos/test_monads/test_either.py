from pandos.monads import Either, Right, Left


class CustomTestError(Exception):

    @classmethod
    def raise_error(cls, *args, **kwargs):
        raise cls(*args, **kwargs)


def test_either_from_value():
    value = 5
    instance = Either.from_value(x=value)
    assert instance.map(lambda x: x == value).resolve()


def test_either_right_map():
    def add_one(x) -> int:
        return x + 1
    value = 5
    either_in = Either.from_value(x=value)
    either_out = either_in.map(add_one)
    assert isinstance(either_out, Right)
    assert either_out.resolve() == add_one(either_in.resolve())


def test_either_left_map():
    def zero_div(x):
        return x / 0

    value = 5
    either_in = Either.from_value(x=value)
    either_out = either_in.map(zero_div)
    try:
        zero_div(value)
        raise ValueError("Transformation should've failed")
    except ZeroDivisionError as e:
        assert isinstance(either_out, Left)


def test_either_sticky_left():
    either_in = Either.from_value(x=0)\
        .map(lambda x: CustomTestError.raise_error())
    either_out = either_in.map(lambda x: x + 1)
    assert isinstance(either_in, Left)
    assert isinstance(either_out, Left)


def test_either_right_flatmap():
    # TODO: Add test for right flatmap
    pass


def test_either_left_flatmap():
    # TODO: Add test for left flatmap
    pass
