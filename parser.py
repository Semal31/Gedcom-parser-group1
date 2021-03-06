#!/usr/bin/python3.8

import sys
import getopt
import os
import util
import collections
from tabulate import tabulate
from datetime import datetime, timedelta
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

ill_dates = ""


def is_valid_tag(level, tag):
    return "Y" if (tag in TAGS and TAGS[tag] == level) else "N"


def get_age(birth_date, death_date=None):
    today = datetime.today()
    date = None
    try:
        date = datetime.strptime(birth_date, "%d %b %Y")
    except ValueError:
        try:
            date = datetime.strptime(birth_date, "%b %Y")
        except ValueError:
            try:
                date = datetime.strptime(birth_date, "%Y")
            except ValueError:
                pass
    if not death_date:
        return (
            today.year - date.year - ((today.month, today.day) < (date.month, date.day))
        )
    else:
        try:
            death_date = datetime.strptime(death_date, "%d %b %Y")
        except ValueError:
            try:
                death_date = datetime.strptime(death_date, "%b %Y")
            except ValueError:
                try:
                    death_date = datetime.strptime(death_date, "%Y")
                except ValueError:
                    pass
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
        try:
            bday = datetime.strptime(v.get("DATE"), "%d %b %Y")
            if "DEAT" in v:
                dday = datetime.strptime(v.get("DEATH_DATE"), "%d %b %Y")
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
        except ValueError:
            bday = "1 JAN 1111"
            dday = "1 JAN 1111"
            rows.append(
                [
                    k,
                    v.get("NAME"),
                    v.get("SEX"),
                    bday,
                    get_age(bday, dday) if "DEAT" in v else get_age(bday),
                    "DEAT" not in v,
                    dday if "DEAT" in v else "N/A",
                    get_children(k, v["FAMC"]) if "FAMC" in v else "N/A",
                    get_spouse_id(k, v["FAMS"]) if "FAMS" in v else "N/A",
                ]
            )
        # Below was the original code before try-except block was incorporated
        # rows.append(
        #     [
        #         k,
        #         v.get("NAME"),
        #         v.get("SEX"),
        #         v.get("DATE"),
        #         get_age(v.get("DATE"), v.get("DEATH_DATE"))
        #         if "DEAT" in v
        #         else get_age(v.get("DATE")),
        #         "DEAT" not in v,
        #         v.get("DEATH_DATE") if "DEAT" in v else "N/A",
        #         get_children(k, v["FAMC"]) if "FAMC" in v else "N/A",
        #         get_spouse_id(k, v["FAMS"]) if "FAMS" in v else "N/A",
        #     ]
        # )
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
    # check_birth_before_marriage(families, individuals)
    # check_age(individuals)
    print("Individuals")
    print(tabulate(get_sorted_individuals(), headers=indi_headers))
    print("\n\nFamilies")
    print(tabulate(get_sorted_families(), headers=fam_headers))
    print("\n")
    # list_over_30_and_single(individuals)
    # unique_first_names(families, individuals)
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
    # check_marriage_to_descendants(families)
    # order_siblings_by_age(families, individuals)
    # check_unique_ids(file_path)
    # us_27(individuals)
    # us_32(individuals)
    # us_24(families)
    # list_upcoming_birthdays(individuals)
    # list_orphans(families, individuals)
    # list_death_in_last_30_days(individuals)
    # us_37(families,individuals)
    # us_42(families,individuals)
    # us_35(individuals)
    us_40(file_path)


def list_death_in_last_30_days(individuals):
    anyDeaths = False
    for individual in individuals:
        if "DEATH_DATE" in individuals[individual]:
            try:
                death_date = datetime.strptime(
                    individuals[individual]["DEATH_DATE"], "%d %b %Y"
                )
            except ValueError:
                try:
                    death_date = datetime.strptime(
                        individuals[individual]["DEATH_DATE"], "%b %Y"
                    )
                except ValueError:
                    try:
                        death_date = datetime.strptime(
                            individuals[individual]["DEATH_DATE"], "%Y"
                        )
                    except ValueError:
                        pass
            today = datetime.today()
            delta = today - death_date
            if delta.days <= 30:
                anyDeaths = True
                print(f"{individuals[individual]['NAME']} has died within 30 days")
    return anyDeaths


def list_upcoming_anniversaries(individuals: dict, families: dict) -> bool:
    anniversaries = 0
    for family in families.values():
        if "MARR" in family:
            marriage_date = datetime.strptime(family["MARR"], "%d %b %Y")
            month_away = datetime.now() + timedelta(days=30)
            marriage_date = marriage_date.replace(year=(datetime.now()).year)
            print(marriage_date, month_away)
            if marriage_date < month_away:
                anniversaries += 1
                husb = individuals[family["HUSB"]]["NAME"]
                wife = individuals[family["WIFE"]]["NAME"]
                print(f"Anniversary number {anniversaries}: {husb} and {wife}")
    return anniversaries


