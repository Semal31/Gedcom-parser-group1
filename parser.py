#!/usr/bin/python3.8

import sys
import getopt
import os

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


def print_information():
    print("Individuals")


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
                    id = tag[1:3]
                    parsing = arguments[0]
                    if parsing == "INDI":
                        individuals[id] = {}
                    else:
                        families[id] = {}
                else:
                    parsing = ""
            elif parsing and tag in TAGS:
                if parsing == "INDI":
                    individuals[id][tag] = " ".join(arguments)
                else:
                    families[id][tag] = " ".join(arguments)

    print("Individuals")
    print(individuals)
    print(families)


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
