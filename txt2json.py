import sys
from collections import OrderedDict
import json

diceware = OrderedDict()

with open(sys.argv[1], "r") as dict_file:
    for line in dict_file.readlines():
        line = line.strip()

        if not line:
            continue

        index, word = line.split("\t")

        diceware[int(index)] = word

with open(sys.argv[2], "w") as output_json:
    json.dump(diceware, output_json, indent=2)
