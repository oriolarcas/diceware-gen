'''
Created on Feb 28, 2019

@author: oriol
'''

import sys
import random

words = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        w = l.strip()
        if not w:
            raise Exception("Empty line in diceware list")
        words.append(l.strip())

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
