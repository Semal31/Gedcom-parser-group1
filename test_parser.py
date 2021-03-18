import pytest

from parser import (
    check_marriage_divorce_dates,
    children_before_death,
    us_05,
    us_10,
    check_birth_before_marriage,
    check_age,
    dates_before_current,
    divorce_before_death,
    us_03,
    us_08
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
    
def test_dates_before_current_valid():
    assert dates_before_current(myfamily.ged) == True
def test_dates_before_current_invalid():
    assert dates_before_current(testUS01_myfamily.ged) == False
    
def test_divorce_before_death_bothDead_invalid():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'DATE': '15 APR 1999'}, '@F2@': {'HUSB': '@I3@', 'WIFE': '@I4@', 'CHIL': ['@I1@', '@I5@'], 'MARR': '8 AUG 1991', 'DIV': '30 DEC 2018'}, '@F3@': {'HUSB': '@I11@', 'WIFE': '@I12@', 'CHIL': ['@I3@'], 'MARR': 'Y'}, '@F4@': {'HUSB': '@I7@', 'WIFE': '@I8@', 'CHIL': ['@I4@', '@I9@', '@I10@'], 'MARR': 'Y'}, '@F5@': {'HUSB': '@I5@', 'WIFE': '@I6@', 'DATE': '31 JUL 2020'}, '@F6@': {'HUSB': '@I15@', 'WIFE': '@I16@', 'CHIL': ['@I7@'], 'MARR': ''}, '@F7@': {'HUSB': '@I13@', 'WIFE': '@I14@', 'CHIL': ['@I8@'], 'MARR': ''}, '@F8@': {'HUSB': '@I17@', 'WIFE': '@I16@', 'MARR': 'Y'}, '@F9@': {'HUSB': '@I1@', 'CHIL': ['@I18@']}}
    individuals = {'@I1@': {'NAME': 'Ryan /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '11 NOV 1999', 'FAMS': '@F9@', 'FAMC': '@F2@'}, '@I2@': {'NAME': 'Alyssa /Bottesi/', 'SEX': 'F', 'BIRT': '', 'DATE': '30 APR 1999', 'FAMS': '@F1@'}, '@I3@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1962', 'DEAT': '', 'DEATH_DATE': '5 APR 1600', 'FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'June /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'DEAT': '', 'DEATH_DATE': '5 APR 1600', 'FAMS': '@F2@', 'FAMC': '@F4@'}, '@I5@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '29 JUL 1994', 'FAMS': '@F5@', 'FAMC': '@F2@'}, '@I6@': {'NAME': 'Felisha /Kissel/', 'SEX': 'F', 'BIRT': '', 'DATE': '12 MAY 1994', 'FAMS': '@F5@'}, '@I7@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '3 NOV 1949', 'FAMS': '@F4@', 'FAMC': '@F6@'}, '@I8@': {'NAME': 'June /Vanderzee/', 'SEX': 'F', 'BIRT': '', 'DATE': '4 APR 1950', 'FAMS': '@F4@', 'FAMC': '@F7@'}, '@I9@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '27 SEP 1972', 'FAMC': '@F4@'}, '@I10@': {'NAME': 'Lynn-marie /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '10 AUG 1976', 'FAMC': '@F4@'}, '@I11@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '8 JAN 1930', 'DEAT': 'Y', 'DEATH_DATE': '6 JAN 1990', 'FAMS': '@F3@'}, '@I12@': {'NAME': 'Leona /Layton/', 'SEX': 'F', 'BIRT': '', 'DATE': '5 AUG 1936', 'FAMS': '@F3@'}, '@I13@': {'NAME': 'Peter /Vanderzee/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUL 1911', 'DEAT': 'Y', 'DEATH_DATE': '26 NOV 1986', 'FAMS': '@F7@'}, '@I14@': {'NAME': 'Olive /Heritage/', 'SEX': 'F', 'BIRT': '', 'DATE': '7 JUN 1919', 'DEAT': 'Y', 'DEATH_DATE': '13 OCT 2009', 'FAMS': '@F7@'}, '@I15@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 MAR 1916', 'DEAT': 'Y', 'DEATH_DATE': '8 JUN 1966', 'FAMS': '@F6@'}, '@I16@': {'NAME': 'Beatrice /Meyne/', 'SEX': 'F', 'BIRT': '', 'DATE': '29 MAY 1914', 'DEAT': 'Y', 'DEATH_DATE': '26 APR 2005', 'FAMS': '@F8@'}, '@I17@': {'NAME': 'Gerrit /Dijkstra/', 'SEX': 'M', 'BIRT': '', 'DATE': '13 SEP 1920', 'DEAT': 'Y', 'DEATH_DATE': '11 SEP 2001', 'FAMS': '@F8@'}, '@I18@': {'NAME': 'Sage /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUN 2020', 'FAMC': '@F9@'}}
    assert divorce_before_death(families, individuals) == False
def test_divorce_before_death_husbDead_invalid():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'DATE': '15 APR 1999'}, '@F2@': {'HUSB': '@I3@', 'WIFE': '@I4@', 'CHIL': ['@I1@', '@I5@'], 'MARR': '8 AUG 1991', 'DIV': '30 DEC 2018'}, '@F3@': {'HUSB': '@I11@', 'WIFE': '@I12@', 'CHIL': ['@I3@'], 'MARR': 'Y'}, '@F4@': {'HUSB': '@I7@', 'WIFE': '@I8@', 'CHIL': ['@I4@', '@I9@', '@I10@'], 'MARR': 'Y'}, '@F5@': {'HUSB': '@I5@', 'WIFE': '@I6@', 'DATE': '31 JUL 2020'}, '@F6@': {'HUSB': '@I15@', 'WIFE': '@I16@', 'CHIL': ['@I7@'], 'MARR': ''}, '@F7@': {'HUSB': '@I13@', 'WIFE': '@I14@', 'CHIL': ['@I8@'], 'MARR': ''}, '@F8@': {'HUSB': '@I17@', 'WIFE': '@I16@', 'MARR': 'Y'}, '@F9@': {'HUSB': '@I1@', 'CHIL': ['@I18@']}}
    individuals = {'@I1@': {'NAME': 'Ryan /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '11 NOV 1999', 'FAMS': '@F9@', 'FAMC': '@F2@'}, '@I2@': {'NAME': 'Alyssa /Bottesi/', 'SEX': 'F', 'BIRT': '', 'DATE': '30 APR 1999', 'FAMS': '@F1@'}, '@I3@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1962', 'DEAT': '', 'DEATH_DATE': '5 APR 1600', 'FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'June /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'FAMS': '@F2@', 'FAMC': '@F4@'}, '@I5@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '29 JUL 1994', 'FAMS': '@F5@', 'FAMC': '@F2@'}, '@I6@': {'NAME': 'Felisha /Kissel/', 'SEX': 'F', 'BIRT': '', 'DATE': '12 MAY 1994', 'FAMS': '@F5@'}, '@I7@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '3 NOV 1949', 'FAMS': '@F4@', 'FAMC': '@F6@'}, '@I8@': {'NAME': 'June /Vanderzee/', 'SEX': 'F', 'BIRT': '', 'DATE': '4 APR 1950', 'FAMS': '@F4@', 'FAMC': '@F7@'}, '@I9@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '27 SEP 1972', 'FAMC': '@F4@'}, '@I10@': {'NAME': 'Lynn-marie /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '10 AUG 1976', 'FAMC': '@F4@'}, '@I11@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '8 JAN 1930', 'DEAT': 'Y', 'DEATH_DATE': '6 JAN 1990', 'FAMS': '@F3@'}, '@I12@': {'NAME': 'Leona /Layton/', 'SEX': 'F', 'BIRT': '', 'DATE': '5 AUG 1936', 'FAMS': '@F3@'}, '@I13@': {'NAME': 'Peter /Vanderzee/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUL 1911', 'DEAT': 'Y', 'DEATH_DATE': '26 NOV 1986', 'FAMS': '@F7@'}, '@I14@': {'NAME': 'Olive /Heritage/', 'SEX': 'F', 'BIRT': '', 'DATE': '7 JUN 1919', 'DEAT': 'Y', 'DEATH_DATE': '13 OCT 2009', 'FAMS': '@F7@'}, '@I15@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 MAR 1916', 'DEAT': 'Y', 'DEATH_DATE': '8 JUN 1966', 'FAMS': '@F6@'}, '@I16@': {'NAME': 'Beatrice /Meyne/', 'SEX': 'F', 'BIRT': '', 'DATE': '29 MAY 1914', 'DEAT': 'Y', 'DEATH_DATE': '26 APR 2005', 'FAMS': '@F8@'}, '@I17@': {'NAME': 'Gerrit /Dijkstra/', 'SEX': 'M', 'BIRT': '', 'DATE': '13 SEP 1920', 'DEAT': 'Y', 'DEATH_DATE': '11 SEP 2001', 'FAMS': '@F8@'}, '@I18@': {'NAME': 'Sage /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUN 2020', 'FAMC': '@F9@'}}
    assert divorce_before_death(families, individuals) == False
