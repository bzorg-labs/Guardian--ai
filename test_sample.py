
from sample import check_number


def test_positive_number():
    assert check_number(5) == "positive"


def test_negative_number():
    assert check_number(-3) == "negative"


def test_zero_number():
    assert check_number(0) == "zero"