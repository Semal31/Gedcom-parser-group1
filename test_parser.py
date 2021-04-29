import pytest

from parser import *

# Generic individuals dict that should pass most tests
CORRECT_INDIVIDUALS = {
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

CORRECT_FAMILIES = {
    "@F2@": {
        "HUSB": "@I3@",
        "WIFE": "@I4@",
        "CHIL": ["@I1@", "@I5@"],
        "MARR": "8 AUG 2020",
        "DIV": "30 DEC 2018",
    }
}


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


def test_dates_before_current_valid():
    assert dates_before_current("myfamily.ged") == True


def test_dates_before_current_invalid():
    assert dates_before_current("testUS01_myfamily.ged") == False


def test_divorce_before_death_bothDead_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"], "MARR": "Y"},
        "@F4@": {
            "HUSB": "@I7@",
            "WIFE": "@I8@",
            "CHIL": ["@I4@", "@I9@", "@I10@"],
            "MARR": "Y",
        },
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"], "MARR": ""},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"], "MARR": ""},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@", "MARR": "Y"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "June /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert divorce_before_death(families, individuals) == False


def test_divorce_before_death_husbDead_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"], "MARR": "Y"},
        "@F4@": {
            "HUSB": "@I7@",
            "WIFE": "@I8@",
            "CHIL": ["@I4@", "@I9@", "@I10@"],
            "MARR": "Y",
        },
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"], "MARR": ""},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"], "MARR": ""},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@", "MARR": "Y"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert divorce_before_death(families, individuals) == False


def test_divorce_before_death_wifeDead_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"], "MARR": "Y"},
        "@F4@": {
            "HUSB": "@I7@",
            "WIFE": "@I8@",
            "CHIL": ["@I4@", "@I9@", "@I10@"],
            "MARR": "Y",
        },
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"], "MARR": ""},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"], "MARR": ""},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@", "MARR": "Y"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
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
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert divorce_before_death(families, individuals) == False


def test_divorce_before_death_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"], "MARR": "Y"},
        "@F4@": {
            "HUSB": "@I7@",
            "WIFE": "@I8@",
            "CHIL": ["@I4@", "@I9@", "@I10@"],
            "MARR": "Y",
        },
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"], "MARR": ""},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"], "MARR": ""},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@", "MARR": "Y"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert divorce_before_death(families, individuals) == True


def test_US03_valid():
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
    assert us_03(individuals) == True


def test_US03_invalid():
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2012",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2009",
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
    assert us_03(individuals) == False


def test_US08_valid():
    families = {"@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"}}
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F1@",
        }
    }
    assert us_08(families, individuals) == True


def test_US08_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "MARR": "15 APR 1999", "CHIL": "@I3@"}
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1998",
            "FAMC": "@F1@",
        }
    }
    assert us_08(families, individuals) == False


def test_US14_valid():
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "@I2@",
            "MARR": "15 APR 1999",
            "CHIL": ["@I3@", "@I4@", "@I5@", "@I6@", "@I7@"],
        }
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I4@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "3 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I5@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "7 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I6@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I7@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "5 DEC 1962",
            "FAMC": "@F1@",
        },
    }
    assert us_14(families, individuals) == True


def test_US14_invalid():
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "@I2@",
            "MARR": "15 APR 1999",
            "CHIL": ["@I3@", "@I4@", "@I5@", "@I6@", "@I7@"],
        }
    }
    individuals = {
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I4@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I5@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I6@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
        "@I7@": {
            "NAME": "Michael /Cooke/",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "FAMC": "@F1@",
        },
    }
    assert us_14(families, individuals) == False


def test_US19_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "", "MARR": "15 APR 1999"},
        "@F2@": {"HUSB": "@I2@", "WIFE": "", "MARR": "15 APR 1999"},
        "@F3@": {"HUSB": "@I3@", "WIFE": "", "MARR": "15 APR 1999"},
        "@F4@": {"HUSB": "@I4@", "WIFE": "@I5@", "MARR": "15 APR 1999"},
    }
    individuals = {
        "@I1@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMS": "@F1@",
        },
        "@I2@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F1@",
            "FAMS": "@F2@",
        },
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMS": "@F3@",
        },
        "@I4@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F2@",
            "FAMS": "@F4@",
        },
        "@I5@": {
            "NAME": "Michael /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F3@",
            "FAMS": "@F4@",
        },
    }
    assert us_19(families, individuals) == True