def list_large_age_differences(individuals: dict, families: dict) -> bool:
    differences = 0
    for family in families.values():
        if "MARR" in family:
            husb = individuals[family["HUSB"]]["NAME"]
            wife = individuals[family["WIFE"]]["NAME"]
            husb_birthdate = datetime.strptime(
                individuals[family["HUSB"]]["DATE"], "%d %b %Y"
            )
            wife_birthdate = datetime.strptime(
                individuals[family["WIFE"]]["DATE"], "%d %b %Y"
            )
            today = datetime.today()
            husb_age = relativedelta(today, husb_birthdate).years
            wife_age = relativedelta(today, wife_birthdate).years
            if husb_age > 2 * wife_age or wife_age > 2 * husb_age:
                differences += 1
                print(
                    f"{husb} and {wife} have an age difference of {abs(husb_age - wife_age)}!"
                )
    return differences


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


def list_deceased(individuals: dict) -> int:
    """Implements user story 29, listing all deceased individuals in a GEDCOM file.
    Author: Ryan Hartman
    Last Modified: 4/12/2021

    Args:
        individuals (dict): A dict of individuals to check

    Returns:
        (int): The number of deceased individuals

    Runtime:
        Ω(1) (when the first individual is an offending case)
        Θ(n)
        O(n)
    """
    deceased = 0
    for id, individual in individuals.items():
        if "DEATH_DATE" in individual:
            if deceased == 0:
                print("Deceased individuals:")
            print(
                f"  -> {individual['NAME']} (ID of {id}) passed away on {individual['DEATH_DATE']}"
            )
            deceased += 1
    if deceased == 0:
        print("No deceased individuals found.")
    return deceased


def names_are_unique(individuals: dict) -> bool:
    """Implements user story 23, checking if all people born on the same day have unique names.
        Author: Ryan Hartman
        Last Modified: 4/12/2021

    Args:
        individuals (dict): A dict of individuals to check

    Returns:
        bool: True if all people born on the same day are unique, false otherwise.

    Runtime:
        Ω(1) (when the first individual is an offending case)
        Θ(n)
        O(n)
    """
    people = {}
    for individual in individuals.values():
        birth_date = individual.get("DATE")
        name = individual.get("NAME")
        if name in people:
            if birth_date in people[name]:
                return False
            else:
                people[name].add(birth_date)
        else:
            people[name] = {birth_date}
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


def list_over_30_and_single(individuals):
    nobody = True
    for id in individuals:
        if "FAMS" not in individuals[id] and "DEAT" not in individuals[id]:
            if get_age(individuals[id]["DATE"]) > 30:
                nobody = False
                print(individuals[id]["NAME"] + " is over 30 and has not been married")
    return nobody


def unique_first_names(families, individuals):
    is_valid = True
    names_birthdays = []
    for id in families:
        if "CHIL" in families[id]:
            for id2 in families[id]["CHIL"]:
                names_birthdays.append(
                    [individuals[id2]["NAME"], individuals[id2]["DATE"]]
                )
            for child in names_birthdays:
                if names_birthdays.count(child) > 1:
                    is_valid = False
                    print("Error: Duplicate child in family: " + id2)
                    break
            names_birthdays.clear()
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


# US12 - Parents not too old
def parents_not_too_old(families, individuals):
    is_valid = True
    for id in families:
        if "CHIL" in families[id]:
            for child in families[id]["CHIL"]:
                child_age = get_age(individuals[child]["DATE"])
                if "WIFE" in families[id]:
                    wife_age = get_age(individuals[families[id]["WIFE"]]["DATE"])
                    if wife_age - child_age >= 60:
                        is_valid = False
                        print(
                            "ERROR: INDIVIDUAL: US12: Wife is too old ("
                            + str(wife_age - child_age),
                            "years older than",
                            get_individual_name(child, individuals).replace("/", "")
                            + ")",
                        )
                if "HUSB" in families[id]:
                    husb_age = get_age(individuals[families[id]["HUSB"]]["DATE"])
                    if husb_age - child_age >= 80:
                        is_valid = False
                        print(
                            "ERROR: INDIVIDUAL: US12: Husband is too old ("
                            + str(husb_age - child_age),
                            "years older than",
                            get_individual_name(child, individuals).replace("/", "")
                            + ")",
                        )
    return is_valid


