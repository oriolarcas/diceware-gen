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

import re

from generator import DicewareGenerator

class CatalanGenerator(DicewareGenerator):
    def __init__(self):
        super().__init__(
            self._replace_file_in_path(__file__, "words.txt"),
            self._replace_file_in_path(__file__, "symbols.yaml"),
            self._replace_file_in_path(__file__, "banned.txt")
        )

    def read_words(self):
        spaces = re.compile(r'\s+')
        with open(self.words_file, "r") as f:
            for l in f.readlines():
                _, w = spaces.split(l.strip())

                w = w.decode("utf-8")

                # Filter Catalan midpoint
                if u"\u00b7" in w:
                    continue

                yield w

if __name__ == '__main__':
    CatalanGenerator().gen_diceware_list()
