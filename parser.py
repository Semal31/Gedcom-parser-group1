#!/usr/bin/python3.8

import sys
import getopt
import os
import util
from tabulate import tabulate
from datetime import datetime
from dateutil.relativedelta import relativedelta

TAGS = {
    "NOTE": 0,
    "TRLR": 0,
    "HEAD": 0,
    "DATE": 2,
    "DIV": 1,
    "CHIL": 1,
    "WIFE": 1,
    "HUSB": 1,
    "MARR": 1,
    "FAM": 0,
    "FAMS": 1,
    "FAMC": 1,
    "DEAT": 1,
    "BIRT": 1,
    "SEX": 1,
    "NAME": 1,
    "INDI": 0,
}


families = {}
individuals = {}


def is_valid_tag(level, tag):
    return "Y" if (tag in TAGS and TAGS[tag] == level) else "N"


def get_age(birth_date, death_date=None):
    today = datetime.today()
    date = datetime.strptime(birth_date, "%d %b %Y")
    if not death_date:
        return (
            today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        )
    else:
        death_date = datetime.strptime(death_date, "%d %b %Y")
        return (
            death_date.year
            - date.year
            - ((today.month, today.day) < (death_date.month, death_date.day))
        )


def get_children(indi_id, fam_id):
    return families[fam_id]["CHIL"]


def get_spouse_id(indi_id, fam_id):
    family = families[fam_id]
    if fam_id == family.get("HUSB"):
        return family["WIFE"]
    else:
        return family["HUSB"]


def get_individual_name(indi_id, individuals):
    return individuals[indi_id]["NAME"]


def get_id_number(id):
    id_string = ""
    for c in id:
        if ord(c) >= ord("0") and ord(c) <= ord("9"):
            id_string += c
    return int(id_string)


def get_sorted_families():
    rows = []
    for k in sorted(families, key=get_id_number):
        v = families[k]
        rows.append(
            [
                k,
                v.get("MARR", "N/A"),
                v.get("DIV", "N/A"),
                v.get("HUSB", "N/A"),
                get_individual_name(v["HUSB"], individuals) if "HUSB" in v else "N/A",
                v.get("WIFE", "N/A"),
                get_individual_name(v["WIFE"], individuals) if "WIFE" in v else "N/A",
                v.get("CHIL", "N/A"),
            ]
        )
    return rows


def get_sorted_individuals():
    rows = []
    for k in sorted(individuals, key=get_id_number):
        v = individuals[k]
        rows.append(
            [
                k,
                v.get("NAME"),
                v.get("SEX"),
                v.get("DATE"),
                get_age(v.get("DATE"), v.get("DEATH_DATE"))
                if "DEAT" in v
                else get_age(v.get("DATE")),
                "DEAT" not in v,
                v.get("DEATH_DATE") if "DEAT" in v else "N/A",
                get_children(k, v["FAMC"]) if "FAMC" in v else "N/A",
                get_spouse_id(k, v["FAMS"]) if "FAMS" in v else "N/A",
            ]
        )
    return rows


