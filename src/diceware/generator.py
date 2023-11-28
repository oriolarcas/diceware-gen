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

from time import time
from difflib import get_close_matches
from os import path
import json
import sys

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

class DicewareGenerator:
    def __init__(self, phrase_size:int, words_file:str, symbols:dict[str, str]=None, banned_path:str=None):
        self.phrase_size = phrase_size
        self.words_file : str = words_file
        self.translation : dict[str, str] = {}
        if symbols is not None:
            self.translation = symbols

        self.banned_list = set()
        if banned_path is not None:
            with open(banned_path) as banned_file:
                for l in banned_file.readlines():
                    w = l.strip()
                    if len(w) == 0 or w.startswith("#"):
                        continue
                    w = self.translate_word(w, self.translation)
                    self.banned_list.add(w)

    @staticmethod
    def _replace_file_in_path(file_path, new_file):
        return path.join(path.dirname(file_path), new_file)

    @staticmethod
    def _read_json(json_path):
        with open(json_path, "r") as json_file:
            return json.load(json_file)

    def translate_word(self, w, subs):
        for newc, oldcs in subs.items():
            for oldc in oldcs:
                w = w.replace(oldc, newc)
        return w

    def read_words(self):
        raise NotImplementedError

    def gen_diceware_list(self):
        total_words = 6**self.phrase_size

        last_time = time()
        last_index = 1

        accepted_keys = []
        accepted_words = {}
        index = 0
        for w_original in self.read_words():
            index += 1
            w = self.translate_word(w_original, self.translation)
            if len(w) <= 3:
                continue
            if w in self.banned_list:
                continue
            if get_close_matches(w, accepted_keys, 1, 0.7):
                continue
            accepted_keys.append(w)
            accepted_words[w] = w_original
            curr_time = time()
            sys.stderr.write("%d -> %d (%3d%%, %5d words/sec): %s\n" % (index,
                                                                 len(accepted_keys),
                                                                 len(accepted_keys) * 100. / total_words,
                                                                 (index - last_index) / (curr_time - last_time),
                                                                 w))
            last_time = curr_time
            last_index = index
            if len(accepted_keys) == total_words:
                break

        indexgen = IndexGen(list(map(str, range(1, 7))), self.phrase_size)
        final_list = []
        for k in sorted(accepted_words.keys()):
            final_list.append("%s\t%s" % (indexgen.next(), accepted_words[k]))
        sys.stdout.write("\n".join(final_list))

if __name__ == '__main__':
    lang = sys.argv[1]
    if lang == "ca":
        from diceware.lang.ca import CatalanGenerator
        CatalanGenerator().gen_diceware_list()
    elif lang == "es":
        from diceware.lang.es import SpanishGenerator
        SpanishGenerator().gen_diceware_list()
    else:
        raise ValueError("Unknown language")
