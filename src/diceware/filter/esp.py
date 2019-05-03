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
import re
from time import time
from difflib import get_close_matches

class IndexGen:
    def __init__(self, sym, digits):
        self.sym = sym
        self.counters = [0] * digits
    
    def __iter__(self):
        return self

    def next(self):
        if self.counters is None:
            raise StopIteration

        current = "".join([self.sym[i] for i in reversed(self.counters)])
        for i in range(len(self.counters)):
            if self.counters[i] < len(self.sym) - 1:
                self.counters[i] += 1
                break
            self.counters[i] = 0
            if i == len(self.counters) - 1:
                self.counters = None
        return current

def translate_word(w, subs):
    for newc, oldcs in subs.items():
        for oldc in oldcs:
            w = w.replace(oldc, newc)
    return w

def filter_words_esp():
    translate = {}
    if len(sys.argv) == 4:
        with open(sys.argv[3]) as f:
            for l in f.readlines():
                cs = l.decode("utf-8").strip().split(" ")
                translate[cs[0]] = cs[1:]
    black_list = set()
    if len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            for l in f.readlines():
                w = l.strip()
                if len(w) == 0 or w[0] == "#":
                    continue
                w = translate_word(w.decode("utf-8"), translate)
                black_list.add(w)

    last_time = time()
    last_index = 1
    
    with open(sys.argv[1]) as f:
        spaces = re.compile(r'\s+')
        accepted_words = []
        index = 0
        for l in f.readlines():
            spl = spaces.split(l.strip())
            index += 1
            if len(spl) != 4:
                continue
            w_original = spl[1].decode("iso-8859-15")
            w = translate_word(w_original, translate)
            if len(w) <= 3:
                continue
            if w in black_list:
                continue
            if get_close_matches(w, accepted_words, 1, 0.7):
                continue
            accepted_words.append(w)
            curr_time = time()
            sys.stderr.write("%d -> %d (%5d words/sec): %s\n" % (index,
                                                               len(accepted_words),
                                                               (index - last_index) / (curr_time - last_time),
                                                               w.encode("utf-8")))
            last_time = curr_time
            last_index = index
            if len(accepted_words) == 6**4:
                break

        accepted_words.sort()
        indexgen = IndexGen([str(i + 1) for i in range(6)], 4)
        final_list = []
        for w in accepted_words:
            final_list.append("%s %s" % (indexgen.next(), w.encode("utf-8")))
        sys.stdout.write("\n".join(final_list))

if __name__ == '__main__':
    filter_words_esp()
