"""Test HTAN Validator class."""
from hdash.validator import htan_validator


def test_validator():
    file_list = []
    file_list.append("tests/data/demographics.csv")
    validator = htan_validator.HtanValidator("HTA3", file_list)
    validation_list = validator.get_validation_list()
    assert len(validation_list) > 2
    validation1 = validation_list[0]
    assert validation1.validation_passed is True
    validation2 = validation_list[1]
    assert validation2.validation_passed is True