def test_US19_invalid():
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "",
            "MARR": "15 APR 1999",
            "CHIL": ["@I2@", "@I3@"],
        },
        "@F2@": {"HUSB": "@I2@", "WIFE": "", "MARR": "15 APR 1999", "CHIL": ["@I4@"]},
        "@F3@": {"HUSB": "@I3@", "WIFE": "", "MARR": "15 APR 1999", "CHIL": ["@I5@"]},
        "@F4@": {"HUSB": "@I4@", "WIFE": "@I5@", "MARR": "15 APR 1999"},
    }
    individuals = {
        "@I1@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMS": "@F1@",
        },
        "@I2@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F1@",
            "FAMS": "@F2@",
        },
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F1@",
            "FAMS": "@F3@",
        },
        "@I4@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F2@",
            "FAMS": "@F4@",
        },
        "@I5@": {
            "NAME": "Michael /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "FAMC": "@F3@",
            "FAMS": "@F4@",
        },
    }
    assert us_19(families, individuals) == False


def test_US16_valid():
    # Male last names
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I1@",
            "WIFE": "@I4@",
            "CHIL": ["@I2@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I1@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I2@": {
            "NAME": "Henry /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I5@": {
            "NAME": "Diana /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 2000",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert us_16(families, individuals) == True


def test_US16_invalid():
    # Male last names
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I1@",
            "WIFE": "@I4@",
            "CHIL": ["@I2@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I1@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I2@": {
            "NAME": "Henry /Smith/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I5@": {
            "NAME": "Diana /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 2000",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert us_16(families, individuals) == False


def test_US21_valid():
    # Correct gender for role
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I1@",
            "WIFE": "@I4@",
            "CHIL": ["@I2@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I1@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I2@": {
            "NAME": "Diana /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 2000",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
        "@I4@": {
            "NAME": "Theresa /Fox/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
    }
    assert us_21(families, individuals) == True


def test_US21_invalid():
    # Correct gender for role
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I1@",
            "WIFE": "@I4@",
            "CHIL": ["@I2@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I1@": {
            "NAME": "Michael /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I2@": {
            "NAME": "Diana /Cooke/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 2000",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
        "@I4@": {
            "NAME": "Theresa /Fox/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2000",
            "DEAT": "",
            "DEATH_DATE": "9 SEP 2007",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
    }
    assert us_21(families, individuals) == False


def test_fewer_than_15_children_correct():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "MARR": "15 APR 1999", "CHIL": "@I3@"}
    }
    assert fewer_than_15_children(families) == True


def test_fewer_than_15_children_incorrect():
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "@I2@",
            "MARR": "15 APR 1999",
            "CHIL": [
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
                "@I2@",
                "@I5@",
            ],
        }
    }
    assert fewer_than_15_children(families) == False


def test_uncle_aunts_cannot_marry_nieces_nephews_correct():
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
        "@I1@": {
            "NAME": "Ryan /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "11 NOV 1999",
            "FAMS": "@F9@",
            "FAMC": "@F2@",
        },
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "June /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
            "FAMS": "@F2@",
            "FAMC": "@F4@",
        },
    }
    assert uncle_aunts_cannot_marry_nieces_nephews(families, individuals) == True


def test_uncle_aunts_cannot_marry_nieces_nephews_incorrect():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {
            "HUSB": "@I11@",
            "WIFE": "@I12@",
            "CHIL": ["@I3@", "@I2@"],
            "MARR": "Y",
        },
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
            "FAMC": "@F3@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
            "FAMS": "@F2@",
            "FAMC": "@F3@",
        },
        "@I4@": {
            "NAME": "June /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "1 OCT 1970",
            "DEAT": "",
            "DEATH_DATE": "5 APR 1600",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert uncle_aunts_cannot_marry_nieces_nephews(families, individuals) == False


def test_siblings_spacing_correct():
    assert siblings_could_be_born(CORRECT_INDIVIDUALS, CORRECT_FAMILIES) == True


def test_siblings_spacing_incorrect():
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
            "DATE": "16 NOV 1999",
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
            "DATE": "16 NOV 1999",  # Should fail here
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    families = {
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        }
    }
    assert siblings_could_be_born(individuals, families) == False


def test_incest_among_siblings_correct():
    assert siblings_do_not_marry(CORRECT_INDIVIDUALS, CORRECT_FAMILIES) == True


def test_incest_among_siblings_incorrect():
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
            "DATE": "16 NOV 1999",  # Should fail here
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
    families = {
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {
            "HUSB": "@I1@",
            "WIFE": "@I5@",
            "CHIL": [],
            "MARR": "8 AUG 2020",
            "DIV": "30 DEC 2018",
        },
    }
    assert siblings_do_not_marry(individuals, families) == False


# US12
def test_parents_not_too_old_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"]},
        "@F4@": {"HUSB": "@I7@", "WIFE": "@I8@", "CHIL": ["@I4@", "@I9@", "@I10@"]},
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"]},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"]},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert parents_not_too_old(families, individuals) == True


def test_parents_not_too_old_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"]},
        "@F4@": {"HUSB": "@I7@", "WIFE": "@I8@", "CHIL": ["@I4@", "@I9@", "@I10@"]},
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"]},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"]},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1837",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert parents_not_too_old(families, individuals) == False