def get_information(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find file '{file_path}'.")

    parsing = False
    id = ""
    with open(file_path, "r") as fp:
        for line in fp:
            parts = line.rstrip().split(" ")
            level, tag, *arguments = parts
            if level == "0":
                if arguments and arguments[0] in ("INDI", "FAM"):
                    id = tag
                    parsing = arguments[0]
                    if parsing == "INDI":
                        individuals[id] = {}
                    else:
                        families[id] = {}
                else:
                    parsing = ""
            elif parsing and tag in TAGS:
                if parsing == "INDI":
                    if tag == "DEAT":
                        individuals[id][tag] = " ".join(arguments)
                        nextline = fp.readline()
                        level, tag, *arguments = nextline.rstrip().split(" ")
                        individuals[id]["DEATH_DATE"] = " ".join(arguments)
                    else:
                        individuals[id][tag] = " ".join(arguments)
                else:
                    if tag == "CHIL":
                        if tag in families[id]:
                            families[id][tag].append(arguments[0])
                        else:
                            families[id][tag] = [arguments[0]]
                    elif tag in ("MARR", "DIV"):
                        nextline = fp.readline()
                        _, next_tag, *arguments = nextline.rstrip().split(" ")
                        if next_tag == "DATE":
                            families[id][tag] = " ".join(arguments)
                    else:
                        families[id][tag] = " ".join(arguments)

    indi_headers = [
        "ID",
        "Name",
        "Gender",
        "Birthday",
        "Age",
        "Alive",
        "Death",
        "Child",
        "Spouse",
    ]
    fam_headers = [
        "ID",
        "Married",
        "Divorced",
        "Husband ID",
        "Husband Name",
        "Wife ID",
        "Wife Name",
        "Children",
    ]
    # check_marriage_divorce_dates(families, individuals)
    check_birth_before_marriage(families, individuals)
    check_age(individuals)
    print("Individuals")
    print(tabulate(get_sorted_individuals(), headers=indi_headers))
    print("\n\nFamilies")
    print(tabulate(get_sorted_families(), headers=fam_headers))
    print("\n")
    # children_before_death(families, individuals)
    # us_05(families,individuals)
    # us_10(families,individuals)
    # divorce_before_death(families, individuals)
    # us_03(individuals)
    # us_08(families,individuals)
    # fewer_than_15_children(families)
    # uncle_aunts_cannot_marry_nieces_nephews(families, individuals)
    # us_16(families, individuals)
    # us_21(families,individuals)
    # us_14(families,individuals)
    # us_19(families, individuals)


def siblings_do_not_marry(individuals: dict, families: dict) -> bool:
    """Implements user story 18, checking if all siblings do not marry.
        Author: Ryan Hartman
        Last Modified: 3/31/2021

    Args:
        individuals (dict): A dict of individuals to check
        families (dict): A dict of families to check

    Returns:
        bool: True when all siblings are not married, false otherwise.

    Runtime:
        Ω(1) (when the first family is an offending case)
        Θ(n)
        O(n)
    """
    for family in families.values():
        if "HUSB" in family or "WIFE" in family:
            print("here2")
            husband = individuals.get(family["HUSB"])
            wife = individuals.get(family["WIFE"])
            if husband == None or wife == None:
                raise ValueError(
                    "Individuals dictionary did not contain an individual found in the families dictionary."
                )
            elif husband.get("FAMC") == wife.get("FAMC"):
                return False
    return True


def siblings_could_be_born(individuals: dict, families: dict) -> bool:
    """Implements user story 13, checking if all siblings in a family are born 9 months
        from each other, or are born within one day of each other.
        Twins can be born at 11:59pm and 12:00am, making them seperated by a day.
        Author: Ryan Hartman
        Last Modified: 3/31/2021

    Args:
        individuals (dict): A dict of individuals to check
        families (dict): A dict of families to check

    Returns:
        bool: True when all siblings are not married, false otherwise.

    Runtime:
        Ω(1) (when the first family is an offending case)
        Θ(n)
        O(n)
    """
    for family in families.values():
        if "CHIL" in family:
            print("here")
            children = []
            for child_id in family["CHIL"]:
                children.append(individuals[child_id])
            birth_dates = list(
                map(
                    lambda child: datetime.strptime(child.get("DATE"), "%d %b %Y"),
                    children,
                )
            )
            for date in birth_dates:
                for second_date in birth_dates:
                    # Make sure the time delta is correct:
                    delta = (
                        date - second_date if date > second_date else second_date - date
                    )
                    if delta.days >= 2 and delta.days < 243:
                        # 30.42 * 8 = 243.36 (30.42 average days in a month)
                        return False

    return True


def check_age(individuals: dict) -> bool:
    """Implements user story 7, ensuring each individual is less than 150 years old.
        Author: Ryan Hartman
        Last Modified: 3/17/2021

    Args:
        individuals (dict): A dict of individuals to check

    Returns:
        bool: True when all ages are less than 150, False otherwise.
    """
    is_valid = True

    for id in individuals:
        person = individuals[id]
        birth_date = person.get("DATE")
        age = get_age(birth_date)
        if age >= 150:
            if is_valid:
                print("ERROR: Individuals cannot be 150 or older!\n")
                is_valid = False
            print(f"{person.get('NAME')} (id {id}) was {age} years old.")

    return is_valid


def fewer_than_15_children(families):
    is_valid = True
    children = 0
    for id in families:
        if "CHIL" in families[id]:
            for chil_id in families[id]["CHIL"]:
                children += 1
    if children >= 15:
        is_valid = False
        print("Error: family '" + id + "' has more than 14 children")
    return is_valid


def uncle_aunts_cannot_marry_nieces_nephews(families, individuals):
    is_valid = True
    husb_sib_ids = []
    wife_sib_ids = []
    for id in families:
        if "CHIL" in families[id]:
            if "HUSB" in families[id]:
                husb_id = families[id]["HUSB"]
                for id2 in families:
                    if "CHIL" in families[id2]:
                        if husb_id in families[id2]["CHIL"]:
                            for chil_id in families[id2]["CHIL"]:
                                if chil_id != husb_id:
                                    husb_sib_ids.append(chil_id)
            if "WIFE" in families[id]:
                wife_id = families[id]["WIFE"]
                for id3 in families:
                    if "CHIL" in families[id3]:
                        if wife_id in families[id3]["CHIL"]:
                            for chil_id2 in families[id3]["CHIL"]:
                                if chil_id2 != wife_id:
                                    wife_sib_ids.append(chil_id2)
            for husb_sib in husb_sib_ids:
                if "FAMS" in individuals[husb_sib]:
                    if individuals[husb_sib]["SEX"] == "M":
                        if "WIFE" in families[individuals[husb_sib]["FAMS"]]:
                            for chil_id3 in families[id]["CHIL"]:
                                if (
                                    families[individuals[husb_sib]["FAMS"]]["WIFE"]
                                    == chil_id3
                                ):
                                    is_valid = False
                                    print(
                                        "Error: Uncle '"
                                        + individuals[husb_sib]["NAME"]
                                        + "' is married to niece '"
                                        + individuals[chil_id3]["NAME"]
                                        + "'"
                                    )
                    else:
                        if "HUSB" in families[individuals[husb_sib]["FAMS"]]:
                            for chil_id4 in families[id]["CHIL"]:
                                if (
                                    families[individuals[husb_sib]["FAMS"]]["HUSB"]
                                    == chil_id4
                                ):
                                    is_valid = False
                                    print(
                                        "Error: Aunt '"
                                        + individuals[husb_sib]["NAME"]
                                        + "' is married to nephew '"
                                        + individuals[chil_id4]["NAME"]
                                        + "'"
                                    )
            for wife_sib in wife_sib_ids:
                if "FAMS" in individuals[wife_sib]:
                    if individuals[wife_sib]["SEX"] == "M":
                        if "WIFE" in families[individuals[wife_sib]["FAMS"]]:
                            for chil_id5 in families[id]["CHIL"]:
                                if (
                                    families[individuals[wife_sib]["FAMS"]]["WIFE"]
                                    == chil_id5
                                ):
                                    is_valid = False
                                    print(
                                        "Error: Uncle '"
                                        + individuals[wife_sib]["NAME"]
                                        + "' is married to niece '"
                                        + individuals[chil_id5]["NAME"]
                                        + "'"
                                    )
                    else:
                        if "HUSB" in families[individuals[wife_sib]["FAMS"]]:
                            for chil_id6 in families[id]["CHIL"]:
                                if (
                                    families[individuals[wife_sib]["FAMS"]]["HUSB"]
                                    == chil_id6
                                ):
                                    is_valid = False
                                    print(
                                        "Error: Aunt '"
                                        + individuals[wife_sib]["NAME"]
                                        + "' is married to nephew '"
                                        + individuals[chil_id6]["NAME"]
                                        + "'"
                                    )
    return is_valid


# Children born before parents death
def children_before_death(families, individuals):
    is_valid = True
    for id in families:
        if "CHIL" in families[id]:
            if "HUSB" in families[id]:
                husband = individuals[families[id]["HUSB"]]
            else:
                husband = None
            if "WIFE" in families[id]:
                wife = individuals[families[id]["WIFE"]]
            else:
                wife = None
            if husband:
                if "DEATH_DATE" in husband:
                    husb_death = datetime.strptime(husband["DEATH_DATE"], "%d %b %Y")
                else:
                    husb_death = False
            else:
                husb_death = False
            if wife:
                if "DEATH_DATE" in wife:
                    wife_death = datetime.strptime(wife["DEATH_DATE"], "%d %b %Y")
                else:
                    wife_death = False
            else:
                wife_death = False
            for chil_id in families[id]["CHIL"]:
                birth_child = individuals[chil_id]["DATE"]
                if birth_child == "":
                    break
                birth_child = datetime.strptime(birth_child, "%d %b %Y")
                if husb_death:
                    new_husb_death = husb_death + relativedelta(months=9)
                    if birth_child > husb_death:
                        print(
                            "Error: Husband: '"
                            + husband["NAME"]
                            + "' death on "
                            + husb_death.strftime("%d-%b-%Y")
                            + " is impossible for child: '"
                            + individuals[chil_id]["NAME"]
                            + "' to be born on "
                            + birth_child.strftime("%d-%b-%Y")
                        )
                        is_valid = False
                if wife_death:
                    if birth_child > wife_death:
                        print(
                            "Error: Wife: '"
                            + wife["NAME"]
                            + "' death on "
                            + wife_death.strftime("%d-%b-%Y")
                            + " is impossible for child: '"
                            + individuals[chil_id]["NAME"]
                            + "' to be born on "
                            + birth_child.strftime("%d-%b-%Y")
                        )
                        is_valid = False
    return is_valid


def check_birth_before_marriage(families: dict, individuals: dict) -> bool:
    """Implements user story 2, ensuring each married couple is married after they were born.
        Author: Ryan Hartman
        Last Modified: 3/17/2021

    Args:
        families    (dict): A list of families to
        individuals (dict): A list of individuals to lookup individuals in families.
                            NOTE: Every spouse in each family MUST be in the individuals dict.
    Throws:
        IndexError:         When an individual in a family cannot be found in the individuals
                            dictionary.

    Returns:
        bool: True when all marriages happen after birth, False otherwise.
    """
    is_valid = True

    def print_error(family_id: str, family: dict, spouse: dict, is_valid: bool) -> None:
        male = spouse["SEX"] == "M"
        if is_valid:
            print(f"ERROR: Individuals cannot be married before being born!\n")
        print(
            f"{'Husband' if male else 'Wife'} of family {family_id} was born {spouse['DATE']}, but got married on {family['MARR']}."
        )

    for id in families:
        if "MARR" in families[id]:
            marriage_date = datetime.strptime(families[id]["MARR"], "%d %b %Y")
            husb_ID = families[id]["HUSB"]
            wife_ID = families[id]["WIFE"]
            husb_birthdate = datetime.strptime(
                individuals[husb_ID].get("DATE"), "%d %b %Y"
            )
            wife_birthdate = datetime.strptime(
                individuals[wife_ID].get("DATE"), "%d %b %Y"
            )
            if husb_birthdate >= marriage_date:
                print_error(id, families[id], individuals[husb_ID], is_valid)
                is_valid = False
            if wife_birthdate >= marriage_date:
                print_error(id, families[id], individuals[husb_ID], is_valid)
                is_valid = False

    return is_valid


# Marriage before divorce
def check_marriage_divorce_dates(families, individuals):
    is_valid = True
    for id in families:
        if "DIV" in families[id]:
            divorce_date = datetime.strptime(families[id]["DIV"], "%d %b %Y")
            marriage_date = datetime.strptime(families[id]["MARR"], "%d %b %Y")
            if divorce_date < marriage_date:
                if is_valid:
                    print("Divorce before marriage is not possible\n")
                print(
                    "Husband: "
                    + get_individual_name(families[id]["HUSB"], individuals).replace(
                        "/", ""
                    )
                    + "\nWife: "
                    + get_individual_name(families[id]["WIFE"], individuals).replace(
                        "/", ""
                    )
                )
                print("\nMarriage: " + families[id]["MARR"])
                print("Divorce: " + families[id]["DIV"])
                is_valid = False
    if not is_valid:
        return False
        sys.exit(1)
    return True


# US01 - Dates before current date
def dates_before_current(file_path):
    f = open(file_path, "r")
    count = 0
    for line in f:
        if "2 DATE" in line:
            formatted_date = datetime.strptime(line[7:-1], "%d %b %Y")
            current_date = datetime.now()
            if formatted_date > current_date:
                print(
                    "ERROR: INDIVIDUAL: US01: Date '"
                    + line[7:-1]
                    + "' is a future date that has not yet occurred"
                )
                count += 1
                # count instances of error found (if none are found then return True)
    if count == 0:
        return True
    else:
        return False


# US06 - Divorce before death
def divorce_before_death(families, individuals):
    count = 0
    for id in families:
        if "DIV" in families[id]:
            div_date = datetime.strptime(families[id]["DIV"], "%d %b %Y")
            print(div_date)
            husb_ID = families[id]["HUSB"]
            wife_ID = families[id]["WIFE"]
            if "DEAT" in individuals[husb_ID] and "DEAT" in individuals[wife_ID]:
                husbDeath = datetime.strptime(
                    individuals[husb_ID]["DEATH_DATE"], "%d %b %Y"
                )
                wifeDeath = datetime.strptime(
                    individuals[wife_ID]["DEATH_DATE"], "%d %b %Y"
                )
                if div_date > husbDeath and div_date > wifeDeath:
                    count += 1
                    print(
                        "ERROR: FAMILY: US06: Divorce between "
                        + "'"
                        + get_individual_name(husb_ID, individuals).replace("/", "")
                        + "' and '"
                        + get_individual_name(wife_ID, individuals).replace("/", "")
                        + "' cannot occur after both partners' deaths."
                    )
            elif "DEAT" in individuals[husb_ID]:
                husbDeath = datetime.strptime(
                    individuals[husb_ID]["DEATH_DATE"], "%d %b %Y"
                )
                if div_date > husbDeath:
                    count += 1
                    print(
                        "ERROR: FAMILY: US06: Divorce between "
                        + "'"
                        + get_individual_name(husb_ID, individuals).replace("/", "")
                        + "' and '"
                        + get_individual_name(wife_ID, individuals).replace("/", "")
                        + "' cannot occur after "
                        + get_individual_name(husb_ID, individuals).replace("/", "")
                        + "'s death."
                    )
            elif "DEAT" in individuals[wife_ID]:
                wifeDeath = datetime.strptime(
                    individuals[wife_ID]["DEATH_DATE"], "%d %b %Y"
                )
                if div_date > wifeDeath:
                    count += 1
                    print(
                        "ERROR: FAMILY: US06: Divorce between "
                        + "'"
                        + get_individual_name(husb_ID, individuals).replace("/", "")
                        + "' and '"
                        + get_individual_name(wife_ID, individuals).replace("/", "")
                        + "' cannot occur after "
                        + get_individual_name(wife_ID, individuals).replace("/", "")
                        + "'s death."
                    )
    if count == 0:
        return True
    else:
        return False


# US05 - Marriage before Death
def us_05(families, individuals):
    is_valid = True
    for id in families:
        if "MARR" in families[id]:
            marriage_Date = datetime.strptime(families[id]["MARR"], "%d %b %Y").date()
            husb_ID = families[id]["HUSB"]
            wife_ID = families[id]["WIFE"]
            if "DEAT" in individuals[husb_ID]:
                husbDeath = datetime.strptime(
                    individuals[husb_ID]["DEATH_DATE"], "%d %b %Y"
                ).date()
                if marriage_Date > husbDeath:
                    print(
                        "ERROR: FAMILY: US05: Marriage occurred after death of husband ("
                        + get_individual_name(husb_ID, individuals).replace("/", "")
                        + ")."
                    )
                    is_valid = False
            if "DEAT" in individuals[wife_ID]:
                wifeDeath = datetime.strptime(
                    individuals[wife_ID]["DEATH_DATE"], "%d %b %Y"
                ).date()
                if marriage_Date > wifeDeath:
                    print(
                        "ERROR: FAMILY: US05: Marriage occurred after death of wife ("
                        + get_individual_name(wife_ID, individuals).replace("/", "")
                        + ")."
                    )
                    is_valid = False
    return is_valid


# US10 - Marriage after 14
def us_10(families, individuals):
    is_valid = True
    for id in families:
        if "MARR" in families[id]:
            marriage_Date = datetime.strptime(families[id]["MARR"], "%d %b %Y").date()
            husb_ID = families[id]["HUSB"]
            wife_ID = families[id]["WIFE"]
            husb_Bday = datetime.strptime(
                individuals[husb_ID]["DATE"], "%d %b %Y"
            ).date()
            wife_Bday = datetime.strptime(
                individuals[wife_ID]["DATE"], "%d %b %Y"
            ).date()
            husb_Age = (marriage_Date - husb_Bday).days / 365
            wife_Age = (marriage_Date - wife_Bday).days / 365
            if husb_Age < 14 and wife_Age < 14:
                print(
                    "ANOMALY: FAMILY: US10: Marriage happened before both husband ("
                    + get_individual_name(husb_ID, individuals).replace("/", "")
                    + ") and wife ("
                    + get_individual_name(wife_ID, individuals).replace("/", "")
                    + ") were 14."
                )
                is_valid = False
            elif husb_Age < 14:
                print(
                    "ANOMALY: FAMILY: US10: Marriage happened before husband ("
                    + get_individual_name(husb_ID, individuals).replace("/", "")
                    + ") was 14."
                )
                is_valid = False
            elif wife_Age < 14:
                print(
                    "ANOMALY: FAMILY: US10: Marriage happened before wife ("
                    + get_individual_name(wife_ID, individuals).replace("/", "")
                    + ")was 14."
                )
                is_valid = False
    return is_valid


# US03 - Birth before death
def us_03(individuals):
    is_valid = True
    for id in individuals:
        if "DEATH_DATE" in individuals[id]:
            birthDate, deathDate = (
                datetime.strptime(individuals[id]["DATE"], "%d %b %Y").date(),
                datetime.strptime(individuals[id]["DEATH_DATE"], "%d %b %Y").date(),
            )
            if birthDate > deathDate:
                print(
                    "ERROR: INDIVIDUAL: US03: Birth occurred after death of individual: "
                    + individuals[id]["NAME"].replace("/", "")
                    + " (id: "
                    + id
                    + ")."
                )
                is_valid = False
    return is_valid


# US08 - Birth before marriage of parents
def us_08(families, individuals):
    is_valid = True
    for id in families:
        if "MARR" in families[id]:
            # Check for edge case of MARR not containing date
            if "DATE" in families[id]:
                marriageDate = datetime.strptime(
                    families[id]["DATE"], "%d %b %Y"
                ).date()
                for childID in families[id]["CHIL"]:
                    childBirthDate = datetime.strptime(
                        individuals[childID]["DATE"], "%d %b %Y"
                    ).date()
                    if childBirthDate < marriageDate:
                        print(
                            "ANOMALY: FAMILY: US08: Child ("
                            + get_individual_name(childID, individuals).replace("/", "")
                            + ") born before marriage of parents in family: "
                            + id
                            + "."
                        )
                        is_valid = False
            else:
                print(
                    "ERROR: FILE: US08: Marriage date not set or properly formatted of family: "
                    + id
                    + "."
                )
                is_valid = False
    return is_valid


# US16 - Male last names
def us_16(families, individuals):
    is_valid = True
    for id in families:
        husb_name = get_individual_name(families[id]["HUSB"], individuals)
        fam_lname = husb_name[husb_name.index("/") + 1 : -1]
        if "CHIL" in families[id]:
            children_idList = families[id]["CHIL"]
            for child in children_idList:
                if individuals[child]["SEX"] == "M":
                    child_name = get_individual_name(child, individuals)
                    if child_name[child_name.index("/") + 1 : -1] != fam_lname:
                        print(
                            "ANOMALY: INDIVIDUAL: US16: "
                            + get_individual_name(child, individuals).replace("/", "")
                            + " does not have a matching family last name of "
                            + fam_lname
                            + "\n"
                        )
                        is_valid = False
    return is_valid


# US21 - Correct gender for role
def us_21(families, individuals):
    is_valid = True
    for id in families:
        husb_id = families[id]["HUSB"]
        wife_id = families[id]["WIFE"]
        if individuals[husb_id]["SEX"] != "M":
            print(
                "ANOMALY: FAMILY: US21: Husband "
                + get_individual_name(husb_id, individuals).replace("/", "")
                + " is not marked as male\n"
            )
            is_valid = False
        if individuals[wife_id]["SEX"] != "F":
            print(
                "ANOMALY: FAMILY: US21: Wife "
                + get_individual_name(wife_id, individuals).replace("/", "")
                + " is not marked as female\n"
            )
            is_valid = False
    return is_valid


# US14 - Multiple births <= 5
def us_14(families, individuals):
    is_valid = True
    for id in families:
        # Check for families with kids
        if "CHIL" in families[id]:
            # Check 5 or more children case before checking individual records
            if len(families[id]["CHIL"]) >= 5:
                childBirthdays = {}
                for child in families[id]["CHIL"]:
                    # increment dict if born on same day or append
                    birthday = individuals[child]["DATE"]
                    if not birthday in childBirthdays:
                        childBirthdays[birthday] = 1
                    else:
                        childBirthdays[birthday] += 1
                # Check if more than 5 births on same day
                for birthdate in childBirthdays:
                    if childBirthdays[birthdate] >= 5:
                        print(
                            "ANOMALY: FAMILY: US14: 5 or more children are born on "
                            + birthdate
                            + " in family "
                            + id
                        )
                        is_valid = False
    return is_valid


# US19 - First cousins should not marry
def us_19(families, individuals):
    is_valid = True
    for id in families:
        grandChildren = []
        if "CHIL" in families[id]:
            # Iterate through children to get grandchildren
            for child in families[id]["CHIL"]:
                if "FAMS" in individuals[child]:
                    family = individuals[child]["FAMS"]
                    if "CHIL" in families[family]:
                        for gChild in families[family]["CHIL"]:
                            grandChildren.append(gChild)
            # Iterate through grand children to determine if married to one another
            for person in grandChildren:
                # Check if sharing same FAMS with cousins ( family in which an individual appears as a spouse )
                if "FAMS" in individuals[person]:
                    for id in grandChildren:
                        if not id == person:
                            if "MARR" in families[individuals[person]["FAMS"]]:
                                if (
                                    families[individuals[person]["FAMS"]]["HUSB"]
                                    == person
                                    and families[individuals[person]["FAMS"]]["WIFE"]
                                    == id
                                    or families[individuals[person]["FAMS"]]["HUSB"]
                                    == id
                                    and families[individuals[person]["FAMS"]]["WIFE"]
                                    == person
                                ):
                                    print(
                                        "ANOMALY: FAMILY: US19: First cousins ("
                                        + person
                                        + " "
                                        + id
                                        + ") should not marry"
                                    )
                                    is_valid = False
    return is_valid


def parse_GEDCOM(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find file '{file_path}'.")
    with open(file_path, "r") as fp:
        indi_id = ""
        fam_id = ""
        for line in fp:
            parts = line.rstrip().split(" ")
            level, tag, *arguments = parts
            print("--> ", line.rstrip())
            # INDI and FAM tags are in a different order.
            # If INDI or FAM appears in the 3rd position (1st argument)
            # then adjust the output message.
            if arguments and arguments[0] in ("INDI", "FAM"):
                actual_tag = arguments[0]
                arguments[0] = tag
                print(
                    f"<-- {level}|{actual_tag}|{is_valid_tag(level, actual_tag)}|{' '.join(arguments)}"
                )

                # Store the ID and the name of the person
                if actual_tag == "INDI":
                    indi_id = arguments[0][1:3]
                else:
                    fam_id = arguments[0][1:3]
            else:
                print(
                    f"<-- {level}|{tag}|{is_valid_tag(int(level), tag)}|{' '.join(arguments)}"
                )
                if tag == "NAME" and indi_id not in individuals and indi_id != "":
                    individuals[indi_id] = " ".join(arguments)
    # print_information()


def print_usage(help: bool):
    msg = f"""Usage:
    {sys.argv[0]} <file_name>
    Args:
        -h: Display help message"""
    msg = "Parses and prints information from a GEDCOM file.\n\n" + msg if help else msg
    print(msg)


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr")
    except getopt.GetoptError:
        print_usage(False)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print_usage(True)
            sys.exit()
        else:
            print_usage(False)
            sys.exit(2)
    if len(args) != 1:
        print_usage(False)
        sys.exit()
    # parse_GEDCOM(args[0])
    get_information(args[0])
