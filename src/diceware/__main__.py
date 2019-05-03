'''
Copyright (C) 2019 Oriol Arcas

This file is part of DicewareGen.

DicewareGen is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DicewareGen is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DicewareGen.  If not, see <https://www.gnu.org/licenses/>.
'''

import sys
import random

words = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        index, w = l.strip().split(" ")
        if not w:
            raise Exception("Empty line in diceware list")
        words.append(w)

rounds = -1
for i in range(10):
    if len(words) == 6**i:
        rounds = i
        break

if rounds < 0:
    raise Exception("Diceware list not a power of 6")
#print("Throwing %d dices for %d words" % (rounds, len(words)))

random.seed()
pwd = []
for _ in range(4):
    pwd.append(random.choice(words))

print("".join(pwd))
