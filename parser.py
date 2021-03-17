#!/usr/bin/python3.8

import sys
import getopt
import os
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
                        _, __, *arguments = nextline.rstrip().split(" ")
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
    print("Individuals")
    print(tabulate(get_sorted_individuals(), headers=indi_headers))
    print("\n\nFamilies")
    print(tabulate(get_sorted_families(), headers=fam_headers))
    print("\n")
    children_before_death(families, individuals)
    # us_05(families,individuals)
    # us_10(families,individuals)

def children_before_death(families, individuals):
  for id in families:
      if "CHIL" in families[id]:
        if "HUSB" in families[id]:
          husband = individuals[families[id]["HUSB"]]
        if "WIFE" in families[id]:
          wife = individuals[families[id]["WIFE"]]
        if "DEATH_DATE" in husband:
          husb_death = datetime.strptime(husband["DEATH_DATE"], "%d %b %Y")
        else: 
          husb_death = False
        if "DEATH_DATE" in wife:
          wife_death = datetime.strptime(wife["DEATH_DATE"], "%d %b %Y")
        else: 
          wife_death = False
        for chil_id in families[id]["CHIL"]:
          birth_child = individuals[chil_id]["DATE"]
          if birth_child == "":
            break
          birth_child = datetime.strptime(birth_child, "%d %b %Y")
          if (husb_death):
            new_husb_death = husb_death + relativedelta(months=9)
            if (birth_child > husb_death):
              print("Error: Husband: '" + husband["NAME"] + "' death on " + husb_death.strftime("%d-%b-%Y") + " is impossible for child: '" + individuals[chil_id]["NAME"] + "' to be born on " + birth_child.strftime("%d-%b-%Y"))
          if (wife_death):
            if (birth_child > wife_death):
              print("Error: Wife: '" + wife["NAME"] + "' death on " + wife_death.strftime("%d-%b-%Y") + " is impossible for child: '" + individuals[chil_id]["NAME"] + "' to be born on " + birth_child.strftime("%d-%b-%Y"))


# Marriage before divorce
def check_marriage_divorce_dates(families, individuals):
  is_valid = True
  for id in families:
      if "DIV" in families[id]:
        divorce_date = datetime.strptime(families[id]["DIV"], "%d %b %Y")
        marriage_date = datetime.strptime(families[id]["MARR"], "%d %b %Y")
        if divorce_date < marriage_date:
          if (is_valid):
            print("Divorce before marriage is not possible\n")
          print("Husband: " + get_individual_name(families[id]["HUSB"], individuals).replace("/", "") + "\nWife: " + get_individual_name(families[id]["WIFE"], individuals).replace("/", ""))
          print("\nMarriage: " + families[id]["MARR"])
          print("Divorce: " + families[id]["DIV"])
          is_valid = False
  if not is_valid:
    return False
    sys.exit(1)
  return True

#US05 - Marriage before Death
def us_05(families,individuals):
    is_valid = True
    for id in families:
        if "MARR" in families[id]:
            marriage_Date = datetime.strptime(families[id]["MARR"], "%d %b %Y").date()
            husb_ID = families[id]["HUSB"]
            wife_ID = families[id]["WIFE"]
            if 'DEAT' in individuals[husb_ID]:
                husbDeath = datetime.strptime(individuals[husb_ID]["DEATH_DATE"],"%d %b %Y").date()
                if marriage_Date > husbDeath:
                    print("ERROR: FAMILY: US05: Marriage occurred after death of husband (" + get_individual_name(husb_ID,individuals).replace("/","") + ").")
                    is_valid = False
            if 'DEAT' in individuals[wife_ID]:
                wifeDeath = datetime.strptime(individuals[wife_ID]["DEATH_DATE"],"%d %b %Y").date()
                if marriage_Date > wifeDeath:
                    print("ERROR: FAMILY: US05: Marriage occurred after death of wife (" + get_individual_name(wife_ID,individuals).replace("/","")+ ").")
                    is_valid = False
    return is_valid

#US10 - Marriage after 14
def us_10(families,individuals):
    is_valid = True
    for id in families:
        if "MARR" in families[id]:
            marriage_Date = datetime.strptime(families[id]["MARR"], "%d %b %Y").date()
            husb_ID = families[id]["HUSB"]
            wife_ID = families[id]["WIFE"]
            husb_Bday = datetime.strptime(individuals[husb_ID]["DATE"], "%d %b %Y").date()
            wife_Bday = datetime.strptime(individuals[wife_ID]["DATE"], "%d %b %Y").date()
            husb_Age = (marriage_Date - husb_Bday).days / 365
            wife_Age = (marriage_Date - wife_Bday).days / 365
            if husb_Age < 14 and wife_Age < 14:
                print("ANOMALY: FAMILY: US10: Marriage happened before both husband ("+ get_individual_name(husb_ID,individuals).replace("/","") + ") and wife ("+get_individual_name(wife_ID,individuals).replace("/","")+ ") were 14.")
                is_valid = False
            elif husb_Age < 14:
                print("ANOMALY: FAMILY: US10: Marriage happened before husband ("+ get_individual_name(husb_ID,individuals).replace("/","") +") was 14.")
                is_valid = False
            elif wife_Age < 14:
                print("ANOMALY: FAMILY: US10: Marriage happened before wife ("+get_individual_name(wife_ID,individuals).replace("/","")+")was 14.")
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
    print_information()


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