# US17 - No marriage to descendants
def check_marriage_to_descendants(families):
    is_valid = True
    for id in families:
        if "CHIL" in families[id]:
            for child in families[id]["CHIL"]:
                if "HUSB" in families[id]:
                    if child == families[id]["HUSB"]:
                        print(
                            "ERROR: INDIVIDUAL: US17:",
                            child,
                            "cannot be married to ancestor",
                            families[id]["WIFE"],
                        )
                        is_valid = False
                if "WIFE" in families[id]:
                    if child == families[id]["WIFE"]:
                        print(
                            "ERROR: INDIVIDUAL: US17:",
                            child,
                            "cannot be married to ancestor",
                            families[id]["HUSB"],
                        )
                        is_valid = False
    return is_valid


def order_siblings_by_age(families, individuals):
    siblings_exist_in_all_fams = True
    for id in families:
        if "CHIL" in families[id]:
            children = {}
            if len(families[id]["CHIL"]) > 1:
                for child in families[id]["CHIL"]:
                    children.update({child: get_age(individuals[child]["DATE"])})
                sorted_children = sorted(children, key=children.get, reverse=True)
                print(
                    "For family",
                    id + ", siblings are ordered in descending age as such:",
                    ", ".join(sorted_children),
                )
            else:
                siblings_exist_in_all_fams = False
                print(
                    "For family",
                    id + ", there is only one child (no siblings to order):",
                    families[id]["CHIL"][0],
                )
        else:
            siblings_exist_in_all_fams = False
            print(
                "For family",
                id + ", there are no children (and therefore no siblings to order)",
            )
    return siblings_exist_in_all_fams


def check_unique_ids(file_path):
    f = open(file_path, "r")
    individual_ids = []
    family_ids = []
    is_valid = True
    for line in f:
        if "0 @" in line:
            if "0 @I" in line:
                individual_ids.append(line.split()[1])
            else:
                family_ids.append(line.split()[1])
    if len(individual_ids) != len(set(individual_ids)):
        is_valid = False
        print("ERROR: US22: Individual: Duplicate individual IDs found")
    if len(family_ids) != len(set(family_ids)):
        is_valid = False
        print("ERROR: US22: Family: Duplicate family IDs found")
    return is_valid


# US27 - Include individual ages
def us_27(individuals):
    age = True
    for id in individuals:
        individual_Name = individuals[id]["NAME"]
        if individuals[id]["DATE"] == None:
            age = False
            print(
                "ERROR: INDIVIDUAL: US27: Individual "
                + individual_Name
                + "does not have age listed in table.\n"
            )
    return age


# US32 - List multiple births
def us_32(individuals):
    multiple_Births = False
    birthdays = []
    for id in individuals:
        bday = individuals[id]["DATE"]
        birthdays.append(str(bday))
    if [
        item for item, count in collections.Counter(birthdays).items() if count > 1
    ] == []:
        return multiple_Births
    else:
        multiple_Births = True
        print(
            "US 32: These dates has multple births: "
            + str(
                [
                    item
                    for item, count in collections.Counter(birthdays).items()
                    if count > 1
                ]
            )
        )
        return multiple_Births


# US24 - Unique families and spouses
def us_24(families):
    is_valid = True
    arrayOfFamilies = []
    for id in families:
        # Iterate through each family and append to local copy of relevant info to check
        family = families[id]
        # Check if any matches with local array (check for duplicate families)
        for fam in arrayOfFamilies:
            if family == fam:
                print("ERROR: US24: Family: Duplicate family found")
                is_valid = False
        arrayOfFamilies.append(family)

    return is_valid


# US30 - List living married
def us_30(individuals):
    print("US30: List living married:")
    for id in individuals:
        # Iterate through each person and check if they meet qualifiers
        if not "DEATH_DATE" in individuals[id]:
            if "FAMS" in individuals[id]:
                print(individuals[id]["NAME"])


# US38 - List upcoming birthdays
def list_upcoming_birthdays(individuals):
    any_bdays = False
    for id in individuals:
        birthdate = datetime.strptime(individuals[id]["DATE"], "%d %b %Y")
        month = int(birthdate.strftime("%m"))
        day = int(birthdate.strftime("%d"))
        d = (month, day)
        curr_month = int(datetime.now().strftime("%m"))
        curr_day = int(datetime.now().strftime("%d"))
        curr_d = (curr_month, curr_day)
        one_mo_later = (curr_month + 1, curr_day)
        if d > curr_d and d < one_mo_later:
            any_bdays = True
            print(
                "US38: Individual: There is an upcoming birthday on",
                birthdate.strftime("%b"),
                day,
                "for individual",
                id,
            )
    return any_bdays