# US17
def test_check_marriage_to_descendants_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"]},
        "@F4@": {"HUSB": "@I7@", "WIFE": "@I8@", "CHIL": ["@I4@", "@I9@", "@I10@"]},
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"]},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"]},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
    }
    assert check_marriage_to_descendants(families) == True


def test_check_marriage_to_descendants_invalid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I5@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"]},
        "@F4@": {"HUSB": "@I7@", "WIFE": "@I8@", "CHIL": ["@I4@", "@I9@", "@I10@"]},
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I17@", "CHIL": ["@I7@"]},
        "@F7@": {"HUSB": "@I8@", "WIFE": "@I14@", "CHIL": ["@I8@"]},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
    }
    assert check_marriage_to_descendants(families) == False


def test_unique_names():
    assert names_are_unique(CORRECT_INDIVIDUALS) == True


def test_unique_names_invalid():
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
        "@I6@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "29 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    assert names_are_unique(individuals) == False


def test_unique_names_duplicate():
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
        "@I6@": {
            "NAME": "Thomas /Hartmans/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "29 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    assert names_are_unique(individuals) == True


def test_no_deceased():
    assert list_deceased(CORRECT_INDIVIDUALS) == 0


def test_deceased():
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
        "@I6@": {
            "NAME": "Thomas /Hartmans/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "29 JUL 1995",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
            "DEATH_DATE": "04 APR 2021",
        },
    }
    assert list_deceased(individuals) == 1


def test_list_over_30_and_single_valid():
    assert list_over_30_and_single(CORRECT_INDIVIDUALS) == True


