"""Test HTAN Validator class."""
from hdash.validator import htan_validator


def test_validator():
    file_list = []
    file_list.append("tests/data/demographics.csv")
    file_list.append("tests/data/biospecimens.csv")
    validator = htan_validator.HtanValidator("HTA3", file_list)
    validation_list = validator.get_validation_list()
    assert len(validation_list) == 5
    validation0 = validation_list[0]
    assert validation0.validation_passed is True
    validation1 = validation_list[1]
    assert validation1.validation_passed is False
    error_list = validation1.error_list
    assert error_list[0] == "HTA3_2A does not match HTAN spec."
    assert error_list[1] == "HTA3_3_3 does not match HTAN spec."

    validation4 = validation_list[4]
    assert validation4.validation_passed is False
    error_list = validation4.error_list
    assert error_list[0].startswith("Biospecimen refers to parent ID:  HTA3")
