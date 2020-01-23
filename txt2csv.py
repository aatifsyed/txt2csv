#!/usr/bin/env python3
"""
Text in, CSV out
"""
import re
import sys
import argparse

listofmodes = {
    "backtrace" : [
        r"[\)\]] (?P<match>[\/a-zA-Z0-9_\.]*?),", # Matches path
        r"line (?P<match>.*?)$" # Matches lines number
    ],
    "bricksoverview" : [
        r"^(?P<match>[0-9]*?) : ", # Match call load
        r"Packet Loss: (?P<match>.*?)%",
        r"Average Delay: (?P<match>.*?)us",
        r"Maximum Delay: (?P<match>.*?)us"
    ]
}

def getinput():
    """
    Returns a list of non-blank lines, without newlines
    """
    if not sys.stdin.isatty(): # We've been piped input
        listoflines = sys.stdin.readlines()
    else:
        raise Exception("\nCouldn't read anything from stdin\n\nTry piping to this program\ncat yourfile | txt2csv -m example")
    listoflines = list(map(lambda x: x.rstrip("\n"), listoflines))
    listoflines = list(filter(lambda x: x != "", listoflines))
    return listoflines

def applyregexes(mode, line):
    """
    Returns a list with the result of each regex in turn

    IN - mode : the key to the list of regexes in the modes dictionary
    IN - line : the string on which to perform the matching
    """
    matches = []

    try:
        regexlist = listofmodes[mode]
    except KeyError:
            print("\nCouldn't find mode!\nHave you specified it correctly?\nIs it in the list of modes?\n")
            raise

    for regex in regexlist:
        if re.search(regex, line):
            match = re.search(regex, line).group("match")
            matches.append(match)
        else:
            matches.append("") # Add an empty string so columns match
    return matches

def arguments():
    """
    Wrapper for argument parser to make main more readable
    """
    parser = argparse.ArgumentParser(description="Returns a comma-separated line for each line from stdin.")
    parser.add_argument("--mode", "-m", required = True, help="Required: Set of regular expressions to use. For each regular expression in that set, a single comma-separated value is added to the line")
    parser.add_argument("--separator", "-s", default=",", help="Optional: specify a separator string other than a comma")
    return parser.parse_args()

def txt2csv():
    args = arguments()
    mode = args.mode
    separator = args.separator

    listoflines = getinput()

    for line in listoflines:
        listofvalues = applyregexes(mode, line)
        commaseparatedline = separator.join(listofvalues)
        print(commaseparatedline)

if (__name__ == "__main__"):
    txt2csv()