# US33 - List orphans
def list_orphans(families, individuals):
    any_orphans = False
    for id in families:
        if "CHIL" in families[id]:
            for child in families[id]["CHIL"]:
                if get_age(individuals[child]["DATE"]) < 18:
                    if "HUSB" in families[id] and "WIFE" in families[id]:
                        if (
                            "DEAT" in individuals[families[id]["HUSB"]]
                            and "DEAT" in individuals[families[id]["WIFE"]]
                        ):
                            any_orphans = True
                            print(
                                "US33: Both parents for family",
                                id,
                                "have died, leaving",
                                child,
                                "(age",
                                str(get_age(individuals[child]["DATE"]))
                                + ") as an orphan.",
                            )
    return any_orphans


# US37 - List recent survivors
def us_37(families, individuals):
    is_valid = False
    output = "US37: "
    for id in individuals:
        if "DEAT" in individuals[id]:
            try:
                death_date = datetime.strptime(
                    individuals[id]["DEATH_DATE"], "%d %b %Y"
                )
            except ValueError:
                try:
                    death_date = datetime.strptime(
                        individuals[id]["DEATH_DATE"], "%b %Y"
                    )
                except ValueError:
                    try:
                        death_date = datetime.strptime(
                            individuals[id]["DEATH_DATE"], "%Y"
                        )
                    except ValueError:
                        pass
            today = datetime.today()
            delta = today - death_date
            if delta.days <= 30:
                dead_ID = id
                fam_ID = individuals[id]["FAMS"]
                output += (
                    individuals[dead_ID]["NAME"].replace("/", "")
                    + " died in the last 30 days\n"
                )
                if families[fam_ID]["HUSB"] == dead_ID:
                    living_spouse_ID = families[fam_ID]["WIFE"]
                else:
                    living_spouse_ID = families[fam_ID]["HUSB"]
                if "DEAT" not in individuals[living_spouse_ID]:
                    output += (
                        "Living Spouse: "
                        + individuals[living_spouse_ID]["NAME"].replace("/", "")
                        + "\n"
                    )
                children = families[fam_ID]["CHIL"]
                for child in children:
                    if "DEAT" not in individuals[child]:
                        output += (
                            "Living Children: "
                            + individuals[child]["NAME"].replace("/", "")
                            + "\n"
                        )
                is_valid = True
                print(output)
    return is_valid


# 42 - Reject illegitimate dates
def us_42(families, individuals):
    is_valid = True
    for id in individuals:
        try:
            test_birthday = datetime.strptime(individuals[id]["DATE"], "%d %b %Y")
        except ValueError:
            print(
                "ERROR: US 42: "
                + individuals[id]["NAME"].replace("/", "")
                + "'s birthday/death date was an illegitimate date and was replaced with 1 JAN 1111"
            )
            is_valid = False
        if "DEAT" in individuals[id]:
            try:
                test_death = datetime.strptime(
                    individuals[id]["DEATH_DATE"], "%d %b %Y"
                )
            except ValueError:
                print(
                    "ERROR: US 42: "
                    + individuals[id]["NAME"].replace("/", "")
                    + "'s birthday/death date was an illegitimate date and was replaced with 1 JAN 1111."
                )
                is_valid = False
    for id in families:
        if "MARR" in families[id]:
            try:
                test_marr = datetime.strptime(families[id]["MARR"], "%d %b %Y")
            except ValueError:
                print(
                    "ERROR: US 42: Family ("
                    + str(id)
                    + ") has an illegitimate marriage date."
                )
                is_valid = False
        if "DIV" in families[id]:
            try:
                test_div = datetime.strptime(families[id]["DIV"], "%d %b %Y")
            except ValueError:
                print(
                    "ERROR: US 42: Family ("
                    + str(id)
                    + ") has an illegitimate divorce date."
                )
                is_valid = False
    return is_valid


# US35 - List Recent Births
def us_35(individuals):
    recent_births = False
    for id in individuals:
        birthdate = datetime.strptime(individuals[id]["DATE"], "%d %b %Y")
        currentDate = datetime.now()
        monthBeforeCurrentDate = datetime.now() - timedelta(days=30)
        if monthBeforeCurrentDate < birthdate < currentDate:
            # Birthdate falls in between
            recent_births = True
            print(
                "US35: Individual: There was a recent birth on",
                birthdate.strftime("%d %b %Y"),
                "for individual",
                id,
            )
    return recent_births


# US40 - Include input line numbers
def us_40(file_path):
    noErrorInFile = True

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find file '{file_path}'.")

    with open(file_path, "r") as fp:
        for index, line in enumerate(fp):
            parts = line.rstrip().split(" ")
            if len(parts) < 2:
                noErrorInFile = False
                print("ERROR: US 40: Error in line ", index)

    return noErrorInFile


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
