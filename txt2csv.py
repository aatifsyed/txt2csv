#!/usr/bin/env python3
"""
Text in, CSV out
"""
import re
import sys
import argparse

listofmodes = {
    "example" : [
        r"\) (?P<match>[\/a-zA-Z0-9_\.]*?),", # Matches path
        r"line (?P<match>[0-9]*?)$" # Matches lines number
    ]
}

def getinput():
    """
    Returns a list of non-blank lines, without newlines

    Fileinput.input() fetches from stdin or filename arguments
    """
    listoflines = []
    if not sys.stdin.isatty(): # We've been piped input
        listoflines = sys.stdin.readlines()
    listoflines = list(filter(lambda x: x != "\n", listoflines))
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

parser = argparse.ArgumentParser(description="Returns a comma-separated line for each line from stdin.")
parser.add_argument("--mode", "-m", required = True, help="Set of regular expressions to use. For each regular expression in that set, a single comma-separated value is added to the line")
args = parser.parse_args()

listoflines = getinput()

mode = "example"

for line in listoflines:
    listofvalues = applyregexes(mode, line)
    commaseparatedline = ",".join(listofvalues)
    print(commaseparatedline)