def test_divorce_before_death_wifeDead_invalid():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'DATE': '15 APR 1999'}, '@F2@': {'HUSB': '@I3@', 'WIFE': '@I4@', 'CHIL': ['@I1@', '@I5@'], 'MARR': '8 AUG 1991', 'DIV': '30 DEC 2018'}, '@F3@': {'HUSB': '@I11@', 'WIFE': '@I12@', 'CHIL': ['@I3@'], 'MARR': 'Y'}, '@F4@': {'HUSB': '@I7@', 'WIFE': '@I8@', 'CHIL': ['@I4@', '@I9@', '@I10@'], 'MARR': 'Y'}, '@F5@': {'HUSB': '@I5@', 'WIFE': '@I6@', 'DATE': '31 JUL 2020'}, '@F6@': {'HUSB': '@I15@', 'WIFE': '@I16@', 'CHIL': ['@I7@'], 'MARR': ''}, '@F7@': {'HUSB': '@I13@', 'WIFE': '@I14@', 'CHIL': ['@I8@'], 'MARR': ''}, '@F8@': {'HUSB': '@I17@', 'WIFE': '@I16@', 'MARR': 'Y'}, '@F9@': {'HUSB': '@I1@', 'CHIL': ['@I18@']}}
    individuals = {'@I1@': {'NAME': 'Ryan /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '11 NOV 1999', 'FAMS': '@F9@', 'FAMC': '@F2@'}, '@I2@': {'NAME': 'Alyssa /Bottesi/', 'SEX': 'F', 'BIRT': '', 'DATE': '30 APR 1999', 'FAMS': '@F1@'}, '@I3@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1962', 'FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'June /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'DEAT': '', 'DEATH_DATE': '5 APR 1600', 'FAMS': '@F2@', 'FAMC': '@F4@'}, '@I5@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '29 JUL 1994', 'FAMS': '@F5@', 'FAMC': '@F2@'}, '@I6@': {'NAME': 'Felisha /Kissel/', 'SEX': 'F', 'BIRT': '', 'DATE': '12 MAY 1994', 'FAMS': '@F5@'}, '@I7@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '3 NOV 1949', 'FAMS': '@F4@', 'FAMC': '@F6@'}, '@I8@': {'NAME': 'June /Vanderzee/', 'SEX': 'F', 'BIRT': '', 'DATE': '4 APR 1950', 'FAMS': '@F4@', 'FAMC': '@F7@'}, '@I9@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '27 SEP 1972', 'FAMC': '@F4@'}, '@I10@': {'NAME': 'Lynn-marie /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '10 AUG 1976', 'FAMC': '@F4@'}, '@I11@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '8 JAN 1930', 'DEAT': 'Y', 'DEATH_DATE': '6 JAN 1990', 'FAMS': '@F3@'}, '@I12@': {'NAME': 'Leona /Layton/', 'SEX': 'F', 'BIRT': '', 'DATE': '5 AUG 1936', 'FAMS': '@F3@'}, '@I13@': {'NAME': 'Peter /Vanderzee/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUL 1911', 'DEAT': 'Y', 'DEATH_DATE': '26 NOV 1986', 'FAMS': '@F7@'}, '@I14@': {'NAME': 'Olive /Heritage/', 'SEX': 'F', 'BIRT': '', 'DATE': '7 JUN 1919', 'DEAT': 'Y', 'DEATH_DATE': '13 OCT 2009', 'FAMS': '@F7@'}, '@I15@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 MAR 1916', 'DEAT': 'Y', 'DEATH_DATE': '8 JUN 1966', 'FAMS': '@F6@'}, '@I16@': {'NAME': 'Beatrice /Meyne/', 'SEX': 'F', 'BIRT': '', 'DATE': '29 MAY 1914', 'DEAT': 'Y', 'DEATH_DATE': '26 APR 2005', 'FAMS': '@F8@'}, '@I17@': {'NAME': 'Gerrit /Dijkstra/', 'SEX': 'M', 'BIRT': '', 'DATE': '13 SEP 1920', 'DEAT': 'Y', 'DEATH_DATE': '11 SEP 2001', 'FAMS': '@F8@'}, '@I18@': {'NAME': 'Sage /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUN 2020', 'FAMC': '@F9@'}}
    assert divorce_before_death(families, individuals) == False