def test_list_over_30_and_single_valid():
    individuals = {
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert list_over_30_and_single(individuals) == False


def test_order_siblings_by_age_multiple_siblings():
    families = {
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I5@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F4@": {"HUSB": "@I7@", "WIFE": "@I8@", "CHIL": ["@I4@", "@I9@", "@I10@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert order_siblings_by_age(families, individuals) == True


def test_order_siblings_by_age_no_siblings():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "@I2@", "DATE": "15 APR 1999"},
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
        "@F3@": {"HUSB": "@I11@", "WIFE": "@I12@", "CHIL": ["@I3@"]},
        "@F4@": {"HUSB": "@I7@", "WIFE": "@I8@", "CHIL": ["@I4@", "@I9@", "@I10@"]},
        "@F5@": {"HUSB": "@I5@", "WIFE": "@I6@", "DATE": "31 JUL 2020"},
        "@F6@": {"HUSB": "@I15@", "WIFE": "@I16@", "CHIL": ["@I7@"]},
        "@F7@": {"HUSB": "@I13@", "WIFE": "@I14@", "CHIL": ["@I8@"]},
        "@F8@": {"HUSB": "@I17@", "WIFE": "@I16@"},
        "@F9@": {"HUSB": "@I1@", "CHIL": ["@I18@"]},
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
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "30 APR 1999",
            "FAMS": "@F1@",
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
        "@I6@": {
            "NAME": "Felisha /Kissel/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "12 MAY 1994",
            "FAMS": "@F5@",
        },
        "@I7@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "3 NOV 1949",
            "FAMS": "@F4@",
            "FAMC": "@F6@",
        },
        "@I8@": {
            "NAME": "June /Vanderzee/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "4 APR 1950",
            "FAMS": "@F4@",
            "FAMC": "@F7@",
        },
        "@I9@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "27 SEP 1972",
            "FAMC": "@F4@",
        },
        "@I10@": {
            "NAME": "Lynn-marie /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 AUG 1976",
            "FAMC": "@F4@",
        },
        "@I11@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "8 JAN 1930",
            "DEAT": "Y",
            "DEATH_DATE": "6 JAN 1990",
            "FAMS": "@F3@",
        },
        "@I12@": {
            "NAME": "Leona /Layton/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "5 AUG 1936",
            "FAMS": "@F3@",
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
        "@I15@": {
            "NAME": "Peter /Lagaveen/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 MAR 1916",
            "DEAT": "Y",
            "DEATH_DATE": "8 JUN 1966",
            "FAMS": "@F6@",
        },
        "@I16@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "29 MAY 1914",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2005",
            "FAMS": "@F8@",
        },
        "@I17@": {
            "NAME": "Gerrit /Dijkstra/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "13 SEP 1920",
            "DEAT": "Y",
            "DEATH_DATE": "11 SEP 2001",
            "FAMS": "@F8@",
        },
        "@I18@": {
            "NAME": "Sage /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUN 2020",
            "FAMC": "@F9@",
        },
    }
    assert order_siblings_by_age(families, individuals) == False


def test_check_unique_ids_valid():
    assert check_unique_ids("myfamily.ged") == True


def test_check_unique_ids_invalid():
    assert check_unique_ids("testUS22_myfamily.ged") == False


def test_US27():
    assert us_27(CORRECT_INDIVIDUALS) == True


def test_US32_valid():
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
            "DATE": "11 NOV 1999",
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
            "DATE": "1 OCT 1970",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    assert us_32(individuals) == True


def test_US32_invalid():
    assert us_32(CORRECT_INDIVIDUALS) == False


def test_US24_valid():
    families = {
        "@F1@": {"HUSB": "@I1@", "WIFE": "", "DATE": "15 APR 1999"},
        "@F2@": {"HUSB": "@I2@", "WIFE": "", "DATE": "15 APR 1999"},
        "@F3@": {"HUSB": "@I3@", "WIFE": "", "DATE": "15 APR 1999"},
        "@F4@": {"HUSB": "@I4@", "WIFE": "@I5@", "DATE": "15 APR 1999"},
    }
    assert us_24(families) == True


def test_US24_invalid():
    families = {
        "@F2@": {
            "HUSB": "@I2@",
            "WIFE": "@I1@",
            "MARR": "15 APR 1999",
            "CHIL": ["@I4@"],
        },
        "@F3@": {
            "HUSB": "@I2@",
            "WIFE": "@I1@",
            "MARR": "15 APR 1999",
            "CHIL": ["@I4@"],
        },
        "@F4@": {"HUSB": "@I4@", "WIFE": "@I5@", "MARR": "15 APR 1999"},
    }
    assert us_24(families) == False


def test_list_upcoming_birthdays_valid():
    individuals = {
        "@I1@": {
            "NAME": "Ryan /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "21 MAY 1999",
            "FAMS": "@F9@",
            "FAMC": "@F2@",
        },
        "@I2@": {
            "NAME": "June /Hartman/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 MAY 1970",
            "FAMS": "@F4@",
            "FAMC": "@F1@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "20 APR 2005",
            "FAMS": "@F9@",
            "FAMC": "@F2@",
        },
    }
    assert list_upcoming_birthdays(individuals) == True


def test_list_upcoming_birthdays_invalid():
    assert list_upcoming_birthdays(CORRECT_INDIVIDUALS) == False


