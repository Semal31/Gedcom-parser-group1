import pytest

from parser import check_marriage_divorce_dates

def test_check_marriage_divorce_dates_with_correct_dates():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'DATE': '15 APR 1999'}, '@F2@': {'HUSB': '@I3@', 'WIFE': '@I4@', 'CHIL': ['@I1@', '@I5@'], 'MARR': '8 AUG 1991', 'DIV': '30 DEC 2018'}}
    individuals = {}
    assert check_marriage_divorce_dates(families, individuals) == True

def test_check_marriage_divorce_dates_with_incorrect_dates():
    families = {'@F1@': {'HUSB': '@I1@', 'WIFE': '@I2@', 'DATE': '15 APR 1999'}, '@F2@': {'HUSB': '@I3@', 'WIFE': '@I4@', 'CHIL': ['@I1@', '@I5@'], 'MARR': '8 AUG 2020', 'DIV': '30 DEC 2018'}}
    individuals = {'@I3@': {'NAME': 'Thomas /Hartman/', 'SEX': 'M', 'BIRT': '', 'DATE': '2 DEC 1962', 'FAMS': '@F2@', 'FAMC': '@F3@'}, '@I4@': {'NAME': 'June /Lagaveen/', 'SEX': 'F', 'BIRT': '', 'DATE': '1 OCT 1970', 'FAMS': '@F2@', 'FAMC': '@F4@'}}
    assert check_marriage_divorce_dates(families, individuals) == False