def test_divorce_before_death_valid():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'DATE': '15 APR 1999'}, '@F2@': {'HUSB': '@I3@', 'WIFE': '@I4@', 'CHIL': ['@I1@', '@I5@'], 'MARR': '8 AUG 1991', 'DIV': '30 DEC 2018'}, '@F3@': {'HUSB': '@I11@', 'WIFE': '@I12@', 'CHIL': ['@I3@'], 'MARR': 'Y'}, '@F4@': {'HUSB': '@I7@', 'WIFE': '@I8@', 'CHIL': ['@I4@', '@I9@', '@I10@'], 'MARR': 'Y'}, '@F5@': {'HUSB': '@I5@', 'WIFE': '@I6@', 'DATE': '31 JUL 2020'}, '@F6@': {'HUSB': '@I15@', 'WIFE': '@I16@', 'CHIL': ['@I7@'], 'MARR': ''}, '@F7@': {'HUSB': '@I13@', 'WIFE': '@I14@', 'CHIL': ['@I8@'], 'MARR': ''}, '@F8@': {'HUSB': '@I17@', 'WIFE': '@I16@', 'MARR': 'Y'}, '@F9@': {'HUSB': '@I1@', 'CHIL': ['@I18@']}}
    individuals = {'@I1@': {'NAME': 'Ryan /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '11 NOV 1999', 'FAMS': '@F9@', 'FAMC': '@F2@'}, '@I2@': {'NAME': 'Alyssa /Bottesi/', 'SEX': 'F', 'BIRT': '', 'DATE': '30 APR 1999', 'FAMS': '@F1@'}, '@I3@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1962', 'FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'June /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'FAMS': '@F2@', 'FAMC': '@F4@'}, '@I5@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '29 JUL 1994', 'FAMS': '@F5@', 'FAMC': '@F2@'}, '@I6@': {'NAME': 'Felisha /Kissel/', 'SEX': 'F', 'BIRT': '', 'DATE': '12 MAY 1994', 'FAMS': '@F5@'}, '@I7@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '3 NOV 1949', 'FAMS': '@F4@', 'FAMC': '@F6@'}, '@I8@': {'NAME': 'June /Vanderzee/', 'SEX': 'F', 'BIRT': '', 'DATE': '4 APR 1950', 'FAMS': '@F4@', 'FAMC': '@F7@'}, '@I9@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '27 SEP 1972', 'FAMC': '@F4@'}, '@I10@': {'NAME': 'Lynn-marie /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '10 AUG 1976', 'FAMC': '@F4@'}, '@I11@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '8 JAN 1930', 'DEAT': 'Y', 'DEATH_DATE': '6 JAN 1990', 'FAMS': '@F3@'}, '@I12@': {'NAME': 'Leona /Layton/', 'SEX': 'F', 'BIRT': '', 'DATE': '5 AUG 1936', 'FAMS': '@F3@'}, '@I13@': {'NAME': 'Peter /Vanderzee/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUL 1911', 'DEAT': 'Y', 'DEATH_DATE': '26 NOV 1986', 'FAMS': '@F7@'}, '@I14@': {'NAME': 'Olive /Heritage/', 'SEX': 'F', 'BIRT': '', 'DATE': '7 JUN 1919', 'DEAT': 'Y', 'DEATH_DATE': '13 OCT 2009', 'FAMS': '@F7@'}, '@I15@': {'NAME': 'Peter /Lagaveen/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 MAR 1916', 'DEAT': 'Y', 'DEATH_DATE': '8 JUN 1966', 'FAMS': '@F6@'}, '@I16@': {'NAME': 'Beatrice /Meyne/', 'SEX': 'F', 'BIRT': '', 'DATE': '29 MAY 1914', 'DEAT': 'Y', 'DEATH_DATE': '26 APR 2005', 'FAMS': '@F8@'}, '@I17@': {'NAME': 'Gerrit /Dijkstra/', 'SEX': 'M', 'BIRT': '', 'DATE': '13 SEP 1920', 'DEAT': 'Y', 'DEATH_DATE': '11 SEP 2001', 'FAMS': '@F8@'}, '@I18@': {'NAME': 'Sage /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '10 JUN 2020', 'FAMC': '@F9@'}}
    assert divorce_before_death(families, individuals) == True

def test_US03_valid():
    individuals = {'@I3@': {'NAME': 'Michael /Cooke/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1962', 'DEAT': '', 'DEATH_DATE':'9 SEP 2007', 'FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'Diana /Chaney/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'FAMS': '@F2@', 'FAMC': '@F4@'}}
    assert us_03(individuals) == True

def test_US03_invalid():
    individuals = {'@I3@': {'NAME': 'Michael /Cooke/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 2012', 'DEAT': '', 'DEATH_DATE':'9 SEP 2009','FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'Diana /Chaney/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'FAMS': '@F2@', 'FAMC': '@F4@'}}
    assert us_03(individuals) == False

def test_US08_valid():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'MARR': '15 APR 1999'}}
    individuals = {'@I3@': {'NAME': 'Michael /Cooke/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 2000', 'FAMC': '@F1@'}}
    assert us_08(families, individuals) == True

def test_US08_invalid():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'MARR': '15 APR 1999', 'CHIL': '@I3@'}}
    individuals = {'@I3@': {'NAME': 'Michael /Cooke/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1998', 'FAMC': '@F1@'}}
    assert us_08(families, individuals) == False