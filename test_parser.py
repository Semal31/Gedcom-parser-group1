import pytest

from parser import (
    check_marriage_divorce_dates,
    children_before_death,
    us_05,
    us_10,
    check_birth_before_marriage,
    check_age,
)


def test_check_marriage_divorce_dates_with_correct_dates():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {}
    assert check_marriage_divorce_dates(families, individuals) == True


def test_check_marriage_divorce_dates_with_incorrect_dates():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "June /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert check_marriage_divorce_dates(families, individuals) == False


def test_children_before_death_with_correct_families():
    families = {
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        }
    }
    individuals = {
        "@I1@": {
            "NAME": "Ryan /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "11 NOV 1999",
            "FAMS": "@F9@",
            "FAMC": "@F2@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "June /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
        "@I5@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "29 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    assert children_before_death(families, individuals) == True


def test_children_before_death_with_incorrect_families():
    families = {
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"], "MARR": ""}
    }
    individuals = {
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 2020",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I13@": {
            "NAME": "Peter /Vanderzee/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUL 1911",
            "DEAT": "Y",
            "DEATH_DATE": "26 NOV 1986",
            "FAMS": "@F7@",
        },
        "@I14@": {
            "NAME": "Olive /Heritage/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "7 JUN 1919",
            "DEAT": "Y",
            "DEATH_DATE": "13 OCT 2009",
            "FAMS": "@F7@",
        },
    }
    assert children_before_death(families, individuals) == False


def test_US05_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert us_05(families, individuals) == True


def test_US05_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert us_05(families, individuals) == False


def test_US10_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert us_10(families, individuals) == True


def test_US10_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2012",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2020",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert us_10(families, individuals) == False


def test_check_birth_before_marriage_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2012",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2020",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert check_birth_before_marriage(families, individuals) == True


def test_check_birth_before_marriage_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1802",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2012",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2020",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert check_birth_before_marriage(families, individuals) == False


def test_check_age_valid():
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2012",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2020",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 JAN 1872",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert check_age(individuals) == True


def test_check_age_invalid():
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2012",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2020",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "Diana /Chaney/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 JAN 1871",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert check_age(individuals) == False