def test_list_orphans_valid():
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "@I2@",
            "CHIL": ["@I3@", "@I4@"],
            "DATE": "15 APR 1999",
        },
        "@F2@": {
            "HUSB": "@I4@",
            "WIFE": "@I5@",
            "MARR": "8 AUG 1991",
            "DIV": "30 DEC 2018",
        },
    }
    individuals = {
        "@I1@": {
            "NAME": "Ryan /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "11 NOV 1970",
            "DEAT": "Y",
            "FAMS": "@F1@",
            "FAMC": "@F2@",
        },
        "@I2@": {
            "NAME": "Beatrice /Meyne/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "11 NOV 1970",
            "DEAT": "Y",
            "FAMS": "@F1@",
            "FAMC": "@F2@",
        },
        "@I3@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 2005",
            "FAMC": "@F1@",
        },
        "@I4@": {
            "NAME": "June /Lagaveen/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "2 DEC 2017",
            "FAMC": "@F1@",
        },
    }
    assert list_orphans(families, individuals) == True


def test_list_orphans_invalid():
    assert list_orphans(CORRECT_FAMILIES, CORRECT_INDIVIDUALS) == False


def test_list_death_in_last_30_days_valid():
    individuals = {
        "@I13@": {
            "NAME": "Peter /Vanderzee/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUL 1911",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2020",
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
    assert list_death_in_last_30_days(individuals) == False


def test_list_death_in_last_30_days_invalid():
    individuals = {
        "@I13@": {
            "NAME": "Peter /Vanderzee/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 JUL 1911",
            "DEAT": "Y",
            "DEATH_DATE": "26 APR 2021",
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
    assert list_death_in_last_30_days(individuals) == True


def test_us37_valid():
    assert us_37(CORRECT_FAMILIES, CORRECT_INDIVIDUALS) == False


def test_us37_invalid():
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
        "@I1@": {
            "NAME": "Wyett /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 OCT 1998",
            "FAM": "@F2@",
        },
        "@I3@": {
            "NAME": "Michael /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "2 DEC 1962",
            "DEAT": "",
            "DEATH_DATE": "16 APR 2021",
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
        "@I5@": {
            "NAME": "Wyett /Cooke/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "10 OCT 1998",
            "FAM": "@F2@",
        },
    }
    assert us_37(families, individuals) == True


def test_us42_valid():
    assert us_42(CORRECT_FAMILIES, CORRECT_INDIVIDUALS) == True


def test_us42_invalid():
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
            "DATE": "39 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    families = {
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "CHIL": ["@I1@", "@I5@"],
            "MARR": "38 AUG 2020",
            "DIV": "33 DEC 2018",
        }
    }
    assert us_42(families, individuals) == False


def test_list_anniversaries():
    individuals = {
        "@I1@": {
            "NAME": "Ryan /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "11 NOV 1999",
            "FAMS": "@F9@",
            "FAMC": "@F2@",
        },
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "15 APR 1999",
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
            "DATE": "39 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
        "@I6@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "39 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "@I2@",
            "MARR": "28 MAY 2020",
        },
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "MARR": "28 NOV 1927",
        },
        "@F3@": {
            "HUSB": "@I5@",
            "WIFE": "@I6@",
            "MARR": "2 MAY 1999",
        },
    }
    assert list_upcoming_anniversaries(individuals, families) == 2


def test_list_large_age_differences():
    individuals = {
        "@I1@": {
            "NAME": "Ryan /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "11 NOV 2020",
            "FAMS": "@F9@",
            "FAMC": "@F2@",
        },
        "@I2@": {
            "NAME": "Alyssa /Bottesi/",
            "SEX": "F",
            "BIRT": "",
            "DATE": "10 NOV 2019",
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
            "DATE": "12 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
        "@I6@": {
            "NAME": "Thomas /Hartman/",
            "SEX": "M",
            "BIRT": "",
            "DATE": "12 JUL 1994",
            "FAMS": "@F5@",
            "FAMC": "@F2@",
        },
    }
    families = {
        "@F1@": {
            "HUSB": "@I1@",
            "WIFE": "@I2@",
            "MARR": "28 MAY 2020",
        },
        "@F2@": {
            "HUSB": "@I3@",
            "WIFE": "@I4@",
            "MARR": "28 NOV 1927",
        },
        "@F3@": {
            "HUSB": "@I5@",
            "WIFE": "@I6@",
            "MARR": "2 MAY 1999",
        },
    }
    assert list_large_age_differences(individuals, families) == 